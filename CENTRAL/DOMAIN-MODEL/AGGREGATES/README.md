# Aggregates - Fronteiras de Consistência

Aggregates são clusters de entidades e value objects tratados como unidade coesa para garantir invariantes de negócio onde aggregate root controla acesso e coordena mudanças de estado interno assegurando consistência transacional e integridade de dados dentro de fronteiras bem definidas.

## Aggregate Roots (3 principais)

### [01-unit-aggregate.md](./01-unit-aggregate.md) - Unit Aggregate
**Aggregate Root:** Unit (unidade habitacional)

**Boundaries (fronteira):**
- Unit (root)
- UnitHolder (relacionamento N:N com Holder)
- Documents (anexos polimórficos)
- Annotations (anotações polimórficas)
- SurveyPoints (pontos topográficos vinculados)

**Invariantes garantidos:**
- Unit deve ter ao menos um Holder antes de status APPROVED
- Soma de ownership_percentage dos UnitHolders ≤ 100%
- Exatamente um UnitHolder com is_primary_holder = true
- Geometria válida sem auto-interseções quando preenchida
- Área > 0 e dentro de limites por modalidade REURB
- Status transitions seguem workflow permitido (state machine)

**Operações principais:**
- AddHolder(), RemoveHolder(), UpdateOwnership()
- AttachDocument(), RemoveDocument()
- AddAnnotation(), ResolveAnnotation()
- UpdateGeometry(), RecalculateArea()
- ChangeStatus() com validação de transições

**Eventos de domínio:**
- UnitCreatedEvent, UnitApprovedEvent, UnitRejectedEvent
- HolderAddedEvent, OwnershipChangedEvent
- GeometryUpdatedEvent, StatusChangedEvent

---

### [02-community-aggregate.md](./02-community-aggregate.md) - Community Aggregate
**Aggregate Root:** Community (comunidade/assentamento)

**Boundaries (fronteira):**
- Community (root)
- Blocks (quadras urbanas)
- CommunityAuthorizations (permissões de acesso Team/Account)
- Documents (anexos da comunidade)
- Annotations (anotações da comunidade)

**Invariantes garantidos:**
- Community deve ter ao menos uma CommunityAuthorization (não pode ficar órfã)
- Block geometries devem estar dentro de Community boundary quando definido
- Município (municipio field) obrigatório para isolamento geográfico
- CommunityAuthorization: OU team_id OU account_id (não ambos nem nenhum)

**Operações principais:**
- AddBlock(), RemoveBlock()
- GrantAccess(), RevokeAccess()
- UpdateBoundary(), RecalculateArea()
- AssignToTeam(), UnassignFromTeam()

**Eventos de domínio:**
- CommunityCreatedEvent, CommunityUpdatedEvent
- AccessGrantedEvent, AccessRevokedEvent
- BlockAddedEvent, BlockRemovedEvent
- BoundaryChangedEvent

---

### [03-legitimation-request-aggregate.md](./03-legitimation-request-aggregate.md) - LegitimationRequest Aggregate
**Aggregate Root:** LegitimationRequest (processo de legitimação fundiária)

**Boundaries (fronteira):**
- LegitimationRequest (root)
- LegitimationResponses (pareceres técnicos/jurídicos)
- LegitimationCertificate (certidão oficial)
- DescriptiveMemorial (memorial descritivo técnico)
- LegitimationPlan (planta técnica gráfica)
- Contestations (contestações de terceiros)
- Documents (documentação do processo)

**Invariantes garantidos:**
- Não aprovar sem documentação obrigatória conforme modalidade (REURB-S vs REURB-E)
- Não emitir certidão antes de status APPROVED
- Contestations devem estar resolvidas antes de APPROVED
- DescriptiveMemorial e LegitimationPlan obrigatórios e approved antes de conclusão
- Protocol_number único por tenant
- Deadline de 120 dias contados de submitted_at conforme Lei 13465/2017
- Status transitions seguem workflow 11 estados (state machine rigorosa)

**Operações principais:**
- Submit(), Approve(), Reject()
- AddResponse(), ResolveResponse()
- IssueCertificate(), RevokeCertificate()
- HandleContestation(), ResolveContestation()
- AttachMemorial(), AttachPlan()
- TransitionStatus() com validação e role-based permissions

**Eventos de domínio:**
- RequestSubmittedEvent, RequestApprovedEvent, RequestRejectedEvent
- ResponseAddedEvent, ContestationReceivedEvent, ContestationResolvedEvent
- CertificateIssuedEvent, CertificateRevokedEvent
- DeadlineApproachingEvent (15 dias antes de vencimento)
- StatusTransitionedEvent

---

## Princípios de Aggregates

**Transactional Consistency:** Mudanças dentro do aggregate são atômicas e consistentes

**Eventual Consistency:** Entre aggregates, consistência eventual via eventos de domínio

**Aggregate Root:** Único ponto de acesso externo, coordena todas operações internas

**Small Aggregates:** Aggregates pequenos melhoram concorrência e performance

**Reference by ID:** Aggregates referenciam outros aggregates apenas por ID, não por objeto completo

**Invariants Enforcement:** Aggregate root garante que invariantes de negócio sempre são respeitados

---

**Última atualização:** 2026-01-10
