# Incident Classification

Classificação de incidentes de segurança do CARF por severidade e tipo orientando resposta apropriada. Severidade P0 Critical (sistema completamente indisponível afetando todos usuários, vazamento dados sensíveis CPF/senhas, ransomware criptografando database, RCE permitindo execução código arbitrário) exige resposta imediata 24/7 war room, SLA resolução 4h, e comunicação ANPD/imprensa se vazamento. Severidade P1 High (funcionalidade crítica quebrada afetando >50% usuários, tentativa acesso não autorizado detectada, DDoS degradando performance, SQL injection vulnerabilidade descoberta) exige resposta 1h horário comercial, SLA resolução 24h, e escalation CTO se não resolvido. Severidade P2 Medium (bug afetando <50% usuários workaround disponível, phishing email reportado usuários, dependency vulnerabilidade medium CVE, rate limiting bypass descoberto) exige resposta 4h, SLA resolução 7 dias, e fix agendado próximo release. Severidade P3 Low (issue cosmético UI, spam reports, dependency vulnerabilidade low CVE, warning logs não críticos) exige resposta 2 dias, SLA resolução 30 dias, e backlog priorizando conforme capacidade. Tipos incidentes (data breach vazamento dados, malware/ransomware infecção, unauthorized access tentativa invasão, DoS/DDoS ataque disponibilidade, social engineering phishing/pretexting, insider threat ação maliciosa colaborador, misconfiguration exposição acidental dados) requerem playbooks específicos response.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
