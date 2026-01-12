# Domain Events

Domain events representam fatos negócio significativos ocorridos sistema disparados aggregate roots após mudanças estado bem-sucedidas permitindo comunicação desacoplada entre aggregates implementação side effects assíncronos notificações invalidação cache atualização métricas integração sistemas externos sendo utilizados modelar fatos negócio outras partes sistema precisam saber disparar side effects sem acoplar lógica aggregate implementar eventual consistency entre aggregates seguindo padrão onde events despachados após SaveChanges garantindo transação commitada executando sequência aggregate executa ação modificando estado interno adiciona event collection interna preservando ordem cronológica repository persiste aggregate SaveChanges commita transação event dispatcher publica events handlers executando lógica assíncrona fora transação original prevenindo rollback cascata com handlers executando side effects notificações email SMS in-app invalidação cache queries métricas contadores dashboards auditoria logs timeline integrações webhooks sistemas externos validações assíncronas background jobs garantindo idempotência events podem reprocessados retry mensageria handlers devem deduplicar por event_id verificar side effect já executado usar operações naturalmente idempotentes SET ao invés INCREMENT.

Eventos organizados por aggregate root sendo Unit aggregate emitindo 5 eventos (UnitCreated HolderLinked HolderUnlinked UnitStatusChanged DocumentUploaded) durante lifecycle unidade habitacional workflow validação cadastro titulares documentos anexos, Community aggregate emitindo 6 eventos (CommunityCreated CommunityBoundaryChanged AccessGranted AccessRevoked BlockAdded CommunityArchived) gestão comunidades autorizações acesso subdivisão territorial arquivamento regularização concluída cancelada, e LegitimationRequest aggregate emitindo 8 eventos (RequestSubmitted ResponseAdded RequestApproved CertificateIssued ContestationReceived DeadlineApproaching RequestRejected CorrectionRequested) workflow legitimação fundiária Lei 13465/2017 processo submetido prazo 120 dias atribuir analista parecer técnico jurídico aprovação deferimento emissão certidão documento oficial QR code cartório contestação terceiro pausar workflow alerta prazos rejeição indeferimento motivos fundamentados correções solicitadas pausar até resubmissão.

## Conceito Base

**[00-domain-event.md](./00-domain-event.md)** - Interface padrões domain events lifecycle propriedades base handlers subscribers dispatch após SaveChanges idempotência

## Unit Aggregate Events

1. **[01-unit-created-event.md](./01-unit-created-event.md)** - Unidade habitacional criada DRAFT inicial
2. **[02-holder-linked-event.md](./02-holder-linked-event.md)** - Titular vinculado UnitHolder ownership estabelecido
3. **[03-holder-unlinked-event.md](./03-holder-unlinked-event.md)** - Titular desvinculado ownership removido
4. **[04-unit-status-changed-event.md](./04-unit-status-changed-event.md)** - Status workflow alterado transições DRAFT PENDING APPROVED
5. **[05-document-uploaded-event.md](./05-document-uploaded-event.md)** - Documento foto anexado validação thumbnails checklist

## Community Aggregate Events

6. **[06-community-created-event.md](./06-community-created-event.md)** - Comunidade assentamento criado área regularização estabelecida
7. **[07-community-boundary-changed-event.md](./07-community-boundary-changed-event.md)** - Perímetro espacial alterado validar units recalcular área
8. **[08-access-granted-event.md](./08-access-granted-event.md)** - Acesso concedido CommunityAuthorization Team Account
9. **[09-access-revoked-event.md](./09-access-revoked-event.md)** - Acesso revogado limpeza dados offline invalidar cache
10. **[10-block-added-event.md](./10-block-added-event.md)** - Quadra urbana adicionada subdivisão territorial
11. **[11-community-archived-event.md](./11-community-archived-event.md)** - Comunidade arquivada regularização concluída cancelada

## LegitimationRequest Aggregate Events

12. **[12-request-submitted-event.md](./12-request-submitted-event.md)** - Processo submetido início prazo 120 dias atribuir analista
13. **[13-response-added-event.md](./13-response-added-event.md)** - Parecer técnico jurídico adicionado análise registrada
14. **[14-request-approved-event.md](./14-request-approved-event.md)** - Processo aprovado regularização deferida
15. **[15-certificate-issued-event.md](./15-certificate-issued-event.md)** - Certidão emitida documento oficial QR code cartório
16. **[16-contestation-received-event.md](./16-contestation-received-event.md)** - Contestação recebida terceiro opõe pausar workflow
17. **[17-deadline-approaching-event.md](./17-deadline-approaching-event.md)** - Prazo aproximando alerta 120 dias priorizar análise
18. **[18-request-rejected-event.md](./18-request-rejected-event.md)** - Processo rejeitado indeferido motivos fundamentados
19. **[19-correction-requested-event.md](./19-correction-requested-event.md)** - Correções solicitadas pausar até resubmissão

---

**Última atualização:** 2026-01-11
