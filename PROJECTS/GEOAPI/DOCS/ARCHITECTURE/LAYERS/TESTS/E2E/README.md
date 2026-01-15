# E2E

Testes end-to-end do GEOAPI exercitando API completa via HTTP requests validando contratos REST, autenticação JWT, autorização RBAC, serialization JSON e fluxos completos desde request até response atravessando todas camadas. WebApplicationFactory cria servidor in-memory hospedando aplicação ASP.NET Core com todas dependências configuradas (DbContext apontando Testcontainers PostgreSQL, Redis mock, Keycloak mock retornando tokens válidos, S3 mock) permitindo enviar HttpClient requests reais para endpoints verificando status codes, headers e response bodies. Testes validam happy paths (criar unidade retorna 201 Created com Location header, listar unidades retorna 200 OK com array JSON) e error scenarios (criar sem autenticação retorna 401 Unauthorized, atualizar entity outro tenant retorna 404 Not Found por RLS, input inválido retorna 400 Bad Request com validation errors ProblemDetails). Fluxos multi-step testam sequências realistas como field agent login → criar unidade → upload foto → submit para análise → analista login → aprovar legitimação verificando state transitions corretas e domain events despachados notificando stakeholders via SignalR.

## Arquivos Principais (a criar)

**Authentication & Authorization:**
- 01-authentication-flow-e2e-tests.md - Login, token refresh, logout
- 02-authorization-rbac-e2e-tests.md - Endpoints protegidos por roles
- 03-multi-tenancy-isolation-e2e-tests.md - RLS isolation cross tenants

**Units Management:**
- 04-create-unit-e2e-tests.md - POST /api/units workflow completo
- 05-update-unit-e2e-tests.md - PUT /api/units/{id} validations
- 06-spatial-queries-e2e-tests.md - GET /api/units?within=polygon
- 07-unit-status-transitions-e2e-tests.md - PATCH status workflow

**Holders Management:**
- 08-create-holder-e2e-tests.md - POST /api/holders com vínculos
- 09-link-holder-to-unit-e2e-tests.md - Relacionamento N:M

**Legitimation Process:**
- 10-legitimation-workflow-e2e-tests.md - Submit → Análise → Aprovação
- 11-legitimation-documents-upload-e2e-tests.md - Upload docs S3

**Teams & Communities:**
- 12-team-assignment-e2e-tests.md - Atribuir equipe para comunidade
- 13-community-stats-e2e-tests.md - Agregações unidades por status

**Reports:**
- 14-generate-report-e2e-tests.md - POST /api/reports async job
- 15-download-report-e2e-tests.md - GET presigned URL S3

**Real-time Notifications:**
- 16-signalr-notifications-e2e-tests.md - WebSocket events push

## Convenções

E2E tests usam HttpClient fornecido por WebApplicationFactory enviando requests reais para endpoints com headers autenticação (Bearer token gerado por helper method), query params e request bodies JSON verificando response via assertions sobre StatusCode, Headers e Content deserialized para DTOs esperados. Test fixtures compartilhados via IClassFixture provêem WebApplicationFactory configurada e DbContext seeded com dados base (users, roles, tenant) reduzindo setup time entre tests mantendo isolation via transaction rollback ou database reset após cada test. Helpers criam tokens JWT válidos com claims específicas (tenant_id, user_id, roles) permitindo tests simular diferentes usuários e verificar authorization policies sem depender de Keycloak real rodando. Response assertions verificam não apenas status code mas schema completo validando response body contra expected DTO structure usando FluentAssertions Should().BeEquivalentTo() comparando deep equality incluindo nested objects e arrays. Performance assertions usando StopWatch verificam endpoints respondem dentro SLA esperado (< 200ms para queries simples, < 2s para aggregations complexas) identificando regressões performance antes deploy production.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (16) antes do rodapé - considerar converter para parágrafo denso.
