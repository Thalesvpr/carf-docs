---
type: leaf
status: review
updated: 2026-01-19
---

# Access Token

Access token é JWT assinado com RS256 usando chave privada do realm CARF. Tempo de vida padrão de 5 minutos configurado em Realm Settings > Tokens > Access Token Lifespan. Valor curto minimiza janela de exposição caso token seja interceptado.

Payload inclui claims padrão do OIDC: sub (UUID do usuário), iss (URL do realm), aud (client_id), exp (timestamp expiração), iat (timestamp emissão). Claims customizados adicionados via protocol mappers do scope carf-tenant: tenant_id (tenant ativo, String), allowed_tenants (array de tenants permitidos, JSON multivalued), community_ids (array de comunidades, JSON multivalued). Claim realm_access.roles contém array de roles do realm.

Estrutura típica do payload para usuário analyst do tenant prefeitura-sjc contém sub com UUID do usuário, iss apontando para URL do realm como auth.carf.example.com/realms/carf, aud com client_id geoweb, timestamps exp e iat, preferred_username e email do usuário, tenant_id com valor prefeitura-sjc, allowed_tenants como array com os tenants permitidos, community_ids como array de UUIDs de comunidades, e realm_access.roles listando apenas analyst (analyst NÃO é composite — não herda field-coordinator nem field-cadastrator, pois são ramos separados da hierarquia).

Frontend armazena access token em memória (variável JavaScript) nunca em localStorage ou sessionStorage. Axios interceptor adiciona header Authorization: Bearer {token} em cada requisição para GEOAPI.
