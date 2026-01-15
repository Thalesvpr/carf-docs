# EVENTS

Domain events representam fatos de negócio significativos ocorridos no sistema. São disparados pelos aggregate roots após mudanças de estado bem-sucedidas, permitindo comunicação desacoplada entre aggregates e execução de side effects assíncronos como notificações, invalidação de cache e integrações.

Os eventos são organizados por aggregate. O Unit aggregate emite eventos durante o ciclo de vida da unidade habitacional, como criação, vinculação de titulares e mudanças de status. O Community aggregate emite eventos de gestão territorial como alteração de perímetro e concessão de acesso. O LegitimationRequest aggregate emite eventos do workflow de legitimação conforme Lei 13.465/2017.

## Conceito Base

- **[00-domain-event.md](./00-domain-event.md)** - Interface e padrões de domain events

## Unit Aggregate

- **[01-unit-created-event.md](./01-unit-created-event.md)** - Unidade criada em status DRAFT
- **[02-holder-linked-event.md](./02-holder-linked-event.md)** - Titular vinculado à unidade
- **[03-holder-unlinked-event.md](./03-holder-unlinked-event.md)** - Titular desvinculado
- **[04-unit-status-changed-event.md](./04-unit-status-changed-event.md)** - Status alterado no workflow
- **[05-document-uploaded-event.md](./05-document-uploaded-event.md)** - Documento anexado

## Community Aggregate

- **[06-community-created-event.md](./06-community-created-event.md)** - Comunidade criada
- **[07-community-boundary-changed-event.md](./07-community-boundary-changed-event.md)** - Perímetro alterado
- **[08-access-granted-event.md](./08-access-granted-event.md)** - Acesso concedido
- **[09-access-revoked-event.md](./09-access-revoked-event.md)** - Acesso revogado
- **[10-block-added-event.md](./10-block-added-event.md)** - Quadra adicionada
- **[11-community-archived-event.md](./11-community-archived-event.md)** - Comunidade arquivada

## LegitimationRequest Aggregate

- **[12-request-submitted-event.md](./12-request-submitted-event.md)** - Processo submetido
- **[13-response-added-event.md](./13-response-added-event.md)** - Parecer adicionado
- **[14-request-approved-event.md](./14-request-approved-event.md)** - Processo aprovado
- **[15-certificate-issued-event.md](./15-certificate-issued-event.md)** - Certidão emitida
- **[16-contestation-received-event.md](./16-contestation-received-event.md)** - Contestação recebida
- **[17-deadline-approaching-event.md](./17-deadline-approaching-event.md)** - Prazo aproximando
- **[18-request-rejected-event.md](./18-request-rejected-event.md)** - Processo rejeitado
- **[19-correction-requested-event.md](./19-correction-requested-event.md)** - Correções solicitadas

---

**Última atualização:** 2026-01-14
