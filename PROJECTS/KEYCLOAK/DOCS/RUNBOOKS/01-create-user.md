---
type: leaf
status: review
description: "Procedimento para criação de usuários no Keycloak via Admin Console e via API"
updated: 2026-02-08
---

# Criar Usuário no Keycloak

## Via Admin Console

O caminho mais direto para criar um usuário é pela interface gráfica do Keycloak. Acesse o Admin Console em `http://localhost:8080` e selecione o realm `carf`. Na seção Users, clique em "Create new user". O campo username deve receber o CPF do usuário (formato `cpf-do-usuario`) ou um email como `email@example.com`. Preencha também o campo Email.

Na aba Attributes, adicione dois atributos essenciais para multi-tenancy. O atributo `tenants` recebe um array JSON com os tenants acessíveis pelo usuário, por exemplo `["tenant1", "tenant2"]`. O atributo `current_tenant` recebe o tenant ativo inicial, por exemplo `tenant1`.

Na aba Credentials, defina a senha do usuário e desmarque a opção "Temporary" para que o sistema não exija troca no primeiro login. Por fim, na aba Role mapping, atribua a role apropriada ao perfil do usuário, como `field-cadastrator`, `analyst` ou `admin`.

## Via Admin API

O fluxo pela API segue três etapas: obtenção do token administrativo, criação do usuário e atribuição de role.

Para obter o token, execute um `curl POST` para `http://localhost:8080/realms/master/protocol/openid-connect/token` com os parâmetros `client_id=admin-cli`, `username=admin`, `password=admin` e `grant_type=password`. Extraia o `access_token` do response via `jq` e armazene na variável `TOKEN`.

Para criar o usuário, execute um `curl POST` para `http://localhost:8080/admin/realms/carf/users` com o header `Authorization: Bearer $TOKEN` e `Content-Type: application/json`. O payload JSON deve conter `username` (ex: `joao.silva`), `email` (ex: `joao@example.com`), `enabled: true`, `emailVerified: false`, o bloco `attributes` com `tenants: ["tenant1"]` e `current_tenant: ["tenant1"]`, e o bloco `credentials` como array contendo um objeto com `type: password`, `value: senha123` e `temporary: false`.

Para atribuir a role, primeiro obtenha o `USER_ID` via `curl GET` para o endpoint `/users` com query parameter `username=joao.silva`, extraindo o `id` do primeiro resultado via `jq`. Em seguida, obtenha o `ROLE_ID` via `curl GET` para o endpoint `/roles/field-cadastrator`, extraindo o `id` via `jq`. Finalmente, execute um `curl POST` para o endpoint `/users/$USER_ID/role-mappings/realm` enviando um array JSON contendo o objeto `{ "id": "$ROLE_ID", "name": "field-cadastrator" }`, associando a role ao usuário recém-criado.

## Verificacao

Para confirmar que o usuário foi criado corretamente, execute um `curl POST` para `http://localhost:8080/realms/carf/protocol/openid-connect/token` com os parâmetros `client_id=reurbweb`, `grant_type=password`, `username=joao.silva` e `password=senha123`. Extraia o `access_token` via `jq` e decodifique o payload JWT usando `cut -d. -f2 | base64 -d | jq`. O resultado deve exibir as claims `tenants`, `current_tenant` e `roles`, confirmando que a autenticacao foi bem-sucedida e que as configuracoes de multi-tenancy estao funcionando.
