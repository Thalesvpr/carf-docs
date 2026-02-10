---
type: leaf
status: review
updated: 2026-02-08
---

# Auth Key Commands

Os commands de chaves de API representam operacoes de criacao e revogacao de chaves utilizadas pelo plugin QGIS (GEOGIS) para autenticacao sem fluxo OAuth2 interativo.

---

## CreateAuthKeyCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Name | string | sim | Nome descritivo da chave (ex: "QGIS Desktop") |

O handler gera UUID v4 como valor da chave, define expiracao em 30 dias a partir da criacao e persiste o registro vinculado ao usuario autenticado e tenant do contexto. O response retorna id, name, key (UUID v4 exibido uma unica vez nesta response), expiresAt e createdAt. O valor da chave nunca mais sera retornado em consultas posteriores por seguranca, sendo armazenado como hash no banco.

Erros possiveis: 401 quando usuario nao esta autenticado.

---

## RevokeAuthKeyCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| KeyId | Guid | sim | Identificador da chave a revogar |

O handler localiza a chave pelo Id e verifica que pertence ao usuario autenticado. Executa remocao logica invalidando a chave para uso futuro. Retorna 204 em caso de sucesso ou 404 se a chave nao existe ou nao pertence ao usuario.
