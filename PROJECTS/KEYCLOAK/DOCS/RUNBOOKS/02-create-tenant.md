---
type: leaf
status: review
updated: 2026-02-08
---

# Criar e Gerenciar Tenants

## Conceito

Tenants no CARF são identificadores armazenados como user attributes no Keycloak. Eles aparecem no JWT como a claim `tenant_id`, permitindo que o backend aplique Row Level Security (RLS) para isolamento de dados.

## Adicionar Tenant a Usuario

O processo requer três chamadas sequenciais à Admin API. Primeiro, obtenha o admin token executando um `curl POST` para `realms/master/protocol/openid-connect/token` com `client_id=admin-cli`, `username=admin`, `password=admin` e `grant_type=password`, extraindo o `access_token` via `jq` e armazenando na variável `TOKEN`.

Em seguida, obtenha o ID do usuário executando um `curl GET` para `admin/realms/carf/users` com query parameter `username=joao.silva`, usando o header `Authorization: Bearer $TOKEN` e extraindo o `id` do primeiro resultado via `jq`, armazenando em `USER_ID`.

Por fim, atualize os attributes do usuário executando um `curl PUT` para `admin/realms/carf/users/$USER_ID` com payload JSON contendo o bloco `attributes` com `tenants: ["tenant1", "tenant2", "tenant3"]` e `current_tenant: ["tenant1"]`. Isso configura o acesso multi-tenant, permitindo que o usuário acesse os três tenants listados com `tenant1` como tenant ativo inicial.

## Trocar Tenant Ativo

Para trocar o tenant ativo sem alterar a lista de tenants acessíveis, execute um `curl PUT` para `admin/realms/carf/users/$USER_ID` com o header `Authorization: Bearer $TOKEN`. O payload JSON deve manter o array `tenants` inalterado (`["tenant1", "tenant2", "tenant3"]`) e modificar apenas o `current_tenant` para o novo valor, por exemplo `["tenant2"]`. A troca é efetivada ao fazer login novamente, quando o JWT passará a conter o novo `tenant_id` e o RLS filtrará os dados de acordo.

## Verificar Tenant no JWT

Para confirmar que o tenant está correto no token, faça login executando um `curl POST` para `realms/carf/protocol/openid-connect/token` com `client_id=reurbweb`, `grant_type=password`, `username=joao.silva` e `password=senha123`. Extraia o `access_token` via `jq` e armazene em `ACCESS_TOKEN`. Em seguida, decodifique o payload com `echo $ACCESS_TOKEN | cut -d. -f2 | base64 -d | jq .tenant_id`. O output deve ser `"tenant2"`, confirmando que a claim `tenant_id` está presente no JWT e reflete o `current_tenant` configurado nos user attributes do Keycloak. Essa claim é usada pelo backend para aplicar RLS, filtrando queries automaticamente por tenant.

## Client-Side Tenant Switcher

A implementação React para troca de tenant via Admin API consiste em uma função assíncrona `switchTenant` que recebe o parâmetro `newTenantId`. A função executa `await adminClient.users.update(...)` passando o objeto com `id: user.sub` e `attributes` contendo `tenants` preservado de `user.tenants` e `current_tenant: [newTenantId]`, atualizando os user attributes no Keycloak. Em seguida, executa `await keycloak.updateToken(5)` para forçar o refresh imediato do token, obtendo um novo JWT com o `tenant_id` atualizado. Isso permite que a interface ofereça um dropdown selector de tenants com switching sem necessidade de relogin completo, mantendo a sessão ativa e a experiência de uso fluida.

## Isolamento de Dados no Backend

O backend .NET implementa o isolamento via RLS usando o `tenant_id` extraído do JWT. O código obtém o tenant com `var tenantId = User.FindFirst("tenant_id").Value` e aplica o filtro nas queries com `var data = await context.Properties.Where(p => p.TenantId == tenantId).ToListAsync()`, retornando apenas registros do tenant atual. Essa camada de filtragem na application layer complementa o PostgreSQL RLS na database layer, implementando defesa em profundidade com múltiplas camadas de segurança para uma multi-tenancy robusta, auditável e em compliance com a LGPD.
