---
type: leaf
status: approved
updated: 2026-02-07
---

# CQRS

Command Query Responsibility Segregation separa operacoes de escrita (commands) de operacoes de leitura (queries) em pipelines distintos, permitindo otimizacoes independentes para cada lado. Na GEOAPI, ambos os lados passam pelo MediatR mas seguem regras e convencoes diferentes.

## Commands

Commands representam intencao de escrita: criar, atualizar, deletar ou transicionar estado. Cada command e um record imutavel contendo exatamente os dados necessarios para a operacao. CreateUnitCommand contem endereco, community_id e coordenadas. ApproveUnitCommand contem unit_id e justificativa. LinkHolderCommand contem unit_id, holder_id, relationship_type e ownership_percentage.

Cada command tem um handler correspondente que recebe o command, executa a logica de negocio via entidades de dominio, persiste as mudancas e retorna um Result indicando sucesso ou falha. O handler nunca retorna DTOs complexos, apenas o ID do recurso criado ou um resultado vazio para operacoes de atualizacao. Apos SaveChanges bem-sucedido, os domain events coletados pela entidade sao despachados via MediatR para handlers assincrono.

Antes de chegar ao handler, o command passa pelo pipeline MediatR. O ValidationBehavior executa o FluentValidation correspondente (CreateUnitCommandValidator verifica campos obrigatorios, formatos e regras de negocio simples). Se a validacao falha, o pipeline retorna erro VALIDATION_ERROR sem executar o handler. O TransactionBehavior envolve a execucao em transacao: se o handler ou qualquer domain event handler lancar excecao, toda a operacao sofre rollback.

Commands executam em transacoes ACID do PostgreSQL garantindo atomicidade. Criar unidade, vincular titular e disparar evento acontecem como operacao atomica: tudo ou nada.

## Queries

Queries representam leitura pura de dados. Cada query retorna DTOs flat otimizados para a necessidade especifica do consumidor. GetUnitByIdQuery retorna UnitDetailDto com todos os campos da unidade incluindo titulares e documentos. ListUnitsByCommunityQuery retorna PaginatedResult de UnitListItemDto com apenas os campos necessarios para listagem.

Handlers de queries nunca alteram estado. Sao seguros para executar multiplas vezes sem efeitos colaterais (idempotentes). Usam projecoes EF Core via Select para materializar apenas as colunas necessarias, minimizando dados trafegados entre banco e aplicacao. Queries de listagem desabilitam tracking do EF Core via AsNoTracking para otimizar performance pois os objetos retornados nao serao modificados.

Queries frequentes e relativamente estaticas usam cache Redis. Listagens de comunidades do tenant tem TTL de 5 minutos pois mudam raramente. Listagens de unidades com filtros dinamicos tem TTL de 30 segundos. O cache e invalidado pelo domain event handler correspondente: UnitCreatedEvent invalida o cache de listagem de unidades da comunidade afetada.

Paginacao padrao em todas as queries de listagem: parametro page (default 1) e limit (default 20, maximo 100). Response inclui total, page, limit e hasNext. Ordenacao configuravel por campos permitidos, variando por entidade.

## Pipeline MediatR

O pipeline MediatR intercepta tanto commands quanto queries em ordem configurada. LoggingBehavior registra o inicio e fim de cada operacao com duracao em milissegundos para monitoramento de performance. ValidationBehavior executa FluentValidation e retorna erros formatados antes de chegar ao handler. Para commands, TransactionBehavior gerencia o escopo da transacao. Para queries, CachingBehavior verifica e atualiza o cache Redis quando aplicavel.

Essa separacao permite que novos behaviors sejam adicionados ao pipeline sem modificar handlers existentes. Um AuditBehavior futuro pode registrar todas as operacoes sem tocar em nenhum command handler.
