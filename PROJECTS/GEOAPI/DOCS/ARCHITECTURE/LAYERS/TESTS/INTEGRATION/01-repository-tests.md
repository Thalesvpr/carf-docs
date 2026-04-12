---
type: leaf
status: review
updated: 2026-02-08
---

# Repository Integration Tests

Os testes de integracao de repositorios validam que a camada de persistencia interage corretamente com o banco PostgreSQL real, incluindo extensoes PostGIS e filtros de multi-tenancy. Utilizam TestContainers para provisionar um container PostgreSQL efemero com a imagem postgis/postgis:16-3.4.

## Setup com Testcontainers

### Container PostgreSQL + PostGIS

A classe `DatabaseFixture` implementa `IAsyncLifetime` e gerencia o ciclo de vida completo do container de banco de dados.

**Inicializacao (InitializeAsync):**

1. Cria o container PostgreSQL usando `new PostgreSqlBuilder()` com imagem `postgis/postgis:16-3.4`
2. Configura usuario (`carf_test`), senha (`test_password`), database (`carf_test_db`)
3. Inicia o container com `container.StartAsync()`
4. Obtem a connection string do container via `container.GetConnectionString()`
5. Constroi as opcoes do DbContext: `optionsBuilder.UseNpgsql(connectionString, o => o.UseNetTopologySuite())`
6. Instancia o `CARFDbContext` com um `TenantContext` de teste (tenant fixo)
7. Executa todas as migrations via `context.Database.MigrateAsync()`
8. Verifica que as extensions PostGIS e uuid-ossp estao instaladas

**Finalizacao (DisposeAsync):**

1. Dispose do DbContext
2. Destruicao do container via `container.DisposeAsync()`

### Escolha: MigrateAsync vs EnsureCreated

O projeto utiliza `MigrateAsync()` (e nao `EnsureCreatedAsync()`) nos testes de integracao pelos seguintes motivos:

| Aspecto | MigrateAsync | EnsureCreatedAsync |
|---------|-------------|-------------------|
| Executa migrations | Sim, todas em ordem | Nao, cria schema diretamente do model |
| Triggers e functions | Criados pelas migrations SQL | Nao criados (apenas estrutura de tabelas) |
| RLS policies | Aplicadas pelas migrations | Nao aplicadas |
| Indices customizados | Criados pelas migrations | Apenas indices do EF Core |
| Fidelidade ao producao | Alta (mesmo caminho) | Baixa (atalho) |
| Velocidade | Mais lento (~2-5s) | Mais rapido (~1s) |

A escolha por `MigrateAsync` garante que os testes validam exatamente o mesmo schema que sera aplicado em producao, incluindo triggers, RLS policies e indices espaciais GiST.

### Connection String do Container

A connection string e obtida dinamicamente do container, eliminando dependencia de banco local:

`Host=localhost;Port={dynamic_port};Database=carf_test_db;Username=carf_test;Password=test_password`

A porta e alocada dinamicamente pelo Testcontainers para evitar conflitos. O metodo `container.GetConnectionString()` retorna a string completa com a porta correta.

### Configuracao do NetTopologySuite

A extensao NetTopologySuite e necessaria para que o Npgsql mapeie corretamente tipos PostGIS (geometry, geography) para tipos .NET (Geometry, Point, Polygon do NTS). Configurada via:

`optionsBuilder.UseNpgsql(connectionString, o => o.UseNetTopologySuite())`

## Cleanup entre Testes

### Padrao Transaction Rollback

Para garantir isolamento entre testes sem recriar o container, cada teste executa dentro de uma transacao que e revertida ao final:

**Setup (construtor do teste ou InitializeAsync do test class):**

1. `transaction = await context.Database.BeginTransactionAsync()` - abre transacao
2. Executa seed de dados de teste dentro da transacao

**Teardown (Dispose ou DisposeAsync):**

1. `await transaction.RollbackAsync()` - reverte todas as mudancas
2. `transaction.Dispose()` - libera a transacao

Esse padrao garante que:

- Cada teste comeca com o banco no estado limpo (apenas schema + dados de seed da fixture)
- Testes podem ser executados em qualquer ordem
- Nao ha vazamento de estado entre testes
- A velocidade e mantida (nao precisa recriar/remigrar o banco)

### Alternativa: Respawn

Para cenarios complexos onde o transaction rollback nao funciona (por exemplo, testes que precisam de commits intermediarios), o projeto oferece a alternativa `Respawn`:

1. Instanciar `Respawner` com tabelas a serem preservadas
2. Apos cada teste, chamar `respawner.ResetAsync(connectionString)`
3. Respawn trunca todas as tabelas exceto as configuradas

## Verificacao de RLS

### Como testar isolamento multi-tenant

Os testes de RLS validam que o PostgreSQL Row Level Security impede acesso cross-tenant. O padrao de teste:

1. Configura sessao como TenantA: `SET app.current_tenant = '{tenantA_id}'`
2. Insere dados como TenantA
3. Configura sessao como TenantB: `SET app.current_tenant = '{tenantB_id}'`
4. Tenta acessar dados de TenantA — resultado esperado e conjunto vazio
5. Insere dados como TenantB
6. Reconfigura sessao como TenantA
7. Verifica que so ve seus proprios dados

Para executar SQL que altera a variavel de sessao, os testes usam:

`await context.Database.ExecuteSqlRawAsync("SET app.current_tenant = '{tenantId}'");`

### Verificacao por Repositorio

Alem dos testes SQL brutos (descritos em `02-database-tests.md`), cada repositorio e testado via interface C# para confirmar que os global query filters do EF Core aplicam o filtro de tenant:

| Cenario | Setup | Query | Verificacao |
|---------|-------|-------|-----------  |
| GetByIdAsync cross-tenant | Unit no TenantA, contexto TenantB | repo.GetByIdAsync(unitAId) | Retorna null |
| ListAsync isolado | 3 units TenantA, 2 units TenantB | repo.ListAsync() (contexto TenantA) | Retorna 3 units |
| CountAsync isolado | 5 units TenantA, 3 units TenantB | repo.CountAsync() (contexto TenantA) | Retorna 5 |

## Cenarios do UnitRepository

A classe `UnitRepositoryTests` exercita as operacoes do repositorio de unidades contra o banco real.

| Repository | Metodo | Cenarios de Teste | Dados de Setup |
|------------|--------|-------------------|----------------|
| UnitRepository | AddAsync | Persistir unidade valida, verificar Id e Code gerados | Community pre-existente |
| UnitRepository | GetByIdAsync | Buscar unidade existente, buscar inexistente (retorna null), buscar cross-tenant (retorna null) | 1 unit no TenantA, 1 unit no TenantB |
| UnitRepository | UpdateAsync | Atualizar endereco, atualizar geometria, atualizar status | Unit Draft pre-existente |
| UnitRepository | DeleteAsync | Excluir unidade existente, excluir com cascade (documentos e holders removidos) | Unit com holders e documentos |
| UnitRepository | ListAsync | Paginacao (page 1, page 2), filtro por status, filtro por community, ordenacao por data | 20 units com status variados |
| UnitRepository | HasOverlapAsync | Poligono sobreposto retorna verdadeiro, poligono distante retorna falso, overlap com a propria unidade (excluida) retorna falso | 2 units com geometrias conhecidas |
| UnitRepository | ListByBoundingBoxAsync | Retorna units dentro do bbox, exclui units fora | 3 units em posicoes conhecidas, bbox configurado |
| UnitRepository | CountByStatusAsync | Conta units por status no tenant | 5 Draft, 3 Pending, 2 Approved |
| UnitRepository | GetByCodeAsync | Busca por codigo (UNI-2026-00001) | Unit com codigo conhecido |

## Cenarios do HolderRepository

| Repository | Metodo | Cenarios de Teste | Dados de Setup |
|------------|--------|-------------------|----------------|
| HolderRepository | AddAsync | Persistir holder pessoa fisica, persistir pessoa juridica | Nenhum dado previo |
| HolderRepository | GetByIdAsync | Buscar holder existente, cross-tenant retorna null | 1 holder por tenant |
| HolderRepository | GetByCpfAsync | Buscar por CPF valido, CPF inexistente retorna null, CPF de outro tenant retorna null | Holders com CPFs conhecidos |
| HolderRepository | ListByUnitIdAsync | Retorna todos os holders vinculados a uma unidade | Unit com 3 holders vinculados |
| HolderRepository | SearchAsync | Busca por nome parcial (LIKE), busca por CPF parcial | 10 holders com nomes variados |
| HolderRepository | ExistsByCpfAsync | CPF existente retorna verdadeiro, CPF inexistente retorna falso | Holder com CPF conhecido |

## Cenarios do CommunityRepository

| Repository | Metodo | Cenarios de Teste | Dados de Setup |
|------------|--------|-------------------|----------------|
| CommunityRepository | AddAsync | Persistir community com boundary PostGIS | Nenhum dado previo |
| CommunityRepository | GetByIdAsync | Buscar existente, cross-tenant retorna null | 1 community por tenant |
| CommunityRepository | ListAsync | Paginacao, filtro por tipo (REURB_S, Quilombola), ordenacao | 10 communities |
| CommunityRepository | ExistsByNameAsync | Nome existente no tenant retorna verdadeiro, mesmo nome em outro tenant retorna falso | Community com nome conhecido |
| CommunityRepository | GetContainingPointAsync | Ponto dentro do boundary retorna community, ponto fora retorna null | Community com boundary conhecido |
| CommunityRepository | GetWithUnitsAsync | Retorna community com units carregadas (eager loading) | Community com 5 units |

## Cenarios do DocumentRepository

| Repository | Metodo | Cenarios de Teste | Dados de Setup |
|------------|--------|-------------------|----------------|
| DocumentRepository | AddAsync | Persistir documento com metadados | Unit pre-existente |
| DocumentRepository | ListByEntityAsync | Retorna documentos de uma unidade, retorna vazio para entidade sem documentos | Unit com 3 documentos |
| DocumentRepository | GetByIdAsync | Buscar documento existente, cross-tenant retorna null | 1 documento por tenant |
| DocumentRepository | DeleteAsync | Excluir documento | Documento pre-existente |

## Aspectos Validados

Esses testes garantem que:

1. As queries espaciais do PostGIS (ST_Intersects, ST_Contains, ST_Within) funcionam corretamente com os mapeamentos NetTopologySuite
2. Os global query filters de multi-tenancy aplicam o isolamento por tenant em todas as consultas
3. As migrations produzem um schema compativel com os mapeamentos do Entity Framework Core
4. A paginacao funciona corretamente com Skip/Take sobre queries ordenadas
5. Os indices GiST sao utilizados nas queries espaciais (validado em `02-database-tests.md`)
6. O cascade delete remove entidades dependentes corretamente
7. A coluna `version` e incrementada em cada update (essencial para sync mobile)

## Tabela Resumo

| Repository | Total de Cenarios | Metodos Testados |
|------------|-------------------|-----------------|
| UnitRepository | 18 | 9 |
| HolderRepository | 11 | 6 |
| CommunityRepository | 10 | 6 |
| DocumentRepository | 6 | 4 |
| **Total** | **45** | **25** |

## Referencias Cruzadas

- Testes de banco de dados (constraints, triggers, RLS, migrations): `TESTS/INTEGRATION/02-database-tests.md`
- DbContext e mapeamentos: `INFRA/PERSISTENCE/01-dbcontext.md`
- Estrategia de testes: `TESTS/00-testing-strategy.md`
- Multi-tenancy: `CENTRAL/DOMAIN/DIAGRAMS/03-multi-tenancy.md`
- Entidades: `DOMAIN/ENTITIES/`
