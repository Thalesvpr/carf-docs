# Data Flow

Fluxo de dados no GEOAPI segue Clean Architecture onde requisição HTTP entra pela Gateway Layer, passa por Application Layer orquestrando use cases, Domain Layer aplicando regras negócio, Infrastructure Layer persistindo dados, e resposta retorna caminho inverso. Request HTTP chega Controller que deserializa JSON para DTO, Middleware autentica JWT extrai tenant_id claims, ValidationFilter valida DTO via FluentValidation, Controller despacha Command ou Query via MediatR.

Command flow para operações escrita inicia CreateUnitCommand com dados DTO, Handler recebe command injeta IUnitRepository ICurrentUser, valida regras negócio via Domain Entity ou Specification, cria Entity via factory method ou construtor validando invariantes, persiste via Repository.Add e UnitOfWork.SaveChanges, dispara Domain Events UnitCreatedEvent via IDomainEventDispatcher, retorna DTO mapeado via extension method ToDto. Query flow para leitura otimizada inicia GetUnitsQuery com filtros paginação, Handler recebe query injeta DbContext diretamente para performance, projeta diretamente para DTO via Select evitando materialização Entity completa, aplica filtros Where OrderBy Skip Take, retorna lista DTOs paginada sem passar por Domain Layer.

Multi-tenancy flow garante isolamento dados onde JWT token contém tenant_id claim, TenantMiddleware extrai claim seta HttpContext.Items, TenantProvider lê HttpContext.Items retorna tenant_id atual, DbContext interceptor ExecuteSqlRaw SET LOCAL app.tenant_id = {tenantId} antes cada query, PostgreSQL RLS policies filtram automaticamente todas tabelas por tenant_id sem necessidade filtro explícito código aplicação.

Error handling flow captura exceções em múltiplas camadas onde Domain Exceptions ValidationException NotFoundException ConflictException contêm detalhes negócio, Application Exceptions UnauthorizedException ForbiddenException tratam autenticação autorização, ExceptionHandlerMiddleware captura todas exceções converte para ProblemDetails RFC 7807 com status code apropriado title detail instance, logs estruturados Serilog registram exception stack trace request context para debugging produção.

Caching flow otimiza leituras frequentes onde Query Handler verifica IDistributedCache Redis antes consultar banco, cache miss executa query banco e armazena resultado cache com TTL configurável, cache hit retorna dados direto Redis sem query banco, Domain Events InvalidateCacheEvent disparam invalidação seletiva quando Entity modificada, cache keys seguem padrão tenant:entity:id permitindo invalidação granular ou por tenant.

---

**Última atualização:** 2026-01-12
