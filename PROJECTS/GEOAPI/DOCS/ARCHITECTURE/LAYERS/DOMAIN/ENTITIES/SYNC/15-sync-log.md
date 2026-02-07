---
type: leaf
status: approved
updated: 2026-02-07
---

# SyncLog

Entidade representando registro de cada operacao de sincronizacao entre o app mobile REURBCAD e o servidor GEOAPI. Rastreia CREATE, UPDATE e DELETE enviados pelo dispositivo, com deteccao automatica de conflitos via versionamento otimista. Herda de BaseEntity fornecendo auditoria temporal.

## Papel no Dominio

O SyncLog e a trilha de rastreabilidade da sincronizacao offline. Cada operacao enviada pelo app e registrada com payload completo, timestamps do client e servidor, e resultado da operacao. Quando conflito e detectado (versao do registro no servidor diferente da versao que o client usou como base), os dados conflitantes sao armazenados para resolucao manual ou automatica.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| UserId | Guid | nao | UUID do usuario que sincronizou. |
| EntityType | string | nao | Tipo da entidade: UNIT, HOLDER, DOCUMENT, COMMUNITY. |
| EntityId | Guid | nao | ID da entidade sincronizada. |
| Operation | string | nao | Tipo de operacao: CREATE, UPDATE, DELETE. |
| Payload | JsonDocument | nao | Dados completos da operacao em formato JSON. |
| SyncedAt | DateTime | nao | Quando a sync foi processada no servidor. |
| ClientTimestamp | DateTime | nao | Timestamp do client no momento da operacao local. |
| ServerTimestamp | DateTime | nao | Timestamp do servidor ao processar. |
| ConflictResolved | bool | nao | Se houve conflito e foi resolvido. Default false. |

## Relacionamentos

Vinculado a um Tenant e a um usuario. Referencia uma entidade via EntityType e EntityId.

## Invariantes de Negocio

Append-only para fins de rastreabilidade. Registros nao sao atualizados apos criacao exceto o campo ConflictResolved que pode mudar de false para true apos resolucao.
