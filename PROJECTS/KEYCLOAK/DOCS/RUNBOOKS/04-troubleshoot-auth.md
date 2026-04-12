---
type: leaf
status: review
updated: 2026-02-08
---

# Troubleshoot Autenticacao

## Usuario Nao Consegue Logar

### Verificar se o Usuario Existe

Obtenha o admin token executando um `curl POST` para `realms/master/protocol/openid-connect/token` com `client_id=admin-cli`, `username=admin`, `password=admin` e `grant_type=password`, extraindo o `access_token` via `jq` e armazenando em `TOKEN`. Em seguida, verifique o usuário com um `curl GET` para `admin/realms/carf/users` com query parameter `username=joao.silva`, usando o header `Authorization: Bearer $TOKEN` e formatando o output com `jq`. O resultado exibirá os dados do usuário se ele existir, ou um array vazio se não for encontrado.

### Verificar se esta Habilitado

Execute um `curl GET` para `admin/realms/carf/users/$USER_ID` com o header `Authorization: Bearer $TOKEN` e extraia a propriedade `enabled` via `jq`. O valor deve ser `true` para permitir o login. Um retorno `false` indica que o usuário está desabilitado, impedindo a autenticação mesmo com credenciais corretas.

### Resetar Senha

Execute um `curl PUT` para `admin/realms/carf/users/$USER_ID/reset-password` com o header `Authorization: Bearer $TOKEN` e `Content-Type: application/json`, enviando o payload JSON com `type: password`, `value: nova_senha` e `temporary: false`. A nova senha é aplicada imediatamente sem requerer troca no primeiro login, permitindo que o usuário autentique novamente e resolvendo problemas de senha esquecida ou bloqueio.

## Token Expirado

### Configuracao de Timeout

Para verificar a configuração atual de token lifespan, execute um `curl GET` para `admin/realms/carf` com o header `Authorization: Bearer $TOKEN` e extraia `accessTokenLifespan` via `jq`, que exibirá a duração em segundos. Para atualizar o timeout, execute um `curl PUT` para `admin/realms/carf` enviando o payload JSON `{ "accessTokenLifespan": 3600 }`, configurando tokens válidos por uma hora. Aumentar o tempo de sessão reduz a frequência de refresh e melhora a experiência do usuário, mas deve ser balanceado com a segurança, pois sessões longas demais aumentam o risco de tokens comprometidos.

### Refresh Token Automatico

O frontend implementa auto-refresh usando um `useEffect` do React que cria um interval com `setInterval`. O callback invoca `keycloak.updateToken(30)`, que faz o refresh do token se ele expirar em menos de trinta segundos. O interval é executado a cada dez mil milissegundos (dez segundos). A função de cleanup retorna `clearInterval` ao desmontar o componente. Esse mecanismo garante sessões persistentes sem interrupção, permitindo ao usuário trabalhar na aplicação sem reautenticação manual, com tokens sempre válidos.

## CORS Errors

### Configurar Web Origins no Client

Para resolver CORS errors, configure as Web Origins do client executando um `curl PUT` para `admin/realms/carf/clients/$CLIENT_ID` com o header `Authorization: Bearer $TOKEN` e `Content-Type: application/json`, enviando o payload JSON com `webOrigins: ["http://localhost:3000", "https://app.carf.gov.br"]`. Isso permite que os browsers aceitem responses do Keycloak vindas das origens especificadas, eliminando bloqueios CORS e garantindo que preflight requests OPTIONS sejam bem-sucedidos e que os authentication flows funcionem corretamente.

## Redirect URI Mismatch

### Adicionar Redirect URIs Validas

Para resolver o erro de redirect URI mismatch, execute um `curl PUT` para `admin/realms/carf/clients/$CLIENT_ID` com payload JSON contendo `redirectUris: ["http://localhost:3000/*", "https://app.carf.gov.br/*", "carf://callback"]`. Esse array cobre os três cenários: web em desenvolvimento, web em produção e mobile via deep linking. Com essas URIs registradas, o Keycloak aceita os redirect callbacks do OAuth authorization code flow em múltiplos ambientes e plataformas, eliminando erros de "invalid redirect uri" que bloqueiam o login.

## Client Secret Invalido

### Verificar Secret Atual

Execute um `curl GET` para `admin/realms/carf/clients/$CLIENT_ID/client-secret` com o header `Authorization: Bearer $TOKEN` e extraia o `value` via `jq -r`. O resultado exibe o secret em plaintext, que pode ser comparado com a configuração da aplicação.

### Comparar com o .env

Execute `grep KEYCLOAK_CLIENT_SECRET .env` para exibir o valor configurado na aplicação. Discrepâncias entre esse valor e o secret no Keycloak indicam que o secret foi rotacionado no Keycloak mas não atualizado no `.env`, causando authentication failures onde o client confidential não consegue obter tokens.

## Tenant Errado no JWT

### Verificar Attributes do Usuario

Execute um `curl GET` para `admin/realms/carf/users/$USER_ID` com o header `Authorization: Bearer $TOKEN` e extraia `attributes` via `jq`. O resultado deve conter `tenants` como um array com a lista de tenants acessíveis e `current_tenant` como array com um único tenant ativo. A ausência desses attributes significa que a multi-tenancy não está configurada corretamente e as claims `tenant_id` não aparecerão no JWT, causando falhas de RLS no backend com queries não filtradas por tenant.

### Verificar Protocol Mapper

Execute um `curl GET` para `admin/realms/carf/client-scopes/carf-tenant/protocol-mappers/models` com o header `Authorization: Bearer $TOKEN` e filtre via `jq` selecionando o mapper com `name == "tenant_id"`. A presença desse mapper confirma que ele está configurado corretamente para transformar o user attribute `current_tenant` na JWT claim `tenant_id`, disponível para extração no backend e filtragem RLS. A ausência do mapper significa que as claims não serão adicionadas aos tokens, mesmo que os attributes do usuário estejam corretos.

## Logs do Keycloak

Para visualizar os logs do Keycloak em tempo real, execute `docker-compose -f docker-compose.dev.yml logs -f keycloak`, que segue o output contínuo mostrando errors, warnings e eventos de autenticação. Para filtrar apenas erros de autenticação, execute `docker-compose logs keycloak | grep -i "login\|error\|failed"`, exibindo apenas linhas relevantes para troubleshooting de login failures. Para debugging profundo de problemas complexos de autenticação, multi-tenancy ou RLS, aumente o log level para debug executando `KC_LOG_LEVEL=debug docker-compose up -d`, habilitando verbose logging detalhado de OAuth flows, SAML requests e database queries.
