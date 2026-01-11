# Domain Events

**Total:** 19 eventos + 1 conceito base

Domain events representam fatos de negócio significativos que ocorreram no sistema disparados por aggregate roots após mudanças de estado bem-sucedidas permitindo comunicação desacoplada entre aggregates e implementação de side effects assíncronos como notificações invalidação de cache atualização de métricas e integração com sistemas externos.

**Quando usar:** Ao modelar fatos de negócio que outras partes do sistema precisam saber, disparar side effects sem acoplar lógica ao aggregate, ou implementar eventual consistency entre aggregates.

---

## 📋 Conceito Base

**[00-domain-event.md](./00-domain-event.md)** - Interface e padrões de domain events, lifecycle, propriedades base, handlers subscribers, dispatch após SaveChanges, idempotência

---

## 🏘️ Unit Aggregate Events (5)

Events emitidos por Unit aggregate root durante lifecycle de unidade habitacional:

1. **[01-unit-created-event.md](./01-unit-created-event.md)** - Unidade habitacional criada (DRAFT inicial)
2. **[02-holder-linked-event.md](./02-holder-linked-event.md)** - Titular vinculado via UnitHolder (ownership estabelecido)
3. **[03-holder-unlinked-event.md](./03-holder-unlinked-event.md)** - Titular desvinculado (ownership removido)
4. **[04-unit-status-changed-event.md](./04-unit-status-changed-event.md)** - Status workflow alterado (DRAFT→PENDING→APPROVED etc)
5. **[05-document-uploaded-event.md](./05-document-uploaded-event.md)** - Documento/foto anexado (validação, thumbnails, checklist)

---

## 🌍 Community Aggregate Events (6)

Events emitidos por Community aggregate root durante gestão de comunidades:

6. **[06-community-created-event.md](./06-community-created-event.md)** - Comunidade/assentamento criado (área de regularização estabelecida)
7. **[07-community-boundary-changed-event.md](./07-community-boundary-changed-event.md)** - Perímetro espacial alterado (validar units dentro, recalcular área)
8. **[08-access-granted-event.md](./08-access-granted-event.md)** - Acesso concedido via CommunityAuthorization (Team ou Account)
9. **[09-access-revoked-event.md](./09-access-revoked-event.md)** - Acesso revogado (limpeza dados offline, invalidar cache)
10. **[10-block-added-event.md](./10-block-added-event.md)** - Quadra urbana adicionada (subdivisão territorial)
11. **[11-community-archived-event.md](./11-community-archived-event.md)** - Comunidade arquivada (regularização concluída ou cancelada)

---

## ⚖️ LegitimationRequest Aggregate Events (8)

Events emitidos por LegitimationRequest aggregate root durante workflow de legitimação fundiária Lei 13465/2017:

12. **[12-request-submitted-event.md](./12-request-submitted-event.md)** - Processo submetido (início prazo 120 dias, atribuir analista)
13. **[13-response-added-event.md](./13-response-added-event.md)** - Parecer técnico/jurídico adicionado (análise registrada)
14. **[14-request-approved-event.md](./14-request-approved-event.md)** - Processo aprovado (regularização deferida)
15. **[15-certificate-issued-event.md](./15-certificate-issued-event.md)** - Certidão emitida (documento oficial, QR code, cartório)
16. **[16-contestation-received-event.md](./16-contestation-received-event.md)** - Contestação recebida (terceiro se opõe, pausar workflow)
17. **[17-deadline-approaching-event.md](./17-deadline-approaching-event.md)** - Prazo se aproximando (alerta 120 dias, priorizar análise)
18. **[18-request-rejected-event.md](./18-request-rejected-event.md)** - Processo rejeitado (indeferido, motivos fundamentados)
19. **[19-correction-requested-event.md](./19-correction-requested-event.md)** - Correções solicitadas (pausar até resubmissão)

---

## 🔄 Padrões de Implementação

### Dispatch de Eventos

Events são despachados **após SaveChanges** garantindo transação foi commitada:

```
1. Aggregate executa ação (CreateUnit, LinkHolder, ApproveRequest)
2. Aggregate adiciona event à collection interna
3. Repository persiste aggregate
4. SaveChanges commita transação
5. Event dispatcher publica events para handlers
```

### Handlers Subscribers

Handlers executam **fora de transação** original prevenindo rollback cascata:

- **Notificações:** Email, SMS, in-app
- **Cache:** Invalidação de queries
- **Métricas:** Contadores, dashboards
- **Auditoria:** Logs, timeline
- **Integrações:** Webhooks, sistemas externos
- **Validações assíncronas:** Background jobs

### Idempotência

Events podem ser reprocessados (retry de mensageria), handlers devem ser **idempotentes**:

- Deduplicar por `event_id` antes de processar
- Verificar se side effect já foi executado
- Use operações naturalmente idempotentes (SET ao invés de INCREMENT)

---

## 📐 Estrutura Padrão de Event

Cada event file segue **dense-paragraph-standard** (200-600 palavras parágrafo contínuo):

**Seções:**
1. **Payload:** Dados contidos no evento (IDs, valores anteriores/novos, timestamps)
2. **Handlers:** Side effects executados por subscribers
3. **Motivações:** Por que evento existe, problemas que resolve
4. **Regras de processamento:** Dispatch após SaveChanges, idempotência, async handlers

**Tecnologia-agnóstico:** Não menciona PostgreSQL, WatermelonDB, .NET, React Native (apenas conceitos)

**Implementações:** Links para (caminho de implementação) com implementações específicas

---

## 🎯 Quando Criar Novo Event

**✅ Criar event quando:**
- Fato de negócio significativo ocorreu (não mudança técnica)
- Outras partes do sistema precisam reagir
- Side effects devem ser desacoplados do aggregate
- Auditoria ou timeline precisa registrar fato
- Integração externa deve ser notificada

**❌ Não criar event para:**
- Mudanças puramente técnicas (cache interno)
- Ações que não interessam outras partes
- Validações síncronas (use métodos do aggregate)

---

## 🔗 Relacionado

**Aggregates:**
- **[01-unit-aggregate.md](../AGGREGATES/01-unit-aggregate.md)** - Emite Unit events
- **[02-community-aggregate.md](../AGGREGATES/02-community-aggregate.md)** - Emite Community events
- **[03-legitimation-request-aggregate.md](../AGGREGATES/03-legitimation-request-aggregate.md)** - Emite Legitimation events

**Implementações:**
- (caminho de implementação) - Backend .NET handlers
- (caminho de implementação) - Application layer handlers

**Ver também:**
- **[00-INDEX.md](../00-INDEX.md)** - Índice completo do modelo de domínio
- **[ENTITIES/](../ENTITIES/README.md)** - Entidades do domínio
- **[VALUE-OBJECTS/](../VALUE-OBJECTS/README.md)** - Value objects

---

**Última atualização:** 2025-01-06
**Status:** ✅ 19/19 eventos documentados (100%)
