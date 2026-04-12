---
type: leaf
status: active
updated: 2026-02-07
---

# Unit Commands

Os commands CQRS de unidades representam todas as operacoes de escrita no agregado Unit. Cada command e um record imutavel que implementa IRequest do MediatR, retornando Result ou Result tipado. Os handlers coordenam validacoes de dominio, persistencia via repositorio e emissao de domain events. Todas as operacoes respeitam o isolamento por tenant extraido do contexto de autenticacao.

---

## CreateUnitCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| CommunityId | Guid | sim | Comunidade a que a unidade pertence |
| Address | AddressDto | sim | Endereco completo com street, number, complement, neighborhood, city, state e zipCode |
| Geometry | GeometryDto | sim | Poligono GeoJSON com type Polygon e coordinates em WGS84 |
| Photos | List de Guid | nao | Lista de UUIDs referenciando documentos ja uploaded |

O handler executa quatro passos sequenciais. Primeiro, valida a geometria via IGeometryValidator verificando que o poligono e valido, fechado e nao auto-intersectante. Segundo, consulta o repositorio para verificar sobreposicao com unidades existentes na mesma comunidade utilizando ST_Intersects do PostGIS. Terceiro, cria a entidade Unit via factory method passando Address, Geometry, CommunityId e TenantId do contexto, gerando automaticamente o codigo no formato UNI-AAAA-NNNNN. Quarto, persiste via repositorio, comita a unidade de trabalho e retorna UnitDto mapeado via AutoMapper.

Emite o domain event UnitCreatedEvent contendo o Id da unidade e CommunityId. Em caso de erro, retorna VALIDATION_ERROR para geometria invalida ou OVERLAP_ERROR para sobreposicao espacial.

---

## UpdateUnitCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Id | Guid | sim | Identificador da unidade |
| Address | AddressDto | nao | Endereco atualizado (atualizacao parcial) |
| Geometry | GeometryDto | nao | Nova geometria (recalcula area e centroide) |

O handler carrega a unidade pelo Id, verifica que o status permite edicao (DRAFT ou REQUIRES_CHANGES) e aplica as alteracoes fornecidas. Quando a geometria e alterada, o handler recalcula a area via ST_Area e o centroide via ST_Centroid. Incrementa o campo version para controle de concorrencia otimista. Se a unidade estiver em status que impede edicao, retorna erro UNIT_LOCKED com HTTP 403.

Emite UnitUpdatedEvent com Id, campos alterados e version anterior. Cenario de erro: concorrencia otimista falha quando version no banco diverge do esperado, retornando CONCURRENCY_CONFLICT.

---

## DeleteUnitCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade a excluir |

O handler carrega a unidade e verifica que o status e DRAFT. Unidades em qualquer outro status nao podem ser excluidas, retornando erro NOT_DRAFT. Executa soft delete preenchendo o campo deleted_at com o timestamp atual. Remove tambem os vinculos em unit_holders associados via cascade.

Emite UnitDeletedEvent com Id e CommunityId. Nao emite evento quando a unidade nao e encontrada, retornando 404.

---

## SubmitUnitCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade a submeter |

O handler carrega a unidade com eager loading dos titulares vinculados. Verifica duas pre-condicoes: a unidade deve estar em status DRAFT e deve ter ao menos um titular vinculado com is_primary igual a true. Quando ambas sao satisfeitas, transiciona o status para PENDING_ANALYSIS via metodo de dominio da entidade Unit.

Emite UnitSubmittedEvent com Id, CommunityId e lista de holder IDs vinculados. Cenarios de erro: NO_HOLDER quando nenhum titular primario esta vinculado, NOT_DRAFT quando o status atual nao permite submissao.

---

## ApproveUnitCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade |
| Justification | string | sim | Justificativa da aprovacao com minimo 10 caracteres |

O handler verifica que o usuario autenticado possui role manager ou superior. Carrega a unidade e confirma que o status e PENDING_ANALYSIS ou IN_REVIEW. Transiciona para APPROVED registrando o manager_id e a justificativa. O campo updated_by e atualizado com o Id do aprovador.

Emite UnitApprovedEvent com Id, ApproverId e Justification. Cenarios de erro: NOT_AUTHORIZED quando o usuario nao tem role suficiente, INVALID_STATUS quando a unidade nao esta em status aprovavel.

---

## RejectUnitCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade |
| Reason | string | sim | Motivo da rejeicao com minimo 50 caracteres |

O handler verifica role manager ou superior do usuario autenticado. Carrega a unidade e confirma status PENDING_ANALYSIS ou IN_REVIEW. Transiciona para REJECTED registrando o motivo completo. O titular primario pode ser notificado via NotificationHub sobre a rejeicao.

Emite UnitRejectedEvent com Id, RejecterId e Reason. Cenarios de erro identicos ao ApproveUnitCommand quanto a autorizacao e status.

---

## LinkHolderCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade |
| HolderId | Guid | sim | Identificador do titular |
| RelationshipType | string | sim | PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR ou HERDEIRO |
| OwnershipPercentage | decimal | condicional | Percentual de propriedade, obrigatorio quando tipo e PROPRIETARIO |
| IsPrimary | bool | nao | Define titular como principal. Default false |

O handler valida que o titular existe e pertence ao mesmo tenant. Verifica que o par (UnitId, HolderId) nao existe em unit_holders para impedir duplicidade. Quando o tipo e PROPRIETARIO, calcula a soma dos percentuais existentes e valida que a adicao nao excede 100 por cento. Quando IsPrimary e true, verifica que nao existe outro titular primario para a unidade.

Emite HolderLinkedEvent com UnitId, HolderId e RelationshipType. Cenarios de erro: DUPLICATE para vinculo ja existente, PERCENTAGE_EXCEEDED quando a soma ultrapassa 100, MULTIPLE_PRIMARY quando ja existe titular primario.

---

## UnlinkHolderCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| UnitId | Guid | sim | Identificador da unidade |
| HolderId | Guid | sim | Identificador do titular a desvincular |

O handler localiza o registro em unit_holders pelo par (UnitId, HolderId) e o remove. Se o titular removido era o primario (is_primary true), o handler nao promove automaticamente outro titular, deixando a unidade sem primario ate que o usuario defina um novo.

Emite HolderUnlinkedEvent com UnitId e HolderId. Retorna 204 em caso de sucesso ou 404 se o vinculo nao existe.
