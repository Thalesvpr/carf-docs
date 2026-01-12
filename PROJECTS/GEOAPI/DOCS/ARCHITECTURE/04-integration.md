# Integrações

GEOAPI integra com sistemas externos via Infrastructure Layer mantendo Domain Layer livre de dependências técnicas. Integrações principais incluem Keycloak OAuth2/OIDC autenticação crítica, PostgreSQL PostGIS persistência crítica, consumidores API GEOWEB REURBCAD ADMIN GEOGIS alta prioridade, Email Server notificações média prioridade, SMS Gateway alertas média prioridade, e File Storage S3 documentos alta prioridade.

Keycloak integration implementa autenticação OAuth2/OIDC onde frontend obtém token via Authorization Code flow com PKCE, GEOAPI valida JWT via middleware AddJwtBearer configurando Authority Audience ValidateIssuerSigningKey, claims extraídos incluem sub user_id preferred_username email realm_access.roles tenant_id, roles mapeados para policies Authorize attribute em Controllers, refresh tokens gerenciados frontend com silent refresh antes expiração. KeycloakAdminService para endpoints /api/admin/* usa client credentials flow com client_secret confidencial para CRUD usuários grupos roles via Keycloak Admin REST API.

PostgreSQL PostGIS integration implementa persistência geoespacial onde EF Core DbContext mapeia Entities para tabelas com Fluent API, PostGIS extension habilita tipos geometry geography para GeoPolygon GeoPoint, spatial indexes GiST otimizam queries ST_Within ST_Intersects ST_Distance, Row-Level Security policies CREATE POLICY tenant_isolation ON units USING tenant_id = current_setting app.tenant_id isolam dados automaticamente, connection pooling Npgsql gerencia conexões com min max pool size, migrations EF Core versionam schema com Up Down methods.

API consumers GEOWEB REURBCAD ADMIN GEOGIS conectam via REST JSON com autenticação Bearer JWT, rate limiting por tenant previne abuso, CORS configurado para origins específicos cada frontend, versionamento API via URL /api/v1/ permite evolução sem quebrar clientes, OpenAPI spec gerada automaticamente via Swashbuckle documenta endpoints para geração client TypeScript.

Serviços externos Email via SendGrid ou SMTP para notificações legitimação aprovada documentos pendentes, SMS via gateway HTTP para alertas urgentes, File Storage via S3-compatible MinIO ou AWS S3 para documentos fotos plantas com presigned URLs acesso temporário, todos implementam interface Domain IEmailService ISmsService IFileStorage permitindo mock em testes e troca implementação sem afetar Domain.

---

**Última atualização:** 2026-01-12
