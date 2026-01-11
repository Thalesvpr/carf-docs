# Criar Usuário no Keycloak

## Via Admin Console
1. Acesse http://localhost:8080 → Admin Console
2. Realm: `carf`
3. Users → Create new user
4. Username: `cpf-do-usuario` ou `email@example.com`
5. Email: preencher
6. Attributes → Add:
   - `tenants`: `["tenant1", "tenant2"]`
   - `current_tenant`: `tenant1`
7. Credentials → Set password (desmarcar "Temporary")
8. Role mapping → Assign role: `user`, `admin`, etc.

## Via Admin API

Obter admin token executando curl POST para http://localhost:8080/realms/master/protocol/openid-connect/token com parâmetros client_id admin-cli username admin password admin grant_type password extraindo access_token via jq armazenando em variável TOKEN. Criar usuário executando curl POST para http://localhost:8080/admin/realms/carf/users com Authorization header Bearer TOKEN Content-Type application/json enviando payload JSON contendo username joao.silva email joao@example.com enabled true emailVerified false attributes tenants array tenant1 current_tenant array tenant1 credentials array contendo objeto type password value senha123 temporary false. Atribuir role obtendo USER_ID via curl para endpoint users com query parameter username joao.silva extraindo id do primeiro resultado via jq, obtendo ROLE_ID via curl para endpoint roles/user extraindo id via jq, e executando curl POST para endpoint users/USER_ID/role-mappings/realm enviando array JSON contendo objeto id ROLE_ID name user associando role ao usuário criado.

## Verificação

Verificar login do usuário executando curl POST para http://localhost:8080/realms/carf/protocol/openid-connect/token com parâmetros client_id geoweb grant_type password username joao.silva password senha123 extraindo access_token via jq decodificando payload JWT usando cut minus d ponto minus f2 pipe base64 minus d pipe jq exibindo claims token incluindo tenants current_tenant roles confirmando autenticação bem-sucedida configurações corretas multi-tenancy funcionando.
