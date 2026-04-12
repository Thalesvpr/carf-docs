---
type: leaf
status: review
description: "Procedimento para rotacao de secrets de clients, admin password e PostgreSQL"
updated: 2026-02-08
---

# Rotacionar Secrets

## Client Secrets (sem downtime)

### Gerar Novo Secret

Para regenerar o secret de um client, primeiro obtenha o admin token executando um `curl POST` para `realms/master/protocol/openid-connect/token` com `client_id=admin-cli`, `username=admin`, `password=admin` e `grant_type=password`, extraindo o `access_token` via `jq` e armazenando em `TOKEN`. Em seguida, regenere o secret executando um `curl POST` para `admin/realms/carf/clients/geogis-client-id/client-secret` com o header `Authorization: Bearer $TOKEN`, extraindo o `value` via `jq` e armazenando em `NEW_SECRET`.

### Atualizar Aplicacoes

Atualize o arquivo `.env` da aplicação com o novo secret executando `echo "KEYCLOAK_CLIENT_SECRET=$NEW_SECRET" >> GEOGIS/.env` e reinicie a aplicação para aplicar o novo secret. O processo ocorre sem downtime, mantendo as sessões ativas dos usuários conectados e garantindo uma transição suave na rotação de credenciais.

## Admin Password

### Via Admin Console

O caminho mais simples é pela interface gráfica. Acesse o Admin Console, navegue até Users, selecione o usuário `admin`, abra a aba Credentials e execute o reset de password.

### Via CLI (Container Parado)

Para redefinir via linha de comando, pare os containers executando `docker-compose -f docker-compose.dev.yml down`. Em seguida, execute um container temporário do Keycloak com `docker-compose -f docker-compose.dev.yml run --rm -e KEYCLOAK_ADMIN_PASSWORD=nova_senha_forte keycloak start-dev --import-realm`, que reseta a senha admin. Finalmente, suba os containers novamente com `docker-compose -f docker-compose.dev.yml up -d`. Este processo requer um breve downtime.

## PostgreSQL Password

### Rotacao sem Downtime

A rotação sem downtime segue quatro passos em sequência. Primeiro, crie um novo usuário no PostgreSQL com `CREATE USER keycloak_new WITH PASSWORD 'nova_senha_forte'` seguido por `GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_new`. Em seguida, atualize as variáveis de environment no `.env` configurando `KC_DB_USERNAME=keycloak_new` e `KC_DB_PASSWORD=nova_senha_forte`. Depois, reinicie o Keycloak com `docker-compose restart keycloak` para aplicar as novas credenciais de conexão ao database. Por fim, remova o usuário antigo com `DROP USER keycloak`, limpando as credenciais anteriores enquanto o sistema permanece funcionando durante todo o processo.

## Frequencia de Rotacao

A tabela a seguir resume a política de rotação periódica para cada tipo de credencial.

| Credencial | Frequência | Observação |
|---|---|---|
| Client secrets | A cada 90 dias | Rotação padrão |
| Admin password | A cada 90 dias | Rotação padrão |
| PostgreSQL password | A cada 180 dias | Rotação estendida |
| Qualquer credencial sob suspeita de vazamento | Imediatamente | Prioridade máxima |

A rotação tempestiva garante a segurança das credenciais, o compliance com políticas organizacionais e a prevenção de exploração de credenciais comprometidas.

## Automacao

Para automatizar a rotação, configure um cron job mensal com a entrada `0 0 1 * * /path/to/carf-keycloak/scripts/rotate-secrets.sh`. Isso garante rotações periódicas automáticas sem intervenção manual, reduzindo o risco de esquecimento humano e mantendo uma disciplina de segurança consistente.
