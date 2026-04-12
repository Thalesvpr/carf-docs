---
type: leaf
status: review
updated: 2026-02-08
---

# API E2E Tests

Os testes end-to-end da GEOAPI validam o comportamento completo da API, da requisicao HTTP ate a persistencia no banco de dados. Utilizam a biblioteca TestContainers para provisionar containers Docker de PostgreSQL (com PostGIS) e Redis durante a execucao, garantindo um ambiente identico ao de producao sem depender de infraestrutura externa.

## Setup com WebApplicationFactory

### ApiFixture

A classe `ApiFixture` implementa `IAsyncLifetime` e gerencia toda a infraestrutura dos testes E2E.

**Inicializacao (InitializeAsync):**

1. Sobe container PostgreSQL (postgis/postgis:16-3.4) via Testcontainers
2. Sobe container Redis (redis:7-alpine) via Testcontainers
3. Cria instancia de `WebApplicationFactory<Program>` com overrides de configuracao
4. Executa migrations no container PostgreSQL
5. Seed de dados basicos (tenant de teste, community de teste)

**Overrides de Services:**

A `WebApplicationFactory` permite substituir servicos registrados no DI container para isolar os testes de dependencias externas.

| Servico Original | Substituicao no Teste | Motivo |
|-----------------|----------------------|--------|
| Connection string PostgreSQL | String do container Testcontainers | Banco isolado por execucao |
| Connection string Redis | String do container Redis | Cache isolado |
| Keycloak (IAuthenticationService) | FakeJwtBearerAuthentication | Nao depende de Keycloak real |
| IFileStorage (MinIO/S3) | InMemoryFileStorage | Nao depende de storage externo |
| IEmailSender | FakeEmailSender | Nao envia emails reais |

**Configuracao do WebApplicationFactory:**

O override e feito no metodo `ConfigureWebHost`:

- `builder.ConfigureServices(services => { ... })` - substitui registros de DI
- `builder.ConfigureTestServices(services => { ... })` - adiciona servicos de teste
- `builder.UseEnvironment("Testing")` - ativa configuracao de teste
- Desabilita background jobs (Hangfire) para evitar interferencia

### Criacao do HttpClient

A fixture cria o `HttpClient` via `factory.CreateClient()`. O client ja aponta para o host in-process (sem necessidade de porta real).

Para cada teste, o client recebe o header Authorization com JWT gerado pelo helper.

## Gerador de JWT Fake

### JwtTestHelper

A classe `JwtTestHelper` gera tokens JWT validos assinados com uma chave simetrica de teste. Os tokens sao aceitos pelo middleware de autenticacao porque o `FakeJwtBearerAuthentication` configura a mesma chave.

**Parametros configuráveis:**

| Claim | Tipo | Exemplo | Obrigatorio |
|-------|------|---------|-------------|
| sub | string (GUID) | `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa` | Sim |
| tenant_id | string (GUID) | `bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb` | Sim |
| roles | array de strings | `["COORDINATOR", "CADASTRATOR"]` | Sim |
| email | string | `agente@carf.gov.br` | Sim |
| name | string | `Joao Agente` | Nao |
| preferred_username | string | `joao.agente` | Nao |

**Metodos:**

- `GenerateToken(tenantId, userId, roles, email)` - gera token JWT com claims especificos
- `GenerateTokenForCoordinator(tenantId)` - atalho para token de coordenador
- `GenerateTokenForCadastrator(tenantId)` - atalho para token de cadastrador
- `GenerateTokenForAdmin()` - atalho para token de administrador do sistema
- `GenerateExpiredToken(tenantId, userId, roles)` - gera token com `exp` no passado

**Configuracao da Chave:**

A chave simetrica de teste e uma string fixa compartilhada entre o `JwtTestHelper` e o `FakeJwtBearerAuthentication`:

- Algoritmo: HMAC SHA-256 (HS256)
- Chave: string fixa de 256 bits usada apenas em testes
- Issuer: `test-issuer`
- Audience: `carf-geoapi-test`
- Lifetime default: 1 hora

### AuthenticateAsAsync Helper

O metodo `AuthenticateAsAsync(client, tenantId, roles)` e um wrapper que:

1. Gera um JWT via `JwtTestHelper.GenerateToken(...)`
2. Adiciona o header `Authorization: Bearer {token}` ao HttpClient
3. Retorna o client configurado para uso no teste

## Setup de Tenant em E2E

### Seed de Dados por Tenant

Antes dos testes de cada fixture, os seguintes dados sao criados no banco:

1. **Tenant de teste** - GUID fixo `bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb`
2. **Community de teste** - community com boundary cobrindo a regiao de Brasilia
3. **Blocos** - 2 blocos dentro da community

Para testes que precisam de dados adicionais, helpers criam entidades sob demanda:

- `CreateUnitAsync(client)` - cria uma unit via POST /api/units e retorna o UnitDto
- `CreateHolderAsync(client)` - cria um holder via POST /api/holders e retorna o HolderDto
- `LinkHolderAsync(client, unitId, holderId)` - vincula holder a unit
- `UploadDocumentAsync(client, unitId, file)` - faz upload de documento

### Isolamento por Teste

Cada classe de teste usa o tenant de teste padrao. Para testes de cross-tenant, um segundo tenant com GUID `cccccccc-cccc-cccc-cccc-cccccccccccc` e criado na fixture.

## Cenarios de Teste por Endpoint

### Units Endpoints

| Cenario | Endpoint | Metodo | Request | Resultado Esperado |
|---------|----------|--------|---------|-------------------|
| Criar unidade valida | /api/units | POST | UnitCreateDto com geometria valida | HTTP 201, corpo contem UnitDto com codigo UNI-YYYY-NNNNN |
| Criar unidade sem geometria | /api/units | POST | UnitCreateDto sem geometry | HTTP 400, erros de validacao |
| Criar unidade com sobreposicao | /api/units | POST | Geometria sobreposta com unit existente | HTTP 409 Conflict |
| Obter unidade por ID | /api/units/{id} | GET | ID valido | HTTP 200, UnitDto completo |
| Obter unidade inexistente | /api/units/{id} | GET | GUID aleatorio | HTTP 404 Not Found |
| Obter unidade de outro tenant | /api/units/{id} | GET | ID de unit do TenantC | HTTP 404 (RLS oculta) |
| Listar unidades com paginacao | /api/units?page=2&limit=20 | GET | Parametros de paginacao | HTTP 200, 20 registros, pagina 2, totalCount correto |
| Listar unidades por status | /api/units?status=Draft | GET | Filtro por status | HTTP 200, apenas units Draft |
| Listar unidades por community | /api/units?communityId={id} | GET | Filtro por community | HTTP 200, apenas units da community |
| Atualizar unidade | /api/units/{id} | PUT | UnitUpdateDto com novos dados | HTTP 200, dados atualizados |
| Atualizar unidade Approved | /api/units/{id} | PUT | Unidade com status Approved | HTTP 422, "Cannot edit approved unit" |
| Excluir unidade Draft | /api/units/{id} | DELETE | Unidade Draft | HTTP 204 No Content |
| Excluir unidade Approved | /api/units/{id} | DELETE | Unidade Approved | HTTP 422, "Cannot delete approved unit" |
| Submit unidade | /api/units/{id}/submit | POST | Unit com holders somando 100% | HTTP 200, status muda para Pending |
| Submit sem holders | /api/units/{id}/submit | POST | Unit sem holders | HTTP 422, "At least one holder required" |
| Aprovar unidade | /api/units/{id}/approve | POST | Unit Pending, role COORDINATOR | HTTP 200, status Approved |
| Aprovar sem permissao | /api/units/{id}/approve | POST | Unit Pending, role CADASTRATOR | HTTP 403 Forbidden |
| Rejeitar unidade | /api/units/{id}/reject | POST | Unit Pending, motivo preenchido | HTTP 200, status Rejected |

### Holders Endpoints

| Cenario | Endpoint | Metodo | Resultado Esperado |
|---------|----------|--------|--------------------|
| Criar holder pessoa fisica | /api/holders | POST | HTTP 201, HolderDto com CPF |
| Criar holder CPF duplicado no tenant | /api/holders | POST | HTTP 409 Conflict |
| Listar holders com busca | /api/holders?search=Joao | GET | HTTP 200, holders com nome contendo "Joao" |
| Vincular holder a unidade | /api/units/{id}/holders | POST | HTTP 200, holder vinculado |
| Desvincular holder | /api/units/{id}/holders/{holderId} | DELETE | HTTP 204 |

### Communities Endpoints

| Cenario | Endpoint | Metodo | Resultado Esperado |
|---------|----------|--------|--------------------|
| Criar community | /api/communities | POST | HTTP 201, CommunityDto com boundary |
| Listar communities | /api/communities | GET | HTTP 200, lista paginada |
| Obter community com stats | /api/communities/{id} | GET | HTTP 200, inclui contagem de units por status |
| Atualizar boundary | /api/communities/{id}/boundary | PUT | HTTP 200, boundary atualizado |

### Documents Endpoints

| Cenario | Endpoint | Metodo | Resultado Esperado |
|---------|----------|--------|--------------------|
| Upload documento | /api/units/{id}/documents | POST (multipart) | HTTP 201, DocumentDto com URL |
| Download documento | /api/documents/{id}/download | GET | HTTP 200, stream do arquivo |
| Listar documentos da unidade | /api/units/{id}/documents | GET | HTTP 200, lista de DocumentDto |
| Upload tipo invalido | /api/units/{id}/documents | POST | HTTP 400, "Invalid document type" |
| Upload acima do limite | /api/units/{id}/documents | POST (11MB) | HTTP 413, "File too large" |

### Sync Endpoints

| Cenario | Endpoint | Metodo | Resultado Esperado |
|---------|----------|--------|--------------------|
| Push batch valido | /api/sync/push | POST | HTTP 200, resultados por operacao |
| Pull desde timestamp | /api/sync/pull?since={ts} | GET | HTTP 200, delta de mudancas |

Para detalhes completos dos testes de sync, consulte `TESTS/E2E/02-sync-e2e-tests.md`.

### Health Endpoints

| Cenario | Endpoint | Metodo | Resultado Esperado |
|---------|----------|--------|--------------------|
| Health check saudavel | /health | GET | HTTP 200, status "Healthy" |
| Ready check | /health/ready | GET | HTTP 200, todos os servicos operacionais |

## Teste de Workflow Completo

O teste `FullWorkflow_CreateToApprove_Success` executa o fluxo de ponta a ponta:

1. **Autenticar como coordenador** - gera JWT com role COORDINATOR
2. **Criar community** - POST /api/communities com boundary
3. **Criar unidade** - POST /api/units com geometria dentro da community
4. **Criar holder** - POST /api/holders com dados de pessoa fisica
5. **Vincular holder** - POST /api/units/{id}/holders com percentual 100%
6. **Upload documento** - POST /api/units/{id}/documents com foto de fachada
7. **Submit unidade** - POST /api/units/{id}/submit — status muda para Pending
8. **Aprovar unidade** - POST /api/units/{id}/approve — status muda para Approved
9. **Verificar estado final** - GET /api/units/{id} retorna unit Approved com holder e documento

Cada etapa verifica o HTTP status code e o corpo da resposta. Se qualquer etapa falhar, o teste falha imediatamente com a mensagem indicando a etapa.

## Testes de Autenticacao e Autorizacao

### Edge Cases de Autenticacao

| Cenario | Setup | Resultado Esperado |
|---------|-------|--------------------|
| Sem token | Request sem header Authorization | HTTP 401 Unauthorized |
| Token expirado | JWT com exp no passado (via GenerateExpiredToken) | HTTP 401 Unauthorized |
| Token com assinatura invalida | JWT assinado com chave diferente | HTTP 401 Unauthorized |
| Token sem tenant_id | JWT sem claim tenant_id | HTTP 401 Unauthorized |
| Token sem roles | JWT com array roles vazio | HTTP 403 para endpoints protegidos |

### Edge Cases de Autorizacao por Role

| Cenario | Role | Endpoint | Resultado Esperado |
|---------|------|----------|--------------------|
| CADASTRATOR cria unidade | CADASTRATOR | POST /api/units | HTTP 201 (permitido) |
| CADASTRATOR aprova unidade | CADASTRATOR | POST /api/units/{id}/approve | HTTP 403 Forbidden |
| COORDINATOR aprova unidade | COORDINATOR | POST /api/units/{id}/approve | HTTP 200 (permitido) |
| CADASTRATOR cria community | CADASTRATOR | POST /api/communities | HTTP 403 Forbidden |
| COORDINATOR cria community | COORDINATOR | POST /api/communities | HTTP 201 (permitido) |
| FIELD_AGENT acesso limitado | FIELD_AGENT | GET /api/units | HTTP 200 (somente leitura) |
| FIELD_AGENT tenta criar | FIELD_AGENT | POST /api/units | HTTP 403 Forbidden |

### Edge Cases de Tenant

| Cenario | Setup | Resultado Esperado |
|---------|-------|--------------------|
| Tenant inexistente | JWT com tenant_id de GUID aleatorio | HTTP 403 ou listagens vazias |
| Acesso cross-tenant via URL | JWT TenantA, GET /api/units/{id_de_TenantB} | HTTP 404 (RLS oculta o recurso) |
| Criacao cross-tenant | JWT TenantA, POST /api/units com communityId de TenantB | HTTP 404 "Community not found" |

## Organizacao dos Testes E2E

```
Carf.GeoApi.Tests.E2E/
  Endpoints/
    UnitsE2ETests.cs
    HoldersE2ETests.cs
    CommunitiesE2ETests.cs
    DocumentsE2ETests.cs
    HealthE2ETests.cs
  Workflows/
    FullWorkflowTests.cs
    SubmitRejectRetryTests.cs
  Auth/
    AuthenticationE2ETests.cs
    AuthorizationE2ETests.cs
    TenantIsolationE2ETests.cs
  Sync/
    PushE2ETests.cs
    PullE2ETests.cs
    ConflictE2ETests.cs
  Fixtures/
    ApiFixture.cs
    FakeJwtBearerAuthentication.cs
    InMemoryFileStorage.cs
    FakeEmailSender.cs
  Helpers/
    JwtTestHelper.cs
    AuthenticateAsAsync.cs
    CreateUnitAsync.cs
    CreateHolderAsync.cs
    SyncSeedHelper.cs
```

## Tabela Resumo de Cobertura

| Grupo de Endpoints | Total de Cenarios | Cobertos | Pendentes |
|-------------------|-------------------|----------|-----------|
| Units (CRUD) | 13 | 13 | 0 |
| Units (Workflow) | 5 | 5 | 0 |
| Holders | 5 | 5 | 0 |
| Communities | 4 | 4 | 0 |
| Documents | 5 | 5 | 0 |
| Sync | 2 | 2 | 0 |
| Health | 2 | 2 | 0 |
| Autenticacao | 5 | 5 | 0 |
| Autorizacao (role) | 7 | 7 | 0 |
| Autorizacao (tenant) | 3 | 3 | 0 |
| Workflow completo | 1 | 1 | 0 |
| **Total** | **52** | **52** | **0** |

## Referencias Cruzadas

- Estrategia de testes: `TESTS/00-testing-strategy.md`
- Testes de sync E2E: `TESTS/E2E/02-sync-e2e-tests.md`
- Controllers da API: `PRESENTATION/CONTROLLERS/`
- Autenticacao Keycloak: `INFRA/INTEGRATIONS/01-keycloak-integration.md`
- Middleware de erros: `PRESENTATION/MIDDLEWARES/01-exception-handling.md`
