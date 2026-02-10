---
type: leaf
status: review
updated: 2026-02-08
---

# RLS Setup (Row Level Security)

Documentacao completa da configuracao de Row Level Security no PostgreSQL para isolamento multi-tenant da GEOAPI. O RLS garante que queries executadas pela aplicacao retornem apenas dados do tenant correto, mesmo que o codigo da aplicacao nao inclua filtro WHERE por tenant_id.

## Visao Geral

O isolamento multi-tenant da GEOAPI combina tres mecanismos:

1. **JWT Claim**: o token do Keycloak contem claim `tenant_id` identificando o tenant do usuario
2. **TenantMiddleware**: extrai `tenant_id` do JWT e define variavel de sessao no PostgreSQL
3. **RLS Policies**: filtram automaticamente todas as queries pela variavel de sessao

Essa abordagem e mais segura que filtros na aplicacao pois opera no nivel do banco de dados, prevenindo vazamento de dados mesmo em caso de bug no codigo.

## Passo 1: Application Role

O primeiro passo e criar um role de aplicacao que NAO seja superuser, pois superusers bypassam RLS automaticamente.

```sql
-- Criar role de aplicacao (NAO superuser)
CREATE ROLE geoapi_app LOGIN PASSWORD 'xxx';

-- Conceder permissoes basicas
GRANT USAGE ON SCHEMA public TO geoapi_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO geoapi_app;

-- Conceder permissoes em sequences (para colunas serial/identity)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO geoapi_app;

-- Garantir que novas tabelas tambem recebam permissoes
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO geoapi_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO geoapi_app;
```

A connection string da GEOAPI em todos os ambientes deve utilizar o role `geoapi_app`, NUNCA o role `postgres` (superuser).

## Passo 2: Habilitar RLS

Habilitar RLS em todas as tabelas que possuem coluna `tenant_id`:

```sql
-- Tabelas de dominio
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE holders ENABLE ROW LEVEL SECURITY;
ALTER TABLE unit_holders ENABLE ROW LEVEL SECURITY;
ALTER TABLE communities ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE blocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE plots ENABLE ROW LEVEL SECURITY;

-- Tabelas de equipe
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_authorizations ENABLE ROW LEVEL SECURITY;

-- Tabelas de autenticacao e sessao
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Tabelas de workflow
ALTER TABLE legitimation_requests ENABLE ROW LEVEL SECURITY;

-- Tabela de auditoria
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
```

Tabelas sem `tenant_id` (ex: migrations, configuracoes globais) NAO recebem RLS.

## Passo 3: Criar Policies

Cada tabela recebe uma policy que filtra registros pelo tenant da sessao atual. A policy utiliza `FOR ALL` para aplicar em SELECT, INSERT, UPDATE e DELETE.

```sql
-- Units
CREATE POLICY tenant_isolation ON units
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Holders
CREATE POLICY tenant_isolation ON holders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Unit Holders
CREATE POLICY tenant_isolation ON unit_holders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Communities
CREATE POLICY tenant_isolation ON communities
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Documents
CREATE POLICY tenant_isolation ON documents
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Blocks
CREATE POLICY tenant_isolation ON blocks
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Plots
CREATE POLICY tenant_isolation ON plots
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Teams
CREATE POLICY tenant_isolation ON teams
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Team Members
CREATE POLICY tenant_isolation ON team_members
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Community Authorizations
CREATE POLICY tenant_isolation ON community_authorizations
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Accounts
CREATE POLICY tenant_isolation ON accounts
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Sessions
CREATE POLICY tenant_isolation ON sessions
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- API Keys
CREATE POLICY tenant_isolation ON api_keys
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Legitimation Requests
CREATE POLICY tenant_isolation ON legitimation_requests
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

-- Audit Logs (policy especial: INSERT sem restricao USING, SELECT filtrado)
CREATE POLICY tenant_isolation_read ON audit_logs
    FOR SELECT
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY tenant_isolation_write ON audit_logs
    FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);
```

A tabela `audit_logs` possui policies separadas para leitura e escrita. A policy de INSERT usa apenas `WITH CHECK` (sem `USING`) para permitir insercoes sem necessidade de ler registros existentes. As policies de UPDATE e DELETE nao sao criadas para `audit_logs`, tornando-a efetivamente append-only.

## Passo 4: Forcar RLS para Table Owner

Por padrao, o owner da tabela pode bypassar RLS. Para prevenir isso:

```sql
ALTER TABLE units FORCE ROW LEVEL SECURITY;
ALTER TABLE holders FORCE ROW LEVEL SECURITY;
ALTER TABLE unit_holders FORCE ROW LEVEL SECURITY;
ALTER TABLE communities FORCE ROW LEVEL SECURITY;
ALTER TABLE documents FORCE ROW LEVEL SECURITY;
ALTER TABLE blocks FORCE ROW LEVEL SECURITY;
ALTER TABLE plots FORCE ROW LEVEL SECURITY;
ALTER TABLE teams FORCE ROW LEVEL SECURITY;
ALTER TABLE team_members FORCE ROW LEVEL SECURITY;
ALTER TABLE community_authorizations FORCE ROW LEVEL SECURITY;
ALTER TABLE accounts FORCE ROW LEVEL SECURITY;
ALTER TABLE sessions FORCE ROW LEVEL SECURITY;
ALTER TABLE api_keys FORCE ROW LEVEL SECURITY;
ALTER TABLE legitimation_requests FORCE ROW LEVEL SECURITY;
ALTER TABLE audit_logs FORCE ROW LEVEL SECURITY;
```

Com `FORCE ROW LEVEL SECURITY`, mesmo o role que criou a tabela e filtrado pelas policies.

## TenantMiddleware

O middleware da aplicacao e responsavel por definir a variavel de sessao `app.current_tenant` no PostgreSQL antes de cada query.

### Fluxo do Middleware

1. Request chega no pipeline ASP.NET Core
2. TenantMiddleware extrai claim `tenant_id` do JWT Bearer token
3. Valida que `tenant_id` e um UUID valido
4. Abre conexao com PostgreSQL (ou reutiliza do pool)
5. Executa `SET LOCAL app.current_tenant = '{tenant_id}'` na conexao
6. `SET LOCAL` garante que a variavel tem escopo de transacao (nao vaza para outras requests)
7. Request segue para o controller/handler
8. Ao final da transacao, a variavel e automaticamente descartada

### Codigo Conceitual do Middleware

```
class TenantMiddleware:
    function invoke(context, next):
        tenantId = context.User.FindFirst("tenant_id")?.Value

        if tenantId is null:
            return 401 Unauthorized ("Missing tenant_id claim")

        if not IsValidUuid(tenantId):
            return 400 Bad Request ("Invalid tenant_id format")

        // Definir tenant na conexao do banco
        dbConnection.Execute("SET LOCAL app.current_tenant = @tenantId", tenantId)

        await next(context)
```

### Super Admin: Acesso Cross-Tenant

O SUPER_ADMIN precisa acessar dados de todos os tenants. Duas abordagens sao usadas:

1. **Endpoints administrativos**: nao passam pelo TenantMiddleware. Usam conexao sem `SET LOCAL`, mas com role de aplicacao (RLS ainda ativo, porem sem variavel definida = retorna 0 registros)
2. **Bypass explicito**: para endpoints que precisam de acesso cross-tenant, o middleware define `SET LOCAL app.current_tenant = '00000000-0000-0000-0000-000000000000'` e uma policy adicional permite esse UUID especial:

```sql
-- Policy adicional para super admin (UUID zero)
CREATE POLICY super_admin_access ON units
    FOR ALL
    USING (
        tenant_id = current_setting('app.current_tenant')::uuid
        OR current_setting('app.current_tenant') = '00000000-0000-0000-0000-000000000000'
    );
```

Na pratica, endpoints administrativos cross-tenant utilizam uma conexao separada com role `geoapi_admin` que possui `BYPASSRLS`:

```sql
CREATE ROLE geoapi_admin LOGIN PASSWORD 'yyy' BYPASSRLS;
GRANT USAGE ON SCHEMA public TO geoapi_admin;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO geoapi_admin;
```

Esse role tem apenas permissao de SELECT para minimizar risco de escrita acidental em dados de outro tenant.

## Testando RLS Manualmente

### Teste Basico de Isolamento

```sql
-- Conectar como geoapi_app
\c geoapi geoapi_app

-- Definir tenant A
SET app.current_tenant = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

-- Inserir registro no tenant A
INSERT INTO units (id, tenant_id, code, status)
VALUES ('unit-001', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'UNI-001', 'DRAFT');

-- Query retorna 1 registro
SELECT count(*) FROM units;  -- Resultado: 1

-- Mudar para tenant B
SET app.current_tenant = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';

-- Query retorna 0 registros (tenant B nao tem dados)
SELECT count(*) FROM units;  -- Resultado: 0

-- Tentar inserir com tenant_id diferente da sessao
INSERT INTO units (id, tenant_id, code, status)
VALUES ('unit-002', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'UNI-002', 'DRAFT');
-- ERRO: new row violates row-level security policy for table "units"
```

### Teste de Contexto Ausente

```sql
-- Limpar contexto de tenant
RESET app.current_tenant;

-- Tentar query sem contexto
SELECT count(*) FROM units;
-- ERRO: unrecognized configuration parameter "app.current_tenant"
-- OU: retorna 0 registros (depende da configuracao do PostgreSQL)
```

Para evitar erro quando a variavel nao esta definida, registrar valor padrao no postgresql.conf:

```sql
-- No postgresql.conf ou via ALTER SYSTEM
ALTER SYSTEM SET app.current_tenant = '00000000-0000-0000-0000-000000000000';
SELECT pg_reload_conf();
```

Com valor padrao UUID zero e sem policy de super admin, queries sem contexto retornam 0 registros (seguro por padrao).

### Teste de Superuser Bypass

```sql
-- Conectar como postgres (superuser)
\c geoapi postgres

-- Superuser IGNORA RLS mesmo com SET LOCAL
SET app.current_tenant = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
SELECT count(*) FROM units;  -- Retorna TODOS os registros de TODOS os tenants!

-- Por isso NUNCA usar superuser na aplicacao
```

## Troubleshooting

| Problema | Causa | Solucao |
|----------|-------|---------|
| Query retorna dados de outro tenant | Aplicacao conectada como superuser (postgres) | Verificar connection string: deve usar role `geoapi_app` |
| Query retorna 0 registros quando deveria retornar dados | Variavel `app.current_tenant` nao definida ou UUID errado | Verificar TenantMiddleware: log do SET LOCAL e confirmar UUID correto |
| INSERT falha com "violates row-level security policy" | `tenant_id` do INSERT nao corresponde ao `app.current_tenant` da sessao | Garantir que a aplicacao define `tenant_id` a partir do JWT, nao de input do usuario |
| Erro "unrecognized configuration parameter" | Variavel `app.current_tenant` sem valor padrao no postgresql.conf | Adicionar `app.current_tenant = '00000000-0000-0000-0000-000000000000'` ao postgresql.conf |
| Performance degradada apos habilitar RLS | Policy RLS forca Seq Scan ao inves de Index Scan | Criar indice em `tenant_id` em todas as tabelas com RLS: `CREATE INDEX idx_units_tenant ON units(tenant_id)` |
| Super admin nao consegue ver dados de outros tenants | Usando role `geoapi_app` que e filtrado por RLS | Usar role `geoapi_admin` com BYPASSRLS para endpoints administrativos cross-tenant |
| Dados inconsistentes apos migracao | Migracao executada sem contexto de tenant | Executar migracoes com role superuser (postgres) ou com BYPASSRLS, nunca como geoapi_app |
| Connection pool retorna dados de outro tenant | SET sem LOCAL: variavel persiste na conexao retornada ao pool | SEMPRE usar `SET LOCAL` (escopo de transacao). Verificar que nao ha `SET` sem LOCAL no codigo |
| Testes de integracao falham com RLS | Testes nao definem contexto de tenant | Configurar test fixture para executar `SET LOCAL app.current_tenant` antes de cada teste |

## Performance

### Indices Recomendados

Toda tabela com RLS deve ter indice em `tenant_id` para que o filtro da policy use Index Scan:

```sql
CREATE INDEX idx_units_tenant ON units(tenant_id);
CREATE INDEX idx_holders_tenant ON holders(tenant_id);
CREATE INDEX idx_unit_holders_tenant ON unit_holders(tenant_id);
CREATE INDEX idx_communities_tenant ON communities(tenant_id);
CREATE INDEX idx_documents_tenant ON documents(tenant_id);
CREATE INDEX idx_blocks_tenant ON blocks(tenant_id);
CREATE INDEX idx_plots_tenant ON plots(tenant_id);
CREATE INDEX idx_teams_tenant ON teams(tenant_id);
CREATE INDEX idx_team_members_tenant ON team_members(tenant_id);
CREATE INDEX idx_community_authorizations_tenant ON community_authorizations(tenant_id);
CREATE INDEX idx_accounts_tenant ON accounts(tenant_id);
CREATE INDEX idx_sessions_tenant ON sessions(tenant_id);
CREATE INDEX idx_api_keys_tenant ON api_keys(tenant_id);
CREATE INDEX idx_legitimation_requests_tenant ON legitimation_requests(tenant_id);
CREATE INDEX idx_audit_logs_tenant ON audit_logs(tenant_id);
```

### Indices Compostos

Para queries frequentes que combinam tenant com outros filtros:

```sql
-- Unidades por tenant e status (dashboard, listagens filtradas)
CREATE INDEX idx_units_tenant_status ON units(tenant_id, status);

-- Holders por tenant e CPF (busca por CPF)
CREATE INDEX idx_holders_tenant_cpf ON holders(tenant_id, cpf);

-- Documents por tenant e entity (documentos de uma unidade)
CREATE INDEX idx_documents_tenant_entity ON documents(tenant_id, entity_id, entity_type);

-- Audit logs por tenant e periodo (consultas de auditoria)
CREATE INDEX idx_audit_logs_tenant_timestamp ON audit_logs(tenant_id, timestamp DESC);
```

### Verificacao de Plano de Execucao

Apos configurar RLS, verificar que queries usam indices:

```sql
SET app.current_tenant = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
EXPLAIN ANALYZE SELECT * FROM units WHERE status = 'DRAFT';
-- Deve mostrar "Index Scan using idx_units_tenant_status"
-- Se mostrar "Seq Scan" + "Filter", o indice nao esta sendo utilizado
```