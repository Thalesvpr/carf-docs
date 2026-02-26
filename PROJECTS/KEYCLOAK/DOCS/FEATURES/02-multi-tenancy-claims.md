---
type: leaf
status: approved
updated: 2026-02-07
---

# Multi-Tenancy Claims

Multi-tenancy no Keycloak CARF e implementado via user attributes mapeados para claims JWT por protocol mappers do scope carf-tenant. Essa abordagem permite que todas as aplicacoes identifiquem o tenant ativo e os tenants permitidos do usuario diretamente a partir do access token, sem consultas adicionais ao Keycloak.

## User Attributes

Cada usuario possui atributos customizados configurados via Admin Console em Users, Attributes ou em lote via Admin API. O atributo tenants e multi-valued contendo array de identificadores dos tenants acessiveis ao usuario, por exemplo ["tenant-uuid-1", "tenant-uuid-2"]. O atributo current_tenant e single-valued indicando o tenant ativo na sessao atual. Validacao de consistencia garante que current_tenant esteja sempre presente no array tenants.

Migracao de usuarios existentes sem atributos de tenant pode ser feita via script bulk usando Admin API ou Required Action UPDATE_PROFILE forcando preenchimento no proximo login.

## Protocol Mappers

Tres mappers no client scope carf-tenant transformam atributos em claims JWT. Todos sao do tipo oidc-usermodel-attribute-mapper configurados no Admin Console em Client Scopes, carf-tenant, Mappers.

| Mapper | User Attribute | Token Claim Name | Claim JSON Type | Multivalued |
|:-------|:---------------|:-----------------|:----------------|:------------|
| tenant_id | current_tenant | tenant_id | String | Nao |
| allowed_tenants | tenants | allowed_tenants | String | Sim |
| community_ids | community_ids | community_ids | String | Sim |

Todos emitem claims em access token e userinfo endpoint. O scope carf-tenant integra os defaultClientScopes, sendo aplicado automaticamente a todos os clients.

## Integracao com Backend

O middleware TenantMiddleware no GEOAPI (.NET) executa apos UseAuthentication e extrai claim tenant_id do JWT via User.FindFirst("tenant_id"). Em seguida, configura variavel de sessao PostgreSQL via SET LOCAL app.tenant_id que aciona Row-Level Security policies automaticamente filtrando todas as queries pelo tenant ativo. Nenhum filtro WHERE explicito e necessario no codigo da aplicacao.

## Integracao com Frontend

No REURBWEB (React), o AuthContext e hook useAuth parseiam keycloak.tokenParsed para extrair tenant_id e allowed_tenants. Quando allowed_tenants contem mais de um valor, o componente TenantSwitcher renderiza dropdown permitindo troca de tenant.

## Fluxo de Troca de Tenant

Quando o usuario seleciona novo tenant no dropdown, o frontend chama POST /api/auth/switch-tenant com o novo tenantId. O backend valida que o tenant solicitado esta presente no claim allowed_tenants do JWT atual, atualiza o user attribute current_tenant via Keycloak Admin API e retorna sucesso. O frontend forca refresh do token via keycloak.updateToken(-1) obtendo novo access token com tenant_id atualizado. A aplicacao recarrega limpando cache para garantir que queries usem o novo contexto de tenant.

## Seguranca

O backend sempre valida tenant_id claim contra allowed_tenants, impedindo spoofing via manipulacao client-side. Tokens sao assinados com RS256 usando chave privada do Keycloak, tornando impossivel forjar claims validos sem acesso a chave. Toda troca de tenant e registrada em audit_log com user_id, old_tenant, new_tenant, timestamp e IP address para compliance e rastreabilidade.
