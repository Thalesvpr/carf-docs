# API

Testes API REST do CARF. authentication-api-tests.md (login credenciais válidas retorna 200 + JWT, inválidas 401, token expirado refresh válido retorna novo token, logout invalida refresh). units-api-tests.md (POST cria unidade retorna 201 + Location header, validação falha 422 errors array, GET by id 200 + json, 404 not found, PATCH atualiza campos parciais, DELETE 204, filtros query params retornam subset correto, paginação page/pageSize). holders-api-tests.md, communities-api-tests.md, reports-api-tests.md, legitimation-api-tests.md seguem padrão similar testando CRUD, validações, autorizações RBAC, multi-tenancy isolation. Integration tests rodando contra banco de dados em containers isolados.

---

**Última atualização:** 2025-01-05
