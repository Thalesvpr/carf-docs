---
type: leaf
status: review
updated: 2026-02-08
---

# Community Aggregate

Agregado de dominio estabelecendo Community como aggregate root, controlando boundaries de consistencia e enforcement de invariantes para o grupo de entidades relacionadas a assentamento ou comunidade em processo de regularizacao fundiaria.

## Raiz do Agregado

Community e a entidade raiz que coordena todas as mudancas dentro do boundary do agregado. Estende BaseAggregateRoot herdando Domain Events, auditoria temporal e concorrencia otimista.

## Componentes Internos

| Componente | Cardinalidade | Descricao |
|------------|---------------|-----------|
| Block | 1:N | Quadras urbanas subdividindo a community geograficamente. Geometria deve estar contida no boundary da community. |
| CommunityAuthorization | 1:N | Controle de acesso granular. Pode ser atribuida a Team (team_id) ou Account individual (account_id), mutuamente exclusivos. |
| Document | 1:N | Anexos polimorficos vinculados a community. EntityType COMMUNITY. |
| Annotation | 1:N | Anotacoes e issues relacionados a community. |

## Invariantes

| Invariante | Descricao |
|------------|-----------|
| Autorizacao ativa | Community deve ter ao menos uma CommunityAuthorization ativa, prevenindo communities orfas inacessiveis. |
| Contencao espacial | Geometria de todos os Blocks filhos deve estar contida no boundary da Community. |
| Nome unico | Nome da Community deve ser unico dentro do tenant. |
| Municipio valido | Campo municipality deve ser nome valido de municipio brasileiro ou codigo IBGE. |
| Protecao contra exclusao | Community nao pode ser deletada se contem Units ativas. Exige migracao ou arquivamento previo. |

## Operacoes da Raiz

| Operacao | Descricao |
|----------|-----------|
| CreateCommunity(dados) | Valida dados basicos, cria community e gera primeira CommunityAuthorization para Account criador. Dispara CommunityCreatedEvent. |
| AddBlock(code, boundary) | Cria Block filho validando que geometria esta dentro do boundary da community e code e unico. Dispara BlockAddedEvent. |
| UpdateBoundary(newGeometry) | Modifica geometria validando que nova geometria contem todos Blocks existentes. Dispara CommunityBoundaryChangedEvent. |
| GrantAccess(teamOrAccountId, permissions) | Cria CommunityAuthorization. Apenas ADMIN ou MANAGER pode conceder. Dispara AccessGrantedEvent. |
| RevokeAccess(authorizationId) | Remove CommunityAuthorization validando que nao e a ultima ativa. Dispara AccessRevokedEvent. |
| Archive() | Marca community como arquivada apos validar que todas Units foram concluidas ou canceladas. Dispara CommunityArchivedEvent. |

## Eventos de Dominio

| Evento | Contexto |
|--------|----------|
| CommunityCreatedEvent | Ao criar community. Permite inicializacao de recursos (pastas S3, indices de busca). |
| CommunityBoundaryChangedEvent | Ao modificar geometria. Permite recalculo de estatisticas espaciais. |
| AccessGrantedEvent | Ao conceder autorizacao. Notifica usuarios sobre novo acesso. |
| AccessRevokedEvent | Ao remover autorizacao. Permite limpeza de caches de permissao. |
| BlockAddedEvent | Ao adicionar quadra. Atualiza indices espaciais e dashboards. |
| CommunityArchivedEvent | Ao arquivar. Permite limpeza de recursos temporarios. |

## Motivacao do Boundary

O boundary do agregado foi escolhido por coesao funcional (Community, Blocks e CommunityAuthorizations sao fortemente acoplados), consistencia transacional (modificacoes precisam ser atomicas para integridade espacial e permissoes) e performance (agregado pequeno sem trazer Units associadas que podem ser milhares).
