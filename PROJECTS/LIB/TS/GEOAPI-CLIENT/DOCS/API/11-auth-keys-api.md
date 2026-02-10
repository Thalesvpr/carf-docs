---
type: leaf
status: review
updated: 2026-02-08
---

# Auth Keys API - Gerenciamento de Chaves de API

A Auth Keys API permite criacao e gerenciamento de chaves de API para integracao server-to-server, usadas principalmente pelo plugin GEOGIS do QGIS. Acessada via propriedade authKeys da instancia GeoApiClient. Tipo ApiKey importado de @carf/tscore/types conforme [03-types-relationships](../../TSCORE/DOCS/API/03-types-relationships.md). Endpoints conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| POST | /api/auth-keys | Gerar chave de API | 201 | 401 | analyst+ |
| GET | /api/auth-keys | Listar chaves ativas | 200 | - | analyst+ |
| DELETE | /api/auth-keys/{id} | Revogar chave | 204 | 404 | analyst+ |

## create (POST /api/auth-keys)

Cria nova chave de API. Body contem apenas name como string descritiva (por exemplo "QGIS Desktop" ou "Script de importacao"). A chave completa (UUID v4) e retornada apenas uma vez nesta response e nunca mais sera exibida; o usuario deve copia-la imediatamente.

Response retorna ApiKeyCreatedResponse:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| id | string | UUID identificador da chave |
| name | string | Nome descritivo informado na criacao |
| key | string | UUID v4 da chave, exibido apenas uma vez |
| expiresAt | string | ISO 8601 timestamp de expiracao (30 dias apos criacao) |
| createdAt | string | ISO 8601 timestamp de criacao |

Restrito a roles analyst ou superior.

## list (GET /api/auth-keys)

Lista chaves ativas do tenant. Sem parametros. Retorna array de ApiKey com id, name, createdAt, expiresAt e lastUsedAt. O campo key nunca e incluido na listagem por seguranca. Restrito a roles analyst ou superior.

## revoke (DELETE /api/auth-keys/{id})

Revoga chave de API imediatamente. Aceita id string. Retorna void (204 No Content). Apos revogacao, qualquer requisicao usando esta chave recebe 401 Unauthorized. Lanca NotFoundError 404 se a chave nao existir. Restrito a roles analyst ou superior.
