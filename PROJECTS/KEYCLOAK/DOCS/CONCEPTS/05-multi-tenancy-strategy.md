---
type: leaf
status: approved
updated: 2026-02-07
---

# Estrategia de Multi-Tenancy

Multi-tenancy no ecossistema CARF e implementado via user attributes no Keycloak mapeados para claims JWT, combinado com Row-Level Security (RLS) no PostgreSQL para isolamento de dados. Cada tenant representa um municipio que utiliza o sistema de regularizacao fundiaria.

## User Attributes

Cada usuario possui dois atributos principais de tenancy. O atributo tenants e um array multi-valued contendo identificadores dos municipios acessiveis, por exemplo ["prefeitura-a", "prefeitura-b"]. O atributo current_tenant e single-valued indicando o tenant ativo no momento, por exemplo "prefeitura-a". Adicionalmente, community_ids lista UUIDs de comunidades acessiveis dentro do tenant corrente.

Esses atributos sao configurados no Admin Console via Users, Attributes ou em lote via Admin API POST /admin/realms/carf/users. Validacao garante que current_tenant esteja sempre presente no array tenants, impedindo referencias orfas.

## Protocol Mappers

Tres protocol mappers no scope carf-tenant transformam atributos em claims JWT. O mapper tenant_id extrai current_tenant para claim tenant_id tipo String. O mapper allowed_tenants extrai tenants para claim allowed_tenants tipo JSON multivalued. O mapper community_ids extrai community_ids para claim community_ids tipo JSON multivalued. Todos emitem claims em access token, ID token e userinfo endpoint.

O resultado e que todo access token emitido contem claims como tenant_id com valor do tenant ativo e allowed_tenants com array dos tenants permitidos, acessiveis por qualquer aplicacao que decodifique o JWT.

## Isolamento de Dados via RLS

O backend GEOAPI implementa isolamento via Row-Level Security do PostgreSQL. O middleware TenantMiddleware executa apos autenticacao, extrai claim tenant_id do JWT via User.FindFirst("tenant_id") e configura variavel de sessao PostgreSQL via SET LOCAL app.tenant_id antes de qualquer query. RLS policies em cada tabela garantem que SELECT retorna apenas rows do tenant ativo, INSERT/UPDATE/DELETE afetam apenas rows do tenant ativo, e tentativas de acessar dados de outros tenants resultam em rows vazias sem necessidade de WHERE tenant_id explicito em cada query.

A abordagem RLS foi escolhida por balancear isolamento forte (tenant A nunca ve dados de tenant B mesmo com SQL injection ou bug) com simplicidade operacional (single database, unified migrations, backups atomicos). Alternativas como schema-per-tenant ou database-per-tenant foram rejeitadas por complicar migrations, backups e cross-tenant reporting.

## Troca de Tenant

Quando um usuario com acesso a multiplos municipios deseja trocar de tenant, o frontend exibe dropdown com valores de allowed_tenants. Ao selecionar novo tenant, o frontend chama POST /api/auth/switch-tenant com o novo tenantId. O backend valida que o tenant solicitado esta presente em allowed_tenants do JWT, atualiza o user attribute current_tenant via Keycloak Admin API e retorna sucesso. O frontend forca refresh do token via keycloak.updateToken(-1) obtendo novo access token com tenant_id atualizado. Todas requisicoes subsequentes usam o novo tenant automaticamente via RLS.

## Propagacao entre Servicos

O tenant_id e propagado para todos os servicos via JWT sem necessidade de shared state ou session store. Cada servico independentemente valida o JWT e extrai tenant_id, garantindo isolamento consistente em toda a arquitetura.

## Onboarding e Offboarding

Tenant onboarding e executado via ADMIN chamando Keycloak Admin API para criar usuarios ou adicionar novo tenant ao array tenants de usuarios existentes. Tenant offboarding remove o tenant do array via PATCH mas nao deleta dados fisicos, pois DELETE CASCADE requer procedimento formal com auditoria para compliance LGPD e possivel retencao temporaria.

## Auditoria

Toda troca de tenant e registrada em tabela audit_log com user_id, old_tenant, new_tenant, timestamp e IP address para compliance e rastreabilidade. Tenant-aware logging captura tenant_id em structured logs (Serilog) permitindo filtrar eventos por municipio.
