# Rotacionar Secrets

## Client Secrets (sem downtime)

### 1. Gerar novo secret

Obter admin token executando curl POST para realms/master/protocol/openid-connect/token com client_id admin-cli username admin password admin grant_type password extraindo access_token via jq armazenando em TOKEN, regenerar secret executando curl POST para admin/realms/carf/clients/geoapi-client-id/client-secret com Authorization header Bearer TOKEN extraindo value via jq armazenando em NEW_SECRET exibindo novo secret gerado.

### 2. Atualizar aplicações

Atualizar arquivo .env das aplicações executando echo KEYCLOAK_CLIENT_SECRET igual NEW_SECRET redirecionando append para GEOAPI/.env seguido por restart aplicação executando docker-compose restart geoapi aplicando novo secret sem downtime mantendo sessões ativas usuários conectados transition suave rotação credenciais segurança mantida.

## Admin Password

### 1. Via Admin Console
1. Acesse Admin Console
2. Users → admin → Credentials
3. Reset password

### 2. Via CLI (container parado)

Parar containers executando docker-compose menos f docker-compose.dev.yml down seguido por executar temporário container Keycloak com docker-compose menos f docker-compose.dev.yml run menos menos rm passando environment variable menos e KEYCLOAK_ADMIN_PASSWORD igual nova_senha_forte executando comando keycloak start-dev menos menos import-realm resetando admin password e finalmente subir containers novamente executando docker-compose menos f docker-compose.dev.yml up menos d aplicando nova senha admin requerendo downtime breve.

## PostgreSQL Password

### Zero downtime

Rotação sem downtime iniciando criando novo user executando CREATE USER keycloak_new WITH PASSWORD nova_senha_forte seguido por GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_new, atualizando variáveis environment .env configurando KC_DB_USERNAME igual keycloak_new KC_DB_PASSWORD igual nova_senha_forte, restart Keycloak executando docker-compose restart keycloak para aplicar novas credenciais conexão database, e finalmente removendo old user executando DROP USER keycloak limpando credenciais antigas mantendo sistema funcionando durante todo processo sem interrupção serviço.

## Quando Rotacionar

Client secrets rotacionados a cada noventa dias, Admin password rotacionado a cada noventa dias, PostgreSQL password rotacionado a cada cento e oitenta dias, e após suspeita de vazamento rotacionar imediatamente garantindo segurança credenciais compliance políticas organizacionais prevenção exploração credenciais comprometidas.

## Automação

Automatizar rotação configurando cron job mensal executando zero zero um asterisco asterisco /path/to/carf-keycloak/scripts/rotate-secrets.sh garantindo rotações periódicas automáticas sem intervenção manual reduzindo risco esquecimento humano mantendo disciplina segurança consistente.
