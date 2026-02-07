---
type: leaf
status: approved
updated: 2026-02-07
---

# ApiKey

Entidade representando chave de API de longa duracao para autenticar o plugin QGIS (GEOGIS) na GEOAPI sem exigir sessao interativa OAuth2. A chave e vinculada a um Account e herda suas permissoes incluindo restricoes de tenant e community_authorization. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

A ApiKey permite que analistas usem o plugin QGIS para acessar dados espaciais da GEOAPI sem manter login ativo no navegador. A chave e um UUID v4 gerado pelo servidor, exibido uma unica vez ao usuario e armazenado como hash SHA-256 no banco. Detalhes completos do ciclo de vida estao documentados em CONCEPTS/05-authentication-key.md.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| AccountId | Guid | nao | FK para Account do usuario que criou a chave. |
| TenantId | Guid | nao | Tenant vinculado. Herdado do Account no momento da criacao. |
| KeyHash | string | nao | SHA-256 hexadecimal da chave original. Unico. A chave original nunca e armazenada. |
| Name | string | nao | Nome descritivo fornecido pelo usuario (exemplo: "QGIS Desktop - Notebook Joao"). Maximo 200 caracteres. |
| ExpiresAt | DateTime | nao | Data de expiracao. 30 dias apos criacao por padrao. |
| LastUsedAt | DateTime | sim | Ultima vez que a chave foi usada. Atualizada a cada request autenticado. |
| IsRevoked | bool | nao | Indica se a chave foi revogada. Default false. |
| RevokedAt | DateTime | sim | Quando foi revogada. |
| CreatedAt | DateTime | nao | Data de criacao. |

## Relacionamentos

Pertence a um Account (obrigatorio). Vinculada a um Tenant (obrigatorio).

## Invariantes de Negocio

KeyHash unico globalmente. Chave expirada ou revogada nao pode ser reativada; o usuario deve gerar nova chave. Troca de senha no Keycloak revoga automaticamente todas as chaves ativas do Account. Rate limit de 100 requisicoes por minuto por chave.
