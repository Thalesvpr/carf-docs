# INCIDENTS

Resposta a incidentes de segurança do CARF. incident-response-plan.md define fases (detecção via monitoring/alerts, triagem avaliando severidade, contenção isolando sistema afetado, erradicação removendo causa raiz, recuperação restaurando serviço, post-mortem documentando lições aprendidas), roles (Incident Commander coordena resposta, Security Lead investiga vetor, Engineering Lead executa fixes, Communications Lead notifica stakeholders), e SLAs (Critical 15min response, High 1h, Medium 4h, Low 24h). incident-classification.md categoriza severidade (Critical: dados vazados/sistema down, High: tentativa invasão/exploit detectado, Medium: vulnerabilidade descoberta, Low: configuração inadequada) e tipo (data breach, DDoS, malware, insider threat, misconfiguration). audit-logging.md especifica eventos logados (autenticação sucesso/falha, alterações dados críticos, mudanças permissions, acessos admin), formato structured JSON, retention 5 anos para compliance, e SIEM integration.

---

**Última atualização:** 2025-12-29
