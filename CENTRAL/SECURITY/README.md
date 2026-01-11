# SECURITY

Políticas de segurança e compliance do sistema CARF cobrindo autenticação via Keycloak (SSO, OIDC, OAuth2, integração LDAP), autorização baseada em roles (RBAC com roles Administrador/Técnico/Fiscal/Cidadão), multi-tenancy com isolamento por Row-Level Security garantindo que cada município veja apenas seus dados, compliance LGPD (consentimento, direito ao esquecimento, portabilidade, DPO, registro de processamento), criptografia (dados em repouso AES-256, dados em trânsito TLS 1.3, hashing bcrypt para senhas), auditoria (logs de acesso, alterações de dados críticos, retention de 5 anos), threat model identificando vetores (SQL injection, XSS, CSRF, broken authentication), POLICIES (política de senhas, política de acesso, política de backup), e INCIDENTS (plano de resposta, classificação de severidade, procedimentos de contenção e recuperação).

## Políticas de Segurança

Ver [POLICIES/](./POLICIES/README.md):
- [01-authentication-policy.md](./POLICIES/01-authentication-policy.md) - Política de autenticação e controle de acesso
- [02-authorization-policy.md](./POLICIES/02-authorization-policy.md) - Política de autorização baseada em roles
- [03-encryption-policy.md](./POLICIES/03-encryption-policy.md) - Política de criptografia de dados
- [04-lgpd-compliance-policy.md](./POLICIES/04-lgpd-compliance-policy.md) - Política de compliance LGPD
- [05-access-control-policy.md](./POLICIES/05-access-control-policy.md) - Política de controle de acesso e permissões

## Resposta a Incidentes

Ver [INCIDENTS/](./INCIDENTS/README.md):
- [01-incident-classification.md](./INCIDENTS/01-incident-classification.md) - Classificação de severidade de incidentes
- [02-incident-response-plan.md](./INCIDENTS/02-incident-response-plan.md) - Plano de resposta a incidentes
- [03-breach-notification.md](./INCIDENTS/03-breach-notification.md) - Procedimentos de notificação de violação
- [04-audit-logging.md](./INCIDENTS/04-audit-logging.md) - Auditoria e logging de segurança

---

**Última atualização:** 2025-12-29
