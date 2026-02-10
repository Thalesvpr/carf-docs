---
type: leaf
status: review
updated: 2026-02-08
---

# Unit Aggregate

Agregado de dominio tendo Unit como raiz, controlando consistencia transacional da unidade habitacional e suas entidades fortemente relacionadas conforme padrao DDD de bounded consistency.

## Raiz do Agregado

Unit e a entidade raiz que coordena todas as mudancas dentro do agregado, garantindo invariantes de negocio. Estende BaseAggregateRoot, herdando suporte a Domain Events e controle de concorrencia otimista via RowVersion.

## Componentes Internos

| Componente | Cardinalidade | Descricao |
|------------|---------------|-----------|
| UnitHolder | 1:N | Relacionamentos N:N com Holders via tabela unit_holders. Armazena tipo de vinculo (PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR, HERDEIRO) e percentual de propriedade. |
| Document | 1:N | Anexos polimorficos vinculados a unidade (fotos, plantas, PDFs). EntityType UNIT, EntityId igual ao Unit.Id. |
| Annotation | 1:N | Observacoes e notas vinculadas a unidade. EntityType UNIT. |

## Invariantes

| Invariante | Descricao |
|------------|-----------|
| Holder obrigatorio para aprovacao | Unit deve ter ao menos um Holder vinculado antes de transicionar para status APPROVED. |
| Soma de propriedade | Soma de ownership_percentage de todos UnitHolder com tipo PROPRIETARIO nao pode exceder 100%. |
| Tipo de documento | Documents vinculados devem ter EntityType igual a UNIT e EntityId igual ao Unit.Id. |
| Geometria contida | Boundary, se preenchido, deve estar dentro ou proximo do perimetro da Community. |
| Codigo unico | Code deve ser unico por tenant no formato UNI-AAAA-NNNNN. |

## Operacoes da Raiz

| Operacao | Descricao |
|----------|-----------|
| LinkHolder(holderId, type, percentage) | Adiciona UnitHolder com validacoes de tipo e percentual. Dispara HolderLinkedEvent. |
| UnlinkHolder(holderId) | Remove vinculo verificando que nao deixa unidade sem holders se status e APPROVED. Dispara HolderUnlinkedEvent. |
| UploadDocument(type, file) | Cria Document anexo validando tipo e tamanho. Dispara DocumentUploadedEvent. |
| AddAnnotation(content, type) | Cria Annotation vinculada a unidade. |
| Approve() | Transiciona status para APPROVED com validacoes pre-aprovacao. Dispara UnitStatusChangedEvent. |
| Reject(reason) | Rejeita unidade com justificativa obrigatoria. Dispara UnitStatusChangedEvent. |
| RequestChanges(issues) | Solicita correcoes retornando status para REQUIRES_CHANGES. |

## Navegacao por Referencia

Unit referencia Community, Block e Plot por ID (CommunityId, BlockId, PlotId) sem carregar objetos completos, evitando agregados grandes. Queries podem fazer join para exibicao, mas mudancas nessas entidades ocorrem em seus proprios agregados.

## Eventos de Dominio

| Evento | Contexto |
|--------|----------|
| UnitCreatedEvent | Ao criar unidade. |
| HolderLinkedEvent | Ao vincular titular. |
| HolderUnlinkedEvent | Ao desvincular titular. |
| UnitStatusChangedEvent | Em transicoes de workflow (Approve, Reject, RequestChanges). |
| DocumentUploadedEvent | Ao anexar arquivo. |

## Persistencia

Repository carrega Unit com todas as colecoes internas em query unica usando eager loading. SaveChanges persiste mudancas em Unit, UnitHolder, Document e Annotation atomicamente. Concorrencia controlada por RowVersion em Unit detectando modificacoes concorrentes.
