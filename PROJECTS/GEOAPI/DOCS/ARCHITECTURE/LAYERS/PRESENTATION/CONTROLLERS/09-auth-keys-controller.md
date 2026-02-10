---
type: leaf
status: review
updated: 2026-02-08
---

# Auth Keys Controller

O AuthKeysController gerencia chaves de API utilizadas pelo plugin QGIS (GEOGIS) para autenticacao sem fluxo OAuth2 interativo. A rota base e /api/auth-keys. Todos os endpoints requerem role analyst ou superior.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/auth-keys | Gerar chave de API | 201 | 401 | analyst+ |
| GET | /api/auth-keys | Listar chaves ativas | 200 | - | analyst+ |
| DELETE | /api/auth-keys/{id} | Revogar chave | 204 | 404 | analyst+ |

## Comportamento

O endpoint de criacao recebe body com name (string descritiva como "QGIS Desktop") e despacha CreateAuthKeyCommand. O handler gera UUID v4 como valor da chave, define expiracao em 30 dias a partir da criacao e persiste o registro. O response retorna id, name, key (UUID v4 exibido uma unica vez), expiresAt e createdAt. O campo key nunca mais sera retornado apos esta response por seguranca. O endpoint de listagem retorna array de objetos com id, name, createdAt, expiresAt e lastUsedAt, sem incluir o valor da chave. O endpoint de revogacao executa soft delete ou remocao logica do registro, retornando 204 ou 404 se a chave nao existe.

## Autorizacao

Todos os endpoints requerem role analyst, manager, admin ou super-admin. Cada usuario pode gerenciar apenas suas proprias chaves, filtradas por created_by no handler.
