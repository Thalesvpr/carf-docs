---
type: leaf
status: review
updated: 2026-02-08
---

# Sync Conflict Resolution

Especificacao detalhada do mecanismo de resolucao de conflitos do protocolo de sincronizacao entre o REURBCAD (mobile) e a GEOAPI (servidor). Conflitos ocorrem quando o mesmo registro e modificado tanto no servidor quanto no dispositivo mobile entre ciclos de sync.

## Estrategias por Campo

Cada campo sincronizavel possui uma estrategia de resolucao configurada. As tres estrategias possiveis sao:

- **SERVER_WINS**: o valor do servidor prevalece automaticamente. Usado para campos controlados por regras de negocio ou workflows do servidor.
- **CLIENT_WINS**: o valor do cliente prevalece automaticamente. Usado para campos de coleta de dados em campo.
- **MANUAL**: requer intervencao do usuario para escolher qual valor manter. Usado para campos complexos onde ambos os lados podem ter alteracoes legitimas.

### Tabela de Estrategias

| Campo | Entidade | Estrategia | Justificativa |
|-------|----------|-----------|--------------|
| status | Unit | SERVER_WINS | Status controlado por workflow no servidor (DRAFT -> PENDING -> APPROVED/REJECTED) |
| approved_at | Unit | SERVER_WINS | Aprovacao so acontece no servidor, via role MANAGER+ |
| approved_by | Unit | SERVER_WINS | Aprovacao so acontece no servidor, via role MANAGER+ |
| observation | Unit | CLIENT_WINS | Campo de texto livre editado em campo pelo agente |
| custom_data | Unit | CLIENT_WINS | Dados customizados coletados em campo (formularios dinamicos) |
| area | Unit | SERVER_WINS | Recalculado pelo PostGIS no servidor via ST_Area apos qualquer alteracao de geometria |
| geometry | Unit | MANUAL | Ambos podem editar; georreferenciador no QGIS e agente em campo. Requer visual diff |
| code | Unit | SERVER_WINS | Codigo gerado sequencialmente pelo servidor, nunca alterado pelo mobile |
| name | Holder | CLIENT_WINS | Correcao de nome em campo apos verificacao de documento |
| cpf | Holder | SERVER_WINS | Validacao Mod-11 e unicidade garantidas no servidor |
| email | Holder | CLIENT_WINS | Atualizado em campo pelo agente durante cadastro |
| phone | Holder | CLIENT_WINS | Atualizado em campo pelo agente durante cadastro |
| holder_type | Holder | SERVER_WINS | Tipo de titular (PF/PJ) validado com regras de negocio no servidor |
| ownership_percentage | UnitHolder | SERVER_WINS | Validacao de soma = 100% entre titulares e feita no servidor |
| is_primary | UnitHolder | SERVER_WINS | Regra de negocio: apenas um titular primario por unidade, validado no servidor |
| boundary | Community | MANUAL | Geometria complexa de limites de comunidade requer visual diff |
| name | Community | SERVER_WINS | Nome oficial da comunidade definido pela administracao |
| type | Community | SERVER_WINS | Tipo de comunidade (RURAL, URBAN, QUILOMBOLA, etc.) definido pela administracao |
| file_key | Document | SERVER_WINS | Chave de armazenamento definida pelo servidor (path no MinIO/S3) |
| file_name | Document | CLIENT_WINS | Nome original do arquivo, definido pelo usuario que fez upload |
| content_type | Document | SERVER_WINS | Validado e normalizado pelo servidor apos upload |
| size_bytes | Document | SERVER_WINS | Calculado pelo servidor apos receber o arquivo |

## Algoritmo de Resolucao

O algoritmo completo de resolucao de conflitos segue 9 passos:

### Passo 1: Receber Push

O cliente envia operacao de UPDATE com `baseVersion` indicando a versao do registro no momento em que o cliente o leu pela ultima vez.

### Passo 2: Comparar Versoes

O servidor compara `baseVersion` do cliente com `version` atual do registro no banco.

- Se `baseVersion == version`: nenhuma alteracao no servidor desde a leitura do cliente. Aceitar operacao diretamente, incrementar version.
- Se `baseVersion < version`: o registro foi alterado no servidor apos a leitura do cliente. Iniciar resolucao de conflito.
- Se `baseVersion > version`: situacao invalida (corrupcao de dados ou bug). Rejeitar operacao com erro.

### Passo 3: Reconstruir Base Record

O servidor utiliza a tabela de auditoria (audit_logs) para reconstruir o estado do registro na `baseVersion` que o cliente conhecia. Esse `baseRecord` serve como referencia para determinar quais campos foram alterados em cada lado.

### Passo 4: Detectar Campos Divergentes

Para cada campo sincronizavel, o servidor compara:

- `serverChanged`: campo atual no servidor difere do baseRecord
- `clientChanged`: campo enviado pelo cliente difere do baseRecord

Quatro cenarios possiveis por campo:

| Server Changed | Client Changed | Resultado |
|---------------|---------------|-----------|
| Nao | Nao | Campo inalterado, manter valor atual |
| Sim | Nao | Apenas servidor alterou, usar valor do servidor |
| Nao | Sim | Apenas cliente alterou, usar valor do cliente |
| Sim | Sim | Conflito real, aplicar estrategia do campo |

### Passo 5: Aplicar Estrategias

Para cada campo com conflito real (ambos alteraram):

- **SERVER_WINS**: usar valor do servidor no registro final
- **CLIENT_WINS**: usar valor do cliente no registro final
- **MANUAL**: adicionar a lista de campos pendentes de resolucao

### Passo 6: Verificar Resolucao Completa

Se todos os campos conflitantes foram auto-resolvidos (SERVER_WINS ou CLIENT_WINS), o servidor aplica o merge automaticamente, incrementa a version e retorna o resultado com `autoResolvedCompletely: true`.

### Passo 7: Retornar Conflitos Manuais

Se ha campos com estrategia MANUAL pendentes, o servidor retorna a resposta de conflito com `autoResolvedCompletely: false` e a lista de `divergentFields` para resolucao pelo usuario.

### Passo 8: Resolucao pelo Usuario

O app mobile exibe interface de resolucao lado a lado (ver secao UI Flow abaixo). O usuario escolhe qual valor manter para cada campo MANUAL ou edita manualmente um valor customizado.

### Passo 9: Submeter Resolucao

O cliente envia `POST /api/sync/resolve-conflict` com as escolhas do usuario. O servidor aplica as resolucoes, incrementa a version e retorna confirmacao.

## Manual Resolution UI Flow

A interface de resolucao manual do REURBCAD apresenta:

### Tela de Lista de Conflitos

Exibida quando o sync retorna um ou mais conflitos com resolucao manual pendente. Mostra lista de registros conflitantes com:

- Icone da entidade (unidade, titular, comunidade)
- Identificador do registro (codigo da unidade, nome do titular)
- Numero de campos pendentes de resolucao
- Data da ultima modificacao no servidor e no cliente

### Tela de Resolucao por Registro

Para cada registro conflitante, exibe comparacao campo a campo:

| Elemento | Descricao |
|----------|-----------|
| Campo | Nome do campo em conflito |
| Valor do Servidor | Valor atual no servidor, com data da alteracao |
| Valor do Cliente | Valor local no dispositivo, com data da alteracao |
| Botao "Manter versao do servidor" | Seleciona o valor do servidor |
| Botao "Manter minha versao" | Seleciona o valor do cliente |
| Botao "Editar manualmente" | Abre editor para o usuario digitar valor customizado |

Para campos de geometria (geometry, boundary), a comparacao e visual:

- Mapa exibe ambos os poligonos sobrepostos com cores distintas (servidor em azul, cliente em vermelho)
- O usuario pode alternar entre versoes para visualizar cada uma individualmente
- A opcao "Editar manualmente" abre o editor de geometria nativo do app

### Regras da Interface

- O usuario deve resolver TODOS os campos pendentes antes de submeter
- Botao "Resolver" so e habilitado quando todas as escolhas foram feitas
- Opcao "Resolver todos como servidor" e "Resolver todos como meu" para agilizar
- Apos submeter, o registro e atualizado localmente com os valores resolvidos

## Timeout de Resolucao

Conflitos manuais tem prazo de 24 horas para resolucao. Se o usuario nao resolver dentro desse prazo:

1. O servidor aplica fallback SERVER_WINS para todos os campos pendentes
2. No proximo pull, o cliente recebe a versao final do servidor
3. A versao local e sobrescrita com a versao do servidor
4. O app exibe notificacao informando que conflitos foram resolvidos automaticamente por timeout

Esse mecanismo evita que conflitos pendentes bloqueiem a sincronizacao indefinidamente.

## Cenarios de Conflito Comuns

### Cenario 1: Agente edita observacao enquanto analista altera status

- Agente em campo edita `observation` da unidade (offline)
- Analista no REURBWEB altera `status` de DRAFT para PENDING
- No sync: `observation` -> CLIENT_WINS (valor do agente), `status` -> SERVER_WINS (valor do analista)
- Resultado: merge automatico, sem intervencao manual

### Cenario 2: Dois dispositivos editam a mesma geometria

- Agente A edita geometria da unidade no campo
- Georreferenciador edita mesma geometria no QGIS via GEOGIS
- No sync do Agente A: `geometry` -> MANUAL
- Agente A ve comparacao visual e escolhe a versao mais precisa

### Cenario 3: Titular renomeado em ambos os lados

- Agente corrige nome do titular em campo: "Maria Silva" -> "Maria da Silva Santos"
- Analista corrige no REURBWEB: "Maria Silva" -> "Maria S. Santos"
- No sync: `name` -> CLIENT_WINS (valor do agente, pois verificou documento em campo)
- Analista ve a alteracao no proximo acesso ao REURBWEB

### Cenario 4: Percentual de propriedade alterado

- Agente define ownership_percentage como 50% para titular A
- Servidor ja atualizou para 60% (apos ajuste do analista para manter soma = 100%)
- No sync: `ownership_percentage` -> SERVER_WINS (servidor garante consistencia da soma)
- Cliente recebe o valor correto no proximo pull