---
type: leaf
status: review
updated: 2026-02-08
---

# Security Implementation

Detalhes concretos da implementacao de seguranca da GEOAPI, incluindo validacao de tokens JWT, rate limiting, HTTPS, gestao de segredos, validacao de entrada e auditoria.

## JWT Token Validation

A GEOAPI valida tokens JWT emitidos pelo Keycloak usando a biblioteca Microsoft.AspNetCore.Authentication.JwtBearer. A configuracao dos parametros de validacao segue:

### TokenValidationParameters

| Parametro | Valor | Descricao |
|-----------|-------|-----------|
| ValidateIssuer | true | Issuer deve corresponder exatamente a URL do realm Keycloak |
| ValidIssuer | `https://auth.carf.gov.br/realms/carf` | URL do realm em producao |
| ValidateAudience | true | Audience deve ser "geoapi" |
| ValidAudience | `geoapi` | Client ID da GEOAPI no Keycloak |
| ValidateLifetime | true | Token expirado e rejeitado |
| RequireExpirationTime | true | Token sem claim `exp` e rejeitado |
| ClockSkew | TimeSpan.FromMinutes(1) | Tolerancia de 1 minuto para diferenca de relogios entre servidores |
| ValidateIssuerSigningKey | true | Assinatura validada contra chave publica do Keycloak |
| IssuerSigningKeyResolver | JWKS endpoint | Chaves carregadas de `/.well-known/openid-configuration` |
| TokenDecryptionKey | none | Tokens sao assinados (RS256), nao encriptados |
| RequireSignedTokens | true | Tokens sem assinatura sao rejeitados |

### Claims Extraidos do Token

| Claim JWT | Propriedade C# | Uso |
|-----------|---------------|-----|
| sub | UserId | Identificacao do usuario |
| tenant_id | TenantId | Isolamento por tenant (custom claim via protocol mapper) |
| realm_access.roles | Roles | Autorizacao RBAC |
| preferred_username | Username | Logging e auditoria |
| email | Email | Notificacoes |

### Refresh de Chaves JWKS

As chaves publicas do Keycloak sao carregadas automaticamente via endpoint JWKS e cacheadas por 24 horas. Quando uma validacao falha por chave desconhecida, o middleware tenta recarregar as chaves uma vez antes de rejeitar o token. Isso permite rotacao de chaves sem downtime.

## Rate Limiting

O rate limiting protege a GEOAPI contra abuso e garante disponibilidade para todos os tenants.

### Configuracao por Camada

| Camada | Limite | Janela | Identificador | Descricao |
|--------|--------|--------|---------------|-----------|
| Per-Tenant | 100 req/min | Sliding window | tenant_id do JWT | Evita que um tenant monopolize recursos |
| Global | 1000 req/min | Fixed window | Total do servidor | Protecao contra DDoS |
| Per-IP (nao autenticado) | 20 req/min | Sliding window | IP do request | Protege endpoints publicos (health, login) |
| Per-User (sync) | 10 req/min | Fixed window | sub do JWT | Evita sync excessivo de um unico dispositivo |

### Implementacao

O rate limiting utiliza o middleware nativo do ASP.NET Core (`Microsoft.AspNetCore.RateLimiting`) com backend em memoria para single-instance ou Redis para multi-instance.

### Headers de Resposta

| Header | Descricao | Exemplo |
|--------|-----------|---------|
| X-RateLimit-Limit | Limite maximo da janela | 100 |
| X-RateLimit-Remaining | Requests restantes na janela atual | 73 |
| X-RateLimit-Reset | Timestamp Unix de quando a janela reseta | 1710510660 |
| Retry-After | Segundos ate poder tentar novamente (apenas no 429) | 30 |

### Resposta ao Exceder Limite

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1710510660

{
  "type": "https://tools.ietf.org/html/rfc6585#section-4",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Rate limit exceeded. Try again in 30 seconds.",
  "traceId": "00-abc123-def456-00"
}
```

## HTTPS Requirements

### Configuracao TLS

| Parametro | Valor | Justificativa |
|-----------|-------|---------------|
| Protocolo minimo | TLS 1.2 | TLS 1.0 e 1.1 possuem vulnerabilidades conhecidas (POODLE, BEAST) |
| Cipher suites | TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256 | Suites modernas com forward secrecy |
| Certificate | Let's Encrypt (producao), dev-certs (desenvolvimento) | Certificados validos em todos os ambientes |

### HSTS (HTTP Strict Transport Security)

| Ambiente | HSTS | max-age | includeSubDomains | preload |
|----------|------|---------|-------------------|---------|
| Development | Desabilitado | - | - | - |
| Staging | Habilitado | 30 dias | Sim | Nao |
| Production | Habilitado | 1 ano (31536000s) | Sim | Sim |

### Desenvolvimento Local

Em desenvolvimento, o certificado HTTPS e configurado via `dotnet dev-certs https --trust`. O Kestrel aceita HTTP na porta 5000 e HTTPS na porta 5001. Em staging e producao, apenas HTTPS e aceito; requests HTTP recebem redirect 301 para HTTPS.

## Secrets Management

### Estrategia por Ambiente

| Ambiente | Mecanismo | Descricao |
|----------|----------|-----------|
| Development | User Secrets + appsettings.Development.json | `dotnet user-secrets set "Keycloak:ClientSecret" "dev-secret"`. Secrets armazenados fora do repositorio em `%APPDATA%\Microsoft\UserSecrets\` |
| CI/CD | Variaveis de ambiente | Secrets injetados pelo pipeline (GitHub Actions secrets ou Azure DevOps variables) |
| Staging | Variaveis de ambiente do container | Definidos no docker-compose ou Kubernetes secrets |
| Production | Azure Key Vault ou HashiCorp Vault | Carregados no startup via configuration provider. Rotacao sem redeploy via reload periodico |

### Secrets Gerenciados

| Secret | Descricao | Rotacao |
|--------|-----------|---------|
| ConnectionStrings:DefaultConnection | String de conexao PostgreSQL | A cada 90 dias |
| Keycloak:ClientSecret | Secret do client "geoapi" no Keycloak | A cada 90 dias |
| Redis:Password | Senha do Redis para cache e rate limiting | A cada 90 dias |
| MinIO:SecretKey | Chave de acesso ao MinIO/S3 para storage | A cada 90 dias |
| Jwt:SigningKey | Nao utilizado (validacao via JWKS) | N/A |

### Regras de Seguranca para Secrets

- NUNCA commitar secrets no repositorio (`.gitignore` inclui `appsettings.*.json` exceto template)
- Secrets em logs sao mascarados automaticamente pelo middleware de logging
- Acesso ao Key Vault requer Managed Identity (sem credenciais em codigo)
- Alertas configurados para rotacao pendente (15 dias antes da expiracao)

## Input Validation

### Camadas de Validacao

| Camada | Tecnologia | Escopo | Exemplo |
|--------|-----------|--------|---------|
| 1. Model Binding | ASP.NET Core | Tipos e formato | JSON invalido retorna 400 |
| 2. FluentValidation | MediatR Pipeline | Regras de negocio | CPF com Mod-11 invalido |
| 3. Domain Validation | Entidades DDD | Invariantes | Status transition invalida |
| 4. Database Constraints | PostgreSQL | Integridade | Unique, FK, CHECK constraints |

### Protecoes Contra Ataques

| Vetor de Ataque | Protecao | Implementacao |
|-----------------|---------|---------------|
| SQL Injection | Queries parametrizadas | EF Core gera queries parametrizadas automaticamente. RLS adiciona camada extra de isolamento |
| XSS | Nao aplicavel | GEOAPI e API-only, sem renderizacao de HTML. Clientes (GEOWEB, REURBCAD) sao responsaveis por sanitizacao na exibicao |
| CSRF | Nao aplicavel | API stateless com Bearer token. Sem cookies de sessao para proteger |
| File Upload Malicioso | Validacao de content type + tamanho | Content types permitidos: image/jpeg, image/png, application/pdf. Tamanho maximo: 10MB por arquivo. Em producao, scan antivirus via ClamAV |
| Mass Assignment | DTOs explicitos | Apenas campos definidos no DTO sao aceitos. Campos como tenant_id e created_by nunca vem do request |
| Denial of Service | Rate limiting + request size | Body maximo: 10MB. Timeout: 60s. Rate limits por tenant, IP e globais |
| Path Traversal | Validacao de file_key | File keys sao geradas pelo servidor (UUID-based). Nomes de arquivo do usuario sao apenas metadados, nunca usados como path |

### Validacao de Upload de Arquivos

| Validacao | Regra | Resposta em Violacao |
|-----------|-------|---------------------|
| Content-Type header | Deve ser image/jpeg, image/png ou application/pdf | 400 Bad Request: "Tipo de arquivo nao suportado" |
| Magic bytes | Primeiros bytes do arquivo devem corresponder ao Content-Type declarado | 400 Bad Request: "Content-Type nao corresponde ao conteudo do arquivo" |
| Tamanho maximo | 10 MB por arquivo | 413 Payload Too Large |
| Nome do arquivo | Max 255 caracteres, sem caracteres especiais (regex: `^[a-zA-Z0-9._-]+$`) | 400 Bad Request: "Nome de arquivo invalido" |
| Antivirus (producao) | Scan ClamAV antes de persistir | 422 Unprocessable Entity: "Arquivo rejeitado pela verificacao de seguranca" |

## Audit Logging

Todas as operacoes de escrita na GEOAPI sao registradas em tabela de auditoria para rastreabilidade e compliance LGPD.

### Estrutura do Registro de Auditoria

| Campo | Tipo | Descricao |
|-------|------|-----------|
| Id | UUID | Identificador unico do log |
| UserId | UUID | ID do usuario que realizou a acao (claim `sub` do JWT) |
| TenantId | UUID | ID do tenant |
| Action | String | Tipo de acao: CREATE, UPDATE, DELETE, APPROVE, REJECT, LOGIN, SYNC |
| EntityType | String | Tipo da entidade: Unit, Holder, Community, Document, LegitimationRequest |
| EntityId | UUID | ID da entidade afetada |
| OldValues | JSONB | Estado anterior do registro (null para CREATE) |
| NewValues | JSONB | Estado novo do registro (null para DELETE) |
| Timestamp | DateTime | Momento exato da acao (UTC) |
| IpAddress | String | IP do request (X-Forwarded-For em producao atras de proxy) |
| UserAgent | String | User-Agent do request (identifica app mobile vs navegador) |
| CorrelationId | UUID | X-Request-Id para correlacao com logs de aplicacao |

### Implementacao

O audit logging e implementado via interceptor do EF Core (`SaveChangesInterceptor`) que captura automaticamente todas as mudancas antes do commit. O interceptor compara os estados `Original` e `Current` de cada entidade rastreada para gerar `OldValues` e `NewValues`.

### Retencao e Acesso

| Parametro | Valor | Justificativa |
|-----------|-------|---------------|
| Retencao minima | 2 anos | Compliance LGPD (Art. 37) |
| Retencao maxima | 5 anos | Preservar historico para disputas juridicas |
| Acesso de leitura | Roles ADMIN e SUPER_ADMIN | Via endpoint /api/admin/audit-logs |
| RLS na tabela | Sim (por tenant) | Admin ve apenas logs do proprio tenant |
| Indexacao | Indices em UserId, EntityType, EntityId, Timestamp | Performance de consultas por usuario, entidade e periodo |
| Imutabilidade | Sem UPDATE ou DELETE permitido | Policy RLS restringe a INSERT only para a tabela audit_logs |

### Exemplos de Registros

**Criacao de unidade:**

```json
{
  "id": "log-uuid-001",
  "userId": "user-uuid-abc",
  "tenantId": "tenant-uuid-xyz",
  "action": "CREATE",
  "entityType": "Unit",
  "entityId": "unit-uuid-new",
  "oldValues": null,
  "newValues": {
    "code": "UNI-2024-00001",
    "status": "DRAFT",
    "area": 150.5,
    "observation": "Lote na esquina"
  },
  "timestamp": "2024-03-15T14:30:00Z",
  "ipAddress": "192.168.1.100",
  "userAgent": "REURBCAD/1.0 (Android 14)",
  "correlationId": "req-uuid-789"
}
```

**Aprovacao de unidade:**

```json
{
  "id": "log-uuid-002",
  "userId": "manager-uuid-def",
  "tenantId": "tenant-uuid-xyz",
  "action": "APPROVE",
  "entityType": "Unit",
  "entityId": "unit-uuid-new",
  "oldValues": {
    "status": "PENDING"
  },
  "newValues": {
    "status": "APPROVED",
    "approved_by": "manager-uuid-def",
    "approved_at": "2024-03-16T10:00:00Z"
  },
  "timestamp": "2024-03-16T10:00:00Z",
  "ipAddress": "200.100.50.25",
  "userAgent": "Mozilla/5.0 (GEOWEB)",
  "correlationId": "req-uuid-901"
}
```