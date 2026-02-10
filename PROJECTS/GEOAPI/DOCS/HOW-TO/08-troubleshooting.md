---
type: leaf
status: review
updated: 2026-02-08
---

# Troubleshooting - GEOAPI

Guia abrangente de resolucao de problemas para o GEOAPI, organizado por categoria. Cada entrada inclui sintoma, causa provavel e solucao passo a passo.

---

## Autenticacao e Autorizacao

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| 401 Unauthorized em todos os endpoints | Token JWT expirado ou Keycloak fora do ar | 1. Verificar Keycloak rodando: `docker compose ps keycloak`. 2. Obter novo token via password grant. 3. Verificar `Authority` no appsettings aponta para `http://localhost:8080/realms/carf` |
| 401 Unauthorized com token recente | `Audience` do token nao bate com configuracao | Decodificar token em jwt.io, verificar campo `aud` contem `geoapi`. Se nao, verificar client config no Keycloak (Audience mapper) |
| 403 Forbidden com token valido | Role insuficiente para o endpoint | 1. Decodificar token em jwt.io. 2. Verificar `realm_access.roles`. 3. Comparar com `[Authorize(Roles = "...")]` no controller. 4. Atribuir role necessaria no Keycloak |
| 403 Forbidden para usuario com role correta | Role claim nao mapeada corretamente | Verificar `TokenValidationParameters.RoleClaimType` no Program.cs. Deve ser `realm_access.roles` ou o path correto no JWT |
| Token expira muito rapido | Token lifetime curto no Keycloak | Keycloak Admin → Realm Settings → Tokens → Access Token Lifespan. Para dev, setar 30 minutos ou mais |
| `IDX10214: Audience validation failed` | Audience mismatch entre token e configuracao | Verificar `Keycloak:Audience` no appsettings. Deve ser exatamente o `client_id` do Keycloak |
| `IDX10205: Issuer validation failed` | Issuer URL diferente entre token e metadata | Verificar que `Authority` usa exatamente a mesma URL que o Keycloak reporta (sem trailing slash). Comparar `iss` do token com `Authority` |
| `Unable to obtain configuration from metadata` | Keycloak ainda iniciando ou URL errada | Aguardar Keycloak ficar healthy. Testar: `curl http://localhost:8080/realms/carf/.well-known/openid-configuration` |
| Login funciona no Swagger mas nao no frontend | CORS bloqueando preflight do token endpoint | Verificar que `AllowedOrigins` inclui a origin do frontend. Verificar headers CORS na resposta |

---

## Row-Level Security (RLS) e Multi-Tenancy

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| RLS nao filtra dados por tenant | Variavel de sessao nao definida | 1. Verificar `TenantMiddleware` esta registrado no pipeline. 2. Verificar que `SET app.current_tenant = '{tenantId}'` e executado antes das queries. 3. Inspecionar logs com level Debug |
| Dados de outro tenant aparecem | RLS policy nao criada para tabela | Verificar: `SELECT * FROM pg_policies WHERE tablename = 'nome_tabela'`. Se vazio, criar policy via migration |
| `current_setting(): unrecognized configuration parameter` | Variavel de sessao nao existe | Executar `SET app.current_tenant = '...'` antes de qualquer query. Verificar que TenantMiddleware nao esta sendo bypassado |
| Performance degradada com RLS | Indice faltando na coluna tenant_id | Criar indice: `CREATE INDEX idx_tabela_tenant ON tabela(tenant_id)`. Verificar plano de execucao com `EXPLAIN ANALYZE` |
| RLS bloqueia superadmin | Policy nao tem excecao para admin | Adicionar clausula `OR current_user = 'geoapi_admin'` na policy, ou usar `SET ROLE` para bypassar |
| Tenant ID nulo no contexto | Claim `tenant_id` ausente no token | Verificar protocol mapper no Keycloak que injeta `tenant_id` como claim. Verificar user attribute no Keycloak |

---

## Entity Framework Core e Database

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Migration falha com `relation already exists` | Migration aplicada parcialmente (crash durante apply) | 1. Verificar `__EFMigrationsHistory`. 2. Se migration esta na history mas tabela nao existe, remover registro manualmente. 3. Se tabela existe mas migration nao esta na history, inserir registro manualmente |
| `No migrations to apply` mas schema esta desatualizado | Migration gerada mas nao commitada por outro dev | `git pull` e re-executar `dotnet ef database update` |
| `The model has changed since the database was last created` | Schema drift entre model e banco | Gerar migration diff: `dotnet ef migrations add FixDrift ...`. Inspecionar o que foi gerado - pode indicar alteracoes manuais no banco |
| `Could not find type 'Geometry'` | Pacote NTS nao instalado ou UseNetTopologySuite nao chamado | `dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL.NetTopologySuite`. Verificar `UseNetTopologySuite()` no `AddDbContext` |
| Query retorna entidades duplicadas | Falta de `AsNoTracking()` + Include circular | Usar `.AsNoTracking()` em queries read-only. Verificar `ReferenceHandler.IgnoreCycles` na serializacao JSON |
| `Npgsql.PostgresException: 23505 duplicate key` | Violacao de constraint unique | Verificar dados duplicados antes de insert. Implementar upsert com `ON CONFLICT` se necessario |
| `Npgsql.PostgresException: 23503 foreign key violation` | Referencia a registro que nao existe | Verificar que a entidade referenciada existe antes do insert. Verificar cascade delete config |
| Connection pool exhausted | Muitas conexoes abertas sem dispose | Verificar que DbContext tem lifetime `Scoped` (padrao). Verificar que nao ha `new AppDbContext()` manual. Verificar connection pool size no connection string (`Maximum Pool Size=100`) |
| Query extremamente lenta | Falta de indice ou N+1 problem | 1. Habilitar EF Core query logging. 2. Verificar numero de queries por request (MiniProfiler). 3. Adicionar `.Include()` ou indices conforme necessario |
| `Timeout expired` em query | Query complexa ou lock de tabela | Aumentar timeout: `CommandTimeout=120` no connection string. Verificar locks: `SELECT * FROM pg_locks WHERE NOT granted` |

---

## PostGIS e Operacoes Geoespaciais

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| `ST_Intersects` retorna erro de tipo | Extension PostGIS nao instalada | `docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "CREATE EXTENSION IF NOT EXISTS postgis;"` |
| `Operation on mixed SRID geometries` | Geometrias com SRIDs diferentes | Converter para mesmo SRID antes da operacao: `ST_Transform(geom, 4326)`. Padronizar SRID 4326 (WGS84) |
| `Geometry type does not match column type` | Coluna espera Polygon mas recebe MultiPolygon | Validar geometria antes de persistir. Usar `ST_Multi()` para converter ou `ST_GeometryN(geom, 1)` para extrair |
| Indice espacial nao e utilizado | Query nao usa operadores espaciais corretos | Verificar com `EXPLAIN ANALYZE`. Usar `&&` (bounding box) antes de `ST_Intersects` para aproveitar indice GiST |
| `Coordinate values out of range` | Coordenadas longitude/latitude invertidas | Longitude: -180 a 180, Latitude: -90 a 90. SRID 4326 usa formato (longitude, latitude) |
| Area calculada retorna valor muito pequeno | Usando `ST_Area` com geometria geografica sem cast | Usar `ST_Area(geom::geography)` para resultado em metros quadrados, ou `ST_Area(ST_Transform(geom, <SRID_projecao_local>))` |
| Topologia invalida (self-intersection) | Poligono com lados que se cruzam | Validar com `ST_IsValid(geom)`. Corrigir com `ST_MakeValid(geom)` |

---

## MinIO / S3 Storage

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Upload falha com `AccessDenied` | Bucket nao existe ou credenciais erradas | 1. Verificar bucket: `mc ls local/`. 2. Criar se necessario: `mc mb local/carf-documents`. 3. Verificar AccessKey/SecretKey no appsettings |
| Upload falha com `EntityTooLarge` | Arquivo excede limite configurado | Verificar `Kestrel:Limits:MaxRequestBodySize` no appsettings. Padrao .NET: 30MB. Aumentar se necessario |
| Download retorna 404 | Objeto nao encontrado no path esperado | Verificar path do objeto: `mc ls local/carf-documents/path/to/file`. Verificar que tenant_id esta no path |
| MinIO console inacessivel (porta 9001) | Container nao iniciou console | Verificar que command inclui `--console-address ":9001"`. Verificar logs: `docker compose logs minio` |
| `Connection refused` ao acessar MinIO | Container nao rodando | `docker compose up -d minio`. Verificar: `docker compose ps minio` |
| Presigned URL expira imediatamente | Relogio do container dessincronizado | Verificar hora do container: `docker exec geoapi-minio date`. Sincronizar com host |
| Upload lento para arquivos grandes | Sem multipart upload configurado | Configurar multipart upload no SDK AWS S3 para arquivos > 5MB. Verificar `TransferUtility` ou `PutObjectAsync` com multipart |

---

## Redis e Cache

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| `Redis connection refused` | Container Redis nao rodando | `docker compose up -d redis`. Verificar: `docker exec geoapi-redis redis-cli ping` |
| Cache retorna dados desatualizados (stale) | TTL muito longo ou invalidacao nao implementada | Verificar TTL da chave: `docker exec geoapi-redis redis-cli TTL "chave"`. Implementar cache invalidation nos command handlers |
| `WRONGTYPE Operation against a key` | Tipo de operacao incompativel com tipo da chave | Verificar tipo: `docker exec geoapi-redis redis-cli TYPE "chave"`. Deletar chave corrompida se necessario |
| Cache miss constante | Chave expirada ou nunca setada | Verificar se o handler de leitura popula o cache. Verificar pattern da chave (deve incluir tenant_id para isolamento) |
| Redis out of memory | Limite de memoria atingido | Verificar: `docker exec geoapi-redis redis-cli INFO memory`. Ajustar `maxmemory` no docker-compose. Verificar policy de eviction |
| Serialization error ao cachear objeto | Objeto com referencia circular ou tipo nao serializavel | Verificar que DTOs (nao entities) sao cacheados. Usar `System.Text.Json` com `ReferenceHandler.IgnoreCycles` |

---

## Hangfire (Background Jobs)

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Hangfire dashboard inacessivel | Auth middleware bloqueando acesso | Verificar config de autorizacao do dashboard. Em dev, usar `AllowAnonymous`. Acessar: `https://localhost:7001/hangfire` |
| Job nao executa | Worker nao esta processando a queue correta | Verificar `Queues` no appsettings: `["default", "sync", "reports"]`. Verificar que job foi enqueued na queue certa |
| Job falha repetidamente (retries) | Exception no handler do job | Verificar exception no Hangfire Dashboard → Failed Jobs. Corrigir a causa raiz e re-enqueue |
| Schema hangfire nao criado | Connection string errada ou permissao insuficiente | Hangfire cria schema automaticamente. Verificar connection string e permissoes do usuario no PostgreSQL |
| Jobs duplicados | Enqueue chamado multiplas vezes | Usar `BackgroundJob.Schedule` com ID idempotente. Ou verificar se job ja existe antes de enqueue |
| Job lento travando outros | Worker unico processando job pesado | Aumentar `WorkerCount` no appsettings. Usar queues separadas para jobs pesados |

---

## SignalR (Real-time Notifications)

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Cliente nao recebe notificacao | Hub nao conectado ou grupo errado | Verificar conexao SignalR no browser devtools (WebSocket tab). Verificar que cliente entrou no grupo correto (tenant/community) |
| `WebSocket connection failed` | HTTPS/WSS mismatch ou proxy bloqueando | Verificar que frontend usa `wss://` para HTTPS. Se atras de proxy, configurar WebSocket passthrough |
| Notificacao chega duplicada | Cliente conectado a multiplas instancias | Configurar Redis backplane para SignalR: `services.AddSignalR().AddStackExchangeRedis(...)` |
| `HubException: unauthorized` | Token nao enviado na conexao WebSocket | Enviar token via query string: `new HubConnectionBuilder().WithUrl("/hub", options => { options.AccessTokenProvider = () => Task.FromResult(token); })` |
| Conexao cai apos 30s | Timeout de keep-alive | Configurar `KeepAliveInterval` e `ClientTimeoutInterval` no Hub. Verificar firewall nao esta cortando conexoes idle |

---

## CORS

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| `Access-Control-Allow-Origin` header ausente | Origin nao esta na lista permitida | Adicionar origin em `Cors:AllowedOrigins` no appsettings. Restart a API |
| Preflight request (OPTIONS) retorna 405 | Middleware CORS nao registrado ou mal posicionado | Verificar `app.UseCors()` esta antes de `app.UseAuthorization()` no pipeline |
| Funciona no Postman mas nao no browser | Postman nao aplica CORS (nao e browser) | Problema e de CORS (browser-only). Verificar configuracao conforme itens acima |
| Credenciais (cookies/auth header) nao enviadas | `AllowCredentials` nao configurado | Adicionar `.AllowCredentials()` na policy CORS. Nota: nao pode usar com `AllowAnyOrigin` |

---

## Swagger e Documentacao

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Swagger nao mostra endpoints | XML documentation nao gerada | Adicionar no `.csproj` do Gateway: `<GenerateDocumentationFile>true</GenerateDocumentationFile>` |
| Schema errado no Swagger | DTO nao atualizado ou conflito de nomes | Verificar que DTO correto e retornado no controller. Verificar `[ProducesResponseType]` attributes |
| Swagger nao autentica | Security definition nao configurada | Verificar `AddSecurityDefinition("Bearer", ...)` e `AddSecurityRequirement(...)` no Program.cs |
| Swagger mostra XML warnings | Membros publicos sem XML doc | Suprimir warning 1591 no `.csproj`: `<NoWarn>1591</NoWarn>` |

---

## Build e Runtime

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Hot reload nao funciona | Usando `dotnet run` ao inves de `dotnet watch` | Usar `dotnet watch run` para hot reload automatico |
| `Unable to find project` | Working directory errado | Verificar que esta na raiz do repositorio ou usar `--project` e `--startup-project` explicitos |
| Build falha com package restore errors | NuGet source inacessivel ou cache corrompido | `dotnet nuget locals all --clear` e depois `dotnet restore` |
| `Port already in use` ao rodar API | Outra instancia rodando ou servico na porta | Parar processo existente. Windows: `netstat -ano \| findstr 7001`. Linux: `lsof -i :7001` |
| `FileNotFoundException` em runtime | Assembly nao copiado para output | Verificar `CopyToOutputDirectory` no `.csproj` para arquivos necessarios |
| `OutOfMemoryException` em requests grandes | Payload muito grande sem streaming | Implementar streaming para uploads/downloads grandes. Verificar `MaxRequestBodySize` |
| Startup lento (>10s) | Muitos servicos sendo inicializados | Verificar health checks nao bloqueiam startup. Usar `IHostedService` para inicializacao assincrona |

---

## Docker e Infraestrutura Local

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Container reiniciando em loop | Configuracao invalida ou dependencia faltando | `docker compose logs <servico>` para ver erro de inicializacao |
| Disco cheio | Volumes e imagens Docker acumulados | `docker system prune -a` (remove tudo nao usado). Para volumes: `docker volume prune` |
| DNS resolution falha entre containers | Containers em redes diferentes | Verificar que todos os servicos usam a mesma network `carf-network` |
| Volume mount lento no macOS | Limitacao do Docker Desktop com bind mounts | Usar named volumes ao inves de bind mounts. Ou testar `:cached` flag |
| Container sem acesso a internet | Proxy corporativo bloqueando | Configurar proxy no Docker Desktop: Settings → Resources → Proxies |

---

## Checklist de Diagnostico Geral

Quando nenhum dos cenarios acima se aplica, seguir este checklist:

| Passo | Comando | O que verificar |
|-------|---------|-----------------|
| 1. Containers rodando? | `docker compose ps` | Todos os servicos `healthy` ou `running` |
| 2. API respondendo? | `curl http://localhost:5001/health` | Status `Healthy` para todos os checks |
| 3. Logs da API | Console onde `dotnet watch run` esta rodando | Exceptions, warnings |
| 4. Logs do Keycloak | `docker compose logs keycloak` | Erros de startup, realm nao encontrado |
| 5. Logs do PostgreSQL | `docker compose logs postgres` | Erros de conexao, permissao |
| 6. Token valido? | Decodificar em jwt.io | `exp` no futuro, `aud` contem `geoapi`, roles presentes |
| 7. Migration aplicada? | `dotnet ef migrations list ...` | Todas marcadas como `(applied)` |
| 8. Buckets existem? | `mc ls local/` | `carf-documents`, `carf-orthofotos`, `carf-exports` |
| 9. Redis acessivel? | `docker exec geoapi-redis redis-cli ping` | Retorna `PONG` |
| 10. Network conectada? | `docker network inspect carf-network` | Todos os containers listados |

---

## Referencias

| Recurso | Link |
|---------|------|
| Setup ambiente | [01-setup-dev-environment.md](./01-setup-dev-environment.md) |
| Docker Compose | [04-docker-compose-reference.md](./04-docker-compose-reference.md) |
| Migrations | [05-database-migrations.md](./05-database-migrations.md) |
| Debugging | [07-debugging-guide.md](./07-debugging-guide.md) |
| Appsettings | [02-appsettings-reference.md](../ARCHITECTURE/LAYERS/PRESENTATION/CONFIGURATION/02-appsettings-reference.md) |
| Environment Variables | [03-environment-variables.md](../ARCHITECTURE/LAYERS/PRESENTATION/CONFIGURATION/03-environment-variables.md) |
