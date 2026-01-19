# Access Token

Access token é JWT assinado com RS256 usando chave privada do realm CARF. Tempo de vida padrão de 5 minutos configurado em Realm Settings > Tokens > Access Token Lifespan. Valor curto minimiza janela de exposição caso token seja interceptado.

Payload inclui claims padrão do OIDC: sub (UUID do usuário), iss (URL do realm), aud (client_id), exp (timestamp expiração), iat (timestamp emissão). Claims customizados adicionados via protocol mappers: tenant_id (tenant ativo), allowed_tenants (array de tenants permitidos), realm_access.roles (array de roles).

Estrutura típica do payload para usuário analyst do tenant prefeitura-sjc contém sub com UUID do usuário, iss apontando para URL do realm como auth.carf.example.com/realms/carf, aud com client_id carf-geoweb, timestamps exp e iat, preferred_username e email do usuário, tenant_id com valor prefeitura-sjc, allowed_tenants como array com os tenants permitidos, e realm_access.roles listando analyst e field-collector.

Frontend armazena access token em memória (variável JavaScript) nunca em localStorage ou sessionStorage. Axios interceptor adiciona header Authorization: Bearer {token} em cada requisição para GEOAPI.

---

**Status:** Review
**Atualizado:** 2026-01-19
**Descrição:** 
