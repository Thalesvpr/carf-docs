# SECURITY

Políticas de segurança e compliance do sistema CARF cobrindo autenticação via Keycloak (SSO, OIDC, OAuth2, integração LDAP), autorização baseada em roles (RBAC com roles Administrador/Técnico/Fiscal/Cidadão), multi-tenancy com isolamento por Row-Level Security garantindo que cada município veja apenas seus dados, compliance LGPD (consentimento, direito ao esquecimento, portabilidade, DPO, registro de processamento), criptografia (dados em repouso AES-256, dados em trânsito TLS 1.3, hashing bcrypt para senhas), auditoria (logs de acesso, alterações de dados críticos, retention de 5 anos), threat model identificando vetores (SQL injection, XSS, CSRF, broken authentication), POLICIES (política de senhas, política de acesso, política de backup), e INCIDENTS (plano de resposta, classificação de severidade, procedimentos de contenção e recuperação).

---

**Última atualização:** 2025-12-29
