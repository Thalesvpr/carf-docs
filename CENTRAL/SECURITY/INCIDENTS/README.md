# INCIDENTS

Resposta a incidentes de segurança do CARF.

A [classificação de incidentes](./01-incident-classification.md) define quatro níveis de severidade: Critical para dados vazados ou sistema down, High para tentativa de invasão ou exploit detectado, Medium para vulnerabilidade descoberta, e Low para configuração inadequada. Os tipos incluem data breach, DDoS, malware, insider threat e misconfiguration.

O [plano de resposta](./02-incident-response-plan.md) define as fases: detecção via monitoring e alerts, triagem avaliando severidade, contenção isolando sistemas afetados, erradicação removendo a causa raiz, recuperação restaurando o serviço, e post-mortem documentando lições aprendidas.

Os SLAs de resposta são: Critical 15 minutos, High 1 hora, Medium 4 horas, Low 24 horas.

A [notificação de breach](./03-breach-notification.md) segue LGPD com comunicação à ANPD em 72 horas, identificação de dados pessoais afetados e notificação aos titulares. O DPO é responsável pela coordenação.

O [audit logging](./04-audit-logging.md) registra eventos de autenticação, alterações em dados críticos, mudanças de permissões e acessos admin em formato JSON estruturado com retenção de 5 anos e integração SIEM.

---

**Última atualização:** 2026-01-14

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (4 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-incident-classification](./01-incident-classification.md) | Incident Classification |
| [02-incident-response-plan](./02-incident-response-plan.md) | Incident Response Plan |
| [03-breach-notification](./03-breach-notification.md) | Breach Notification |
| [04-audit-logging](./04-audit-logging.md) | Audit Logging |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
