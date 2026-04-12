---
type: leaf
status: review
updated: 2026-02-08
---

# Database Tests

Este documento detalha os testes de integracao que validam constraints, triggers, RLS (Row Level Security), migrations e funcionalidades PostGIS diretamente no banco PostgreSQL. Utilizam Testcontainers com a imagem postgis/postgis:16-3.4 para garantir ambiente identico ao de producao.

## Infraestrutura de Teste

Os testes de banco utilizam a mesma `DatabaseFixture` descrita em `01-repository-tests.md`. Adicionalmente, alguns testes executam SQL bruto via `context.Database.ExecuteSqlRawAsync()` para validar comportamentos que nao sao expostos pela camada de repositorio.

Para testes que manipulam RLS, a fixture configura a variavel de sessao `app.current_tenant` via SQL:

`SET app.current_tenant = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';`

## Testes de Constraints CHECK

Constraints CHECK validam invariantes a nivel de banco, funcionando como ultima linha de defesa apos a validacao no dominio.

### Constraint: area > 0

| Cenario | SQL/Acao | Resultado Esperado |
|---------|----------|--------------------|
| Area positiva | INSERT com area = 1500.5 | Insert bem-sucedido |
| Area zero | INSERT com area = 0 | Lanca PostgresException com violacao de CHECK constraint |
| Area negativa | INSERT com area = -100 | Lanca PostgresException com violacao de CHECK constraint |
| Area nula | INSERT com area = NULL | Lanca PostgresException (coluna NOT NULL) |

### Constraint: ownership_percentage entre 0 e 100

| Cenario | SQL/Acao | Resultado Esperado |
|---------|----------|--------------------|
| Percentual 50% | INSERT unit_holders com percentage = 50.00 | Insert bem-sucedido |
| Percentual 0% | INSERT com percentage = 0.00 | Insert bem-sucedido (titular sem percentual definido) |
| Percentual 100% | INSERT com percentage = 100.00 | Insert bem-sucedido |
| Percentual negativo | INSERT com percentage = -1.00 | Lanca PostgresException violacao CHECK |
| Percentual acima de 100 | INSERT com percentage = 100.01 | Lanca PostgresException violacao CHECK |

### Constraint: unit code unico por tenant

| Cenario | SQL/Acao | Resultado Esperado |
|---------|----------|--------------------|
| Codigo unico no tenant | INSERT UNI-2026-00001 no TenantA | Insert bem-sucedido |
| Mesmo codigo no mesmo tenant | INSERT UNI-2026-00001 no TenantA novamente | Lanca PostgresException violacao UNIQUE |
| Mesmo codigo em tenant diferente | INSERT UNI-2026-00001 no TenantB | Insert bem-sucedido (UNIQUE scoped por tenant) |

### Constraint: CPF unico por tenant

| Cenario | SQL/Acao | Resultado Esperado |
|---------|----------|--------------------|
| CPF unico no tenant | INSERT holder com CPF 52998224725 no TenantA | Insert bem-sucedido |
| Mesmo CPF no mesmo tenant | INSERT holder com CPF 52998224725 no TenantA novamente | Lanca PostgresException violacao UNIQUE |
| Mesmo CPF em tenant diferente | INSERT holder com CPF 52998224725 no TenantB | Insert bem-sucedido |

### Constraints de Foreign Key

| Cenario | Constraint | Resultado Esperado |
|---------|------------|--------------------|
| FK unit_holders -> units (cascade) | DELETE unit com holders vinculados | Holders removidos em cascata |
| FK unit_holders -> holders (restrict) | DELETE holder que esta vinculado a unidade | Lanca PostgresException violacao FK (RESTRICT) |
| FK documents -> units (cascade) | DELETE unit com documentos | Documentos removidos em cascata |
| FK units -> communities (restrict) | DELETE community com unidades | Lanca PostgresException violacao FK (RESTRICT) |
| FK valida | INSERT unit_holder com unit_id existente | Insert bem-sucedido |
| FK invalida | INSERT unit_holder com unit_id inexistente | Lanca PostgresException violacao FK |

## Testes de Triggers

Triggers implementam validacoes complexas que requerem consulta a multiplas linhas.

### Trigger: soma ownership_percentage = 100% na submissao

Este trigger valida que a soma dos percentuais de titularidade de uma unidade e exatamente 100% quando o status muda para Pending.

| Cenario | Setup | Acao | Resultado Esperado |
|---------|-------|------|--------------------|
| Soma correta | Holder A 60%, Holder B 40% | UPDATE status para Pending | Update bem-sucedido |
| Soma incompleta | Holder A 60%, Holder B 30% (90%) | UPDATE status para Pending | Lanca PostgresException mensagem "ownership must sum to 100%" |
| Soma excedente | Holder A 60%, Holder B 50% (110%) | UPDATE status para Pending | Lanca PostgresException |
| Sem holders | Nenhum holder vinculado | UPDATE status para Pending | Lanca PostgresException mensagem "at least one holder required" |
| Nao validado em Draft | Holder A 50% (incompleto) | UPDATE outros campos mantendo Draft | Update bem-sucedido (trigger so dispara na transicao para Pending) |

### Trigger: exatamente um titular primario por unidade

Este trigger garante que cada unidade tem no maximo um holder com `is_primary = true`.

| Cenario | Setup | Acao | Resultado Esperado |
|---------|-------|------|--------------------|
| Primeiro titular primario | Unidade sem primario | INSERT holder com is_primary = true | Insert bem-sucedido |
| Segundo titular primario | Unidade ja tem primario | INSERT holder com is_primary = true | Lanca PostgresException mensagem "only one primary holder allowed" |
| Alterar primario | Holder A primario, Holder B nao | UPDATE Holder A is_primary = false, UPDATE Holder B is_primary = true (transacao) | Update bem-sucedido |
| Titular nao-primario | Unidade ja tem primario | INSERT holder com is_primary = false | Insert bem-sucedido |

## Testes de RLS (Row Level Security)

Os testes de RLS validam o isolamento completo entre tenants a nivel de banco de dados. Cada teste configura a variavel de sessao `app.current_tenant` e verifica que somente os dados do tenant corrente sao vissiveis.

### Setup de RLS

Antes de cada teste, a fixture executa:

1. `SET app.current_tenant = '<tenant_a_id>';` - Define o tenant da sessao
2. Insere dados no TenantA atraves do contexto configurado
3. Abre nova conexao, executa `SET app.current_tenant = '<tenant_b_id>';`
4. Insere dados no TenantB

### Cenarios de Isolamento

| Cenario | Setup | Query | Resultado Esperado |
|---------|-------|-------|--------------------|
| Select isolado - units | 3 units em TenantA, 2 units em TenantB | SELECT * FROM units (sessao TenantA) | Retorna apenas 3 units |
| Select isolado - holders | 2 holders em TenantA, 3 holders em TenantB | SELECT * FROM holders (sessao TenantA) | Retorna apenas 2 holders |
| Select isolado - communities | 1 community em cada tenant | SELECT * FROM communities (sessao TenantB) | Retorna apenas 1 community |
| Select por ID cross-tenant | Unit com ID conhecido no TenantA | SELECT * FROM units WHERE id = X (sessao TenantB) | Retorna 0 linhas (nao nulo, conjunto vazio) |
| Insert respeita tenant | Sessao TenantA | INSERT unit sem especificar tenant_id | tenant_id preenchido automaticamente com TenantA |
| Update cross-tenant bloqueado | Unit no TenantA | UPDATE units SET ... WHERE id = X (sessao TenantB) | 0 linhas afetadas |
| Delete cross-tenant bloqueado | Unit no TenantA | DELETE FROM units WHERE id = X (sessao TenantB) | 0 linhas afetadas |
| Join respeita RLS | Units e holders em ambos os tenants | SELECT u.*, h.* FROM units u JOIN unit_holders uh ... JOIN holders h ... (sessao TenantA) | Retorna apenas dados do TenantA |
| Subquery respeita RLS | Communities em ambos os tenants | SELECT * FROM units WHERE community_id IN (SELECT id FROM communities) (sessao TenantA) | Retorna apenas units de communities do TenantA |
| Sem tenant definido | Nenhum SET app.current_tenant | SELECT * FROM units | Retorna 0 linhas (politica default deny) |

### Verificacao SQL Detalhada

Para cada cenario de RLS, o teste executa SQL bruto e verifica o resultado:

```
-- Arranjo: inserir dados como TenantA
SET app.current_tenant = 'aaaa...';
INSERT INTO units (id, code, tenant_id, ...) VALUES (...);

-- Acao: tentar acessar como TenantB
SET app.current_tenant = 'bbbb...';
SELECT count(*) FROM units WHERE id = '<id_da_unit_de_A>';

-- Verificacao: count deve ser 0
```

## Testes de Migrations

Os testes de migrations validam que o schema do banco e consistente apos a execucao de todas as migrations e que as migrations sao idemopotentes.

### Cenarios

| Cenario | Acao | Resultado Esperado |
|---------|------|--------------------|
| Migrate up completo | Executar todas as migrations do zero | Schema criado sem erros, todas as tabelas existem |
| Migrate up idempotente | Executar Migrate() duas vezes seguidas | Segunda execucao nao lanca excecao (migrations ja aplicadas) |
| Schema consistency | Apos migrate, comparar com model snapshot | Nenhuma diferenca detectada pelo HasPendingModelChanges |
| Tabela units existe | Apos migrate | Tabela units existe com todas as colunas esperadas |
| Tabela holders existe | Apos migrate | Tabela holders existe com coluna cpf VARCHAR(11) |
| Tabela communities existe | Apos migrate | Tabela communities existe com coluna boundary geometry(Polygon, 4326) |
| Indices espaciais criados | Apos migrate | Indice GiST em units.geometry existe |
| Indices de tenant criados | Apos migrate | Indice B-tree em tenant_id existe em todas as tabelas multi-tenant |
| RLS policies ativas | Apos migrate | Politica de RLS habilitada em units, holders, communities |
| Extension PostGIS | Apos migrate | Extension postgis instalada |
| Extension uuid-ossp | Apos migrate | Extension uuid-ossp instalada |
| Coluna version existe | Apos migrate | Coluna version (INTEGER) existe em units, holders, communities (para sync mobile) |

### Verificacao de Schema

Os testes consultam `information_schema.columns` e `pg_indexes` para validar a estrutura:

- `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'units'` - verifica colunas
- `SELECT indexname FROM pg_indexes WHERE tablename = 'units' AND indexdef LIKE '%gist%'` - verifica indice GiST
- `SELECT polname FROM pg_policy WHERE polrelid = 'units'::regclass` - verifica politica RLS

## Testes PostGIS

Os testes PostGIS validam que as funcoes espaciais funcionam corretamente e que os indices GiST sao utilizados pelo query planner.

### Funcoes Espaciais

| Cenario | Funcao PostGIS | Resultado Esperado |
|---------|---------------|--------------------|
| Intersecao entre poligonos | ST_Intersects(geomA, geomB) | Retorna verdadeiro para poligonos sobrepostos |
| Sem intersecao | ST_Intersects(geomA, geomC) | Retorna falso para poligonos distantes |
| Contencao | ST_Contains(community_boundary, unit_geometry) | Retorna verdadeiro quando unit esta dentro da community |
| Nao contido | ST_Contains(community_boundary, unit_fora) | Retorna falso quando unit esta fora |
| Area em metros quadrados | ST_Area(ST_Transform(geom, 31983)) | Area aproximada do poligono em m2 |
| Centroide | ST_Centroid(geom) | Ponto central do poligono |
| Bounding box | ST_Intersects(geom, ST_MakeEnvelope(xmin, ymin, xmax, ymax, 4326)) | Filtra por envelope geografico |
| Distancia | ST_Distance(ST_Transform(geomA, 31983), ST_Transform(geomB, 31983)) | Distancia em metros entre dois pontos |
| Buffer | ST_Buffer(ST_Transform(geom, 31983), 10) | Poligono expandido em 10m |
| Validacao | ST_IsValid(geom) | Retorna verdadeiro para geometria valida |
| Simplificacao | ST_Simplify(geom, 0.0001) | Geometria simplificada com menos vertices |

### Performance de Indices GiST

| Cenario | Query | Verificacao |
|---------|-------|-----------  |
| Indice GiST utilizado em ST_Intersects | EXPLAIN ANALYZE SELECT * FROM units WHERE ST_Intersects(geometry, ...) | Plano de execucao contem "Index Scan using ix_units_geometry" |
| Indice GiST utilizado em ST_Contains | EXPLAIN ANALYZE SELECT * FROM units WHERE ST_Contains(geometry, ...) | Plano de execucao contem referencia ao indice GiST |
| Indice GiST utilizado em bounding box | EXPLAIN ANALYZE SELECT * FROM units WHERE geometry && ST_MakeEnvelope(...) | Plano de execucao contem "Bitmap Index Scan" no indice GiST |
| Sem Seq Scan em tabela grande | Tabela com 1000+ geometrias, query espacial | Plano de execucao nao contem "Seq Scan on units" |

Para validar o uso de indice, o teste executa `EXPLAIN (ANALYZE, FORMAT JSON)` e parseia o JSON resultante verificando que o campo `Node Type` contem `Index Scan` ou `Bitmap Index Scan`.

## Tabela Resumo

| Categoria | Total de Cenarios | Foco |
|-----------|-------------------|------|
| Constraints CHECK | 12 | Invariantes numéricas (area, percentual) |
| Constraints UNIQUE | 6 | Unicidade scoped por tenant |
| Constraints FK | 6 | Integridade referencial, cascade/restrict |
| Triggers | 9 | Validacoes multi-linha (soma percentual, primary holder) |
| RLS | 10 | Isolamento multi-tenant completo |
| Migrations | 11 | Consistencia de schema, idempotencia |
| PostGIS funcoes | 11 | Funcoes espaciais, validacao de geometria |
| PostGIS performance | 4 | Uso de indices GiST |
| **Total** | **69** | |

## Referencias Cruzadas

- Mapeamento DbContext: `INFRA/PERSISTENCE/01-dbcontext.md`
- Testes de repositorios: `TESTS/INTEGRATION/01-repository-tests.md`
- Value objects de geometria: `DOMAIN/VALUE-OBJECTS/GEO/`
- Modelo ER: `CENTRAL/DOMAIN/DIAGRAMS/02-er-diagram.md`
- Multi-tenancy: `CENTRAL/DOMAIN/DIAGRAMS/03-multi-tenancy.md`
