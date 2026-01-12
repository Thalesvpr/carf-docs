# CONTROLLERS

Controllers REST do GEOAPI organizados por feature seguindo convenção RESTful com rotas padronizadas (GET /api/units, POST /api/units, GET /api/units/{id}, PUT /api/units/{id}, DELETE /api/units/{id}) e versionamento via URL ou header. Controllers herdam de ControllerBase marcados com [ApiController] habilitando validação automática ModelState, binding automático de request body/query params e retorno automático ProblemDetails para errors. Métodos action recebem DTOs validados, executam commands/queries via IMediator injetado, mapeiam Result<T> para ActionResult apropriado (Ok/Created/BadRequest/NotFound) e retornam responses com status codes HTTP semânticos. Autorização declarativa via [Authorize] attribute com policies verificando roles e claims específicas antes de executar action, rate limiting por endpoint via [RateLimit] attribute e API documentation via Swagger annotations gerando OpenAPI spec automático para consumers. Controllers não contêm lógica negócio apenas orquestração thin delegando para Application layer mantendo separation of concerns.

## Arquivos Principais (a criar)

**Core Controllers:**
- 01-units-controller.md - CRUD unidades + queries espaciais
- 02-holders-controller.md - Gestão titulares e vínculos
- 03-communities-controller.md - Comunidades e stats
- 04-teams-controller.md - Equipes técnicas
- 05-legitimation-controller.md - Workflow legitimação

**Supporting:**
- 06-documents-controller.md - Upload/download arquivos
- 07-reports-controller.md - Geração relatórios sob demanda
- 08-health-controller.md - Health checks e readiness probes

**Conventions:**
- 09-controller-base-patterns.md - Padrões comuns reutilizáveis
- 10-error-responses.md - Formatação ProblemDetails

---

**Última atualização:** 2026-01-12
