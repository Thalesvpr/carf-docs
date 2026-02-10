---
type: leaf
status: review
updated: 2026-02-08
---

# Authorization

O sistema de autorizacao da GEOAPI implementa RBAC hierarquico com 6 realm roles do Keycloak, isolamento por tenant via RLS e controle de acesso granular por comunidade.

## Hierarquia de Roles

As 6 roles sao organizadas em hierarquia de arvore (nao linear) via composite roles do Keycloak. Super-admin inclui admin, que inclui manager. Manager bifurca em dois ramos: analyst (ramo escritorio) e field-coordinator (ramo campo). Field-coordinator inclui field-cadastrator como role base. Analyst nao herda de field-coordinator pois sao contextos distintos (escritorio versus campo). Ao atribuir role manager a um usuario, ele automaticamente ganha analyst, field-coordinator e field-cadastrator. Ao atribuir admin, ganha tambem manager e todos abaixo.

## Permissoes por Role

O field-cadastrator pode criar e editar unidades proprias, capturar fotos e sincronizar dados via app mobile. O field-coordinator supervisiona equipe de campo com acesso a metricas de produtividade e menu mobile completo. O analyst pode validar unidades, criar processos de legitimacao e gerar relatorios. O manager pode aprovar e rejeitar unidades e processos de legitimacao. O admin pode gerenciar usuarios e roles do proprio tenant via endpoints /api/admin. O super-admin pode criar tenants, transferir usuarios entre tenants e acessar todos os tenants.

## Tres Niveis de Validacao

O primeiro nivel usa atributo Authorize nos controllers, bloqueando acesso de usuarios nao autenticados com 401 Unauthorized. O segundo nivel usa Authorize com Roles especificando roles permitidas, retornando 403 Forbidden para roles insuficientes. O terceiro nivel e validacao programatica dentro dos handlers usando HasAnyRole para logica condicional, como admin que so ve usuarios do proprio tenant enquanto super-admin ve todos.

## Isolamento por Tenant

Em paralelo as roles, o tenant_id do JWT e extraido pelo TenantMiddleware e definido como variavel de sessao no PostgreSQL. Policies RLS filtram automaticamente todas as queries, garantindo que mesmo um admin so acessa dados do proprio tenant.

## Acesso por Comunidade

Alem de roles e tenant, equipes de campo tem acesso restrito a comunidades especificas via tabela community_authorizations. O nivel de permissao (READ, WRITE, ADMIN) determina o que a equipe pode fazer em cada comunidade.

## Permission Matrix

A tabela abaixo detalha as permissoes de cada role para cada endpoint da API. Os valores indicam o escopo de acesso: "Proprias" (registros criados pelo usuario), "Equipe" (registros de membros da equipe), "Todas tenant" (todos os registros do tenant), "Todas" (todos os registros de todos os tenants), "Tenant" (operacao restrita ao proprio tenant), "Autorizadas" (comunidades com autorizacao explicita via community_authorizations).

| Endpoint | Metodo | FIELD_CADASTRATOR | FIELD_COORDINATOR | ANALYST | MANAGER | ADMIN | SUPER_ADMIN |
|----------|--------|-------------------|-------------------|---------|---------|-------|-------------|
| /api/units | GET | Proprias | Equipe | Todas tenant | Todas tenant | Todas tenant | Todas |
| /api/units | POST | Sim | Sim | Sim | Sim | Sim | Sim |
| /api/units/{id} | PUT | Proprias (Draft) | Equipe (Draft) | Todas (Draft) | Todas (Draft/Pending) | Todas | Todas |
| /api/units/{id}/submit | POST | Proprias | Equipe | Todas | Todas | Todas | Todas |
| /api/units/{id}/approve | POST | Nao | Nao | Nao | Sim | Sim | Sim |
| /api/units/{id}/reject | POST | Nao | Nao | Nao | Sim | Sim | Sim |
| /api/holders | GET | Proprias | Equipe | Todas tenant | Todas tenant | Todas tenant | Todas |
| /api/holders | POST | Sim | Sim | Sim | Sim | Sim | Sim |
| /api/communities | GET | Autorizadas | Autorizadas | Todas tenant | Todas tenant | Todas tenant | Todas |
| /api/communities | POST | Nao | Nao | Nao | Nao | Sim | Sim |
| /api/admin/users | GET | Nao | Nao | Nao | Nao | Tenant | Todos |
| /api/admin/users | POST | Nao | Nao | Nao | Nao | Tenant | Todos |
| /api/sync/push | POST | Sim | Sim | Nao | Nao | Nao | Nao |
| /api/sync/changes | GET | Sim | Sim | Nao | Nao | Nao | Nao |
| /api/legitimation | POST | Nao | Nao | Sim | Sim | Sim | Sim |
| /api/legitimation/{id}/approve | POST | Nao | Nao | Nao | Sim | Sim | Sim |
| /api/reports | POST | Nao | Nao | Sim | Sim | Sim | Sim |

Os endpoints de sync (/api/sync/*) sao exclusivos para roles de campo (FIELD_CADASTRATOR e FIELD_COORDINATOR) pois apenas o app mobile REURBCAD utiliza o protocolo offline-first. Roles de analise, gestao e administracao acessam a GEOAPI diretamente via GEOWEB ou ADMIN, que operam sempre online.

A restricao "Proprias (Draft)" significa que o usuario so pode editar registros criados por ele e apenas enquanto estiverem no status DRAFT. A restricao "Equipe (Draft)" estende isso para registros de qualquer membro da equipe coordenada.

## RLS Policy SQL

O isolamento por tenant e implementado via Row Level Security (RLS) do PostgreSQL, garantindo que mesmo queries sem filtro WHERE retornem apenas dados do tenant correto.

```sql
-- Habilitar RLS nas tabelas com escopo de tenant
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE holders ENABLE ROW LEVEL SECURITY;
ALTER TABLE communities ENABLE ROW LEVEL SECURITY;

-- Policy: filtrar pelo tenant da sessao atual
CREATE POLICY tenant_isolation ON units
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY tenant_isolation ON holders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

CREATE POLICY tenant_isolation ON communities
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);
```

A clausula `USING` filtra registros em operacoes SELECT, UPDATE e DELETE. A clausula `WITH CHECK` valida que INSERTs e UPDATEs sempre incluam o tenant_id correto. A variavel `app.current_tenant` e definida pelo TenantMiddleware no inicio de cada request via `SET LOCAL`, garantindo escopo de transacao. Para detalhes completos da configuracao RLS, ver `ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/03-rls-setup.md`.

## CORS Configuration

A configuracao CORS varia por ambiente para balancear seguranca e praticidade no desenvolvimento.

| Ambiente | AllowedOrigins | AllowCredentials | AllowedHeaders | AllowedMethods |
|----------|---------------|-----------------|----------------|----------------|
| Development | http://localhost:3000, http://localhost:5173, http://localhost:4321 | true | Authorization, Content-Type, X-Tenant-Id, X-Request-Id | GET, POST, PUT, DELETE, PATCH, OPTIONS |
| Staging | https://staging.geoweb.carf.dev, https://staging.admin.carf.dev, https://staging.webdocs.carf.dev | true | Authorization, Content-Type, X-Tenant-Id, X-Request-Id | GET, POST, PUT, DELETE, PATCH, OPTIONS |
| Production | https://geoweb.carf.gov.br, https://admin.carf.gov.br, https://webdocs.carf.gov.br | true | Authorization, Content-Type, X-Tenant-Id, X-Request-Id | GET, POST, PUT, DELETE, PATCH, OPTIONS |

O app mobile REURBCAD nao precisa de CORS pois faz requests nativos via HTTP client, sem restricoces de same-origin policy do navegador. O AllowCredentials e habilitado em todos os ambientes para suportar envio do cookie de sessao do Keycloak durante o fluxo Authorization Code com PKCE. O header X-Tenant-Id e enviado explicitamente pelo GEOWEB e ADMIN para indicar o tenant selecionado. O header X-Request-Id e um correlation ID para rastreamento de requests distribuidos.
