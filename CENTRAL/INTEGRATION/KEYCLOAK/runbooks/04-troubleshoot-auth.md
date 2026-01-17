# Troubleshoot Autenticação

## Usuário não consegue logar

### Verificar se usuário existe

Obter admin token executando curl POST para realms/master/protocol/openid-connect/token com client_id admin-cli username admin password admin grant_type password extraindo access_token via jq armazenando em TOKEN seguido por verificar usuário executando curl GET para admin/realms/carf/users com query parameter username joao.silva usando Authorization header Bearer TOKEN formatando output com jq exibindo dados usuário se existir ou array vazio se não encontrado.

### Verificar se está habilitado

Verificar se usuário está habilitado executando curl GET para admin/realms/carf/users/USER_ID com Authorization header Bearer TOKEN extraindo propriedade enabled via jq devendo retornar true para permitir login false indicando usuário desabilitado impedindo autenticação mesmo com credenciais corretas.

### Resetar senha

Resetar senha do usuário executando curl PUT para admin/realms/carf/users/USER_ID/reset-password com Authorization header Bearer TOKEN Content-Type application/json enviando payload JSON contendo type password value nova_senha temporary false aplicando nova senha imediatamente sem requerer troca primeiro login permitindo usuário autenticar novamente resolvendo problemas senha esquecida ou bloqueio.

## Token expirado

### Configuração de timeout

Ver configuração atual de token lifespan executando curl GET para admin/realms/carf com Authorization header Bearer TOKEN extraindo accessTokenLifespan via jq exibindo duração em segundos, atualizar timeout executando curl PUT para admin/realms/carf enviando payload JSON accessTokenLifespan igual três mil e seiscentos configurando tokens válidos por uma hora aumentando tempo sessão reduzindo frequência refresh melhorando UX mas balanceando segurança sessões longas demais aumentam risco tokens comprometidos.

### Refresh token

Frontend implementa auto refresh usando React useEffect criando interval executando setInterval callback invocando keycloak.updateToken com parâmetro trinta refreshing token se expirar em menos de trinta segundos executando a cada dez mil milissegundos dez segundos cleanup retornando clearInterval ao desmontar component garantindo sessões persistentes sem interrupção usuário trabalhando aplicação sem reauthenticação manual UX seamless tokens sempre válidos.

## CORS errors

### Configurar Web Origins no client

Resolver CORS errors configurando Web Origins executando curl PUT para admin/realms/carf/clients/CLIENT_ID com Authorization header Bearer TOKEN Content-Type application/json enviando payload JSON webOrigins array contendo http://localhost:3000 e https://app.carf.gov.br permitindo browsers aceitar responses Keycloak de origens especificadas eliminando bloqueios CORS preflight requests OPTIONS bem-sucedidos authentication flows funcionando corretamente.

## Redirect URI mismatch

### Adicionar redirect URIs válidas

Resolver redirect URI mismatch executando curl PUT para admin/realms/carf/clients/CLIENT_ID enviando payload JSON redirectUris array contendo http://localhost:3000/asterisco https://app.carf.gov.br/asterisco e carf://callback cobrindo web development web production e mobile deep linking permitindo OAuth authorization code flow redirect callbacks validados Keycloak aceitando autenticação múltiplos ambientes plataformas sem errors invalid redirect uri bloqueando login.

## Client secret inválido

### Verificar secret atual

Verificar client secret atual executando curl GET para admin/realms/carf/clients/CLIENT_ID/client-secret com Authorization header Bearer TOKEN extraindo value via jq menos r exibindo secret plaintext comparável com configuração application.

### Comparar com .env

Comparar secret Keycloak com environment variable executando grep KEYCLOAK_CLIENT_SECRET .env exibindo valor configurado aplicação identificando discrepâncias secret rotacionado Keycloak mas não atualizado .env causando authentication failures client confidential não conseguindo obter tokens.

## Tenant errado no JWT

### Verificar attributes do usuário

Verificar attributes do usuário executando curl GET para admin/realms/carf/users/USER_ID com Authorization header Bearer TOKEN extraindo attributes via jq devendo ter tenants array com lista tenants acessíveis e current_tenant array com único tenant ativo atual, ausência desses attributes significa multi-tenancy não configurado corretamente claims tenant_id não aparecerão JWT causando RLS failures backend queries não filtradas por tenant.

### Verificar protocol mapper

Verificar protocol mapper tenant_id configurado executando curl GET para admin/realms/carf/client-scopes/profile/protocol-mappers/models com Authorization header Bearer TOKEN filtrando via jq selecionando mapper name igual tenant_id confirmando mapper existe configurado corretamente transformando user attribute current_tenant em JWT claim tenant_id disponível backend extraction RLS filtering, ausência mapper significa claims não adicionados tokens mesmo attributes usuário corretos.

## Logs do Keycloak

Visualizar logs Keycloak em tempo real executando docker-compose menos f docker-compose.dev.yml logs menos f keycloak seguindo output contínuo identificando errors warnings eventos autenticação, filtrar erros de autenticação executando docker-compose logs keycloak pipe grep menos i login barra vertical error barra vertical failed exibindo apenas linhas relevantes troubleshooting login failures, aumentar log level para debug executando KC_LOG_LEVEL igual debug docker-compose up menos d habilitando verbose logging detalhado OAuth flows SAML requests database queries facilitando debugging profundo problemas complexos autenticação multi-tenancy RLS.
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
