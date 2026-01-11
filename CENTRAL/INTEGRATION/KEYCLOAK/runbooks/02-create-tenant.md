# Criar e Gerenciar Tenants

## Conceito
Tenants no CARF são identificadores em user attributes que aparecem no JWT como `tenant_id`.

## Adicionar Tenant a Usuário

Obter admin token executando curl POST para realms/master/protocol/openid-connect/token com client_id admin-cli username admin password admin grant_type password extraindo access_token via jq armazenando em TOKEN, obter user ID executando curl GET para admin/realms/carf/users com query parameter username joao.silva usando Authorization header Bearer TOKEN extraindo id do primeiro resultado via jq armazenando em USER_ID, e atualizar attributes executando curl PUT para admin/realms/carf/users/USER_ID enviando payload JSON contendo attributes object com tenants array tenant1 tenant2 tenant3 e current_tenant array tenant1 configurando multi-tenancy para usuário permitindo acesso múltiplos tenants com tenant1 como ativo inicial.

## Trocar Tenant Ativo

Atualizar apenas current_tenant executando curl PUT para admin/realms/carf/users/USER_ID com Authorization header Bearer TOKEN enviando payload JSON mantendo tenants array tenant1 tenant2 tenant3 inalterado mas modificando current_tenant array para tenant2 efetivando troca de tenant ativo sem alterar permissões acesso tenants disponíveis para usuário garantindo isolamento dados via RLS ao fazer login novamente.

## Verificar Tenant no JWT

Fazer login e decodificar token executando curl POST para realms/carf/protocol/openid-connect/token com client_id geoweb grant_type password username joao.silva password senha123 extraindo access_token via jq armazenando em ACCESS_TOKEN seguido por echo ACCESS_TOKEN pipe cut menos d ponto menos f2 pipe base64 menos d pipe jq ponto tenant_id exibindo output tenant2 confirmando claim tenant_id presente no JWT payload refletindo current_tenant configurado no Keycloak user attributes usado backend RLS isolamento dados queries filtradas automaticamente.

## Client-Side Tenant Switcher

Implementação React para trocar tenant via Admin API definindo função async switchTenant recebendo parâmetro newTenantId executando await adminClient.users.update passando objeto id igual user.sub attributes contendo tenants preservado de user.tenants e current_tenant array newTenantId atualizando Keycloak user attributes seguido por await keycloak.updateToken com parâmetro cinco forçando refresh token imediato obtendo novo JWT com tenant_id atualizado refletindo mudança permitindo interface usuário dropdown selector múltiplos tenants switching sem relogin completo mantendo sessão ativa UX fluida.

## Isolamento de Dados (Backend)

Backend .NET implementa RLS com tenant_id do JWT extraindo claim executando var tenantId igual User.FindFirst com parâmetro tenant_id acessando propriedade Value seguido por var data igual await context.Properties aplicando filtro Where com lambda p TenantId igual igual tenantId executando ToListAsync retornando apenas registros matching tenant atual garantindo isolamento completo dados nível application layer complementando PostgreSQL RLS database layer defesa em profundidade múltiplas camadas segurança multi-tenancy robusta confiável auditável compliance LGPD separação tenant obrigatória crítica.
