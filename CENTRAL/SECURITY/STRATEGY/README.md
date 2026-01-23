---
type: readme
status: draft
updated: 2026-01-22
---

# STRATEGY

Estrategia de seguranca do sistema CARF com abordagem de defesa em profundidade.

O documento [01-security-strategy](./01-security-strategy.md) define as sete camadas de protecao implementadas: protecao contra brute force, rate limiting via Ingress NGINX, politica de senha forte, isolamento do admin console, criptografia TLS e JWT, audit logging com retencao de 90 dias, e headers de seguranca HTTP.

Esta estrategia atende os requisitos de conformidade LGPD para dados sensiveis de regularizacao fundiaria. As politicas especificas derivadas estao em [POLICIES](../POLICIES/README.md) e os procedimentos de resposta a incidentes em [INCIDENTS](../INCIDENTS/README.md).
