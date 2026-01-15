# POLICIES

Políticas de segurança do CARF definindo regras e controles obrigatórios.

A política de [autenticação](./01-authentication-policy.md) define o uso de Keycloak com SSO OAuth2/OIDC, validação de tokens JWT com assinatura RS256, refresh token rotation e MFA obrigatório para roles elevados via TOTP ou SMS. Session timeout de 30 minutos por inatividade.

A política de [autorização](./02-authorization-policy.md) implementa RBAC com cinco níveis: SUPER_ADMIN, ADMIN, MANAGER, ANALYST e FIELD_AGENT. Permissões granulares por tipo de recurso seguindo princípio de least privilege e segregação de responsabilidades.

A política de [criptografia](./03-encryption-policy.md) exige AES-256 para dados em repouso, TLS 1.3 mínimo para dados em trânsito, certificate pinning no mobile, HSTS headers e bcrypt com work factor 12 para senhas.

A política de [compliance LGPD](./04-lgpd-compliance-policy.md) garante consentimento explícito, portabilidade via exportação JSON, direito ao esquecimento com anonimização, DPO designado e notificação de breach à ANPD em 72 horas.

A política de [controle de acesso](./05-access-control-policy.md) define MFA obrigatório para ADMIN, session timeout, audit log de alterações de permissões e revisão anual das políticas.

## Políticas

- **[01-authentication-policy.md](./01-authentication-policy.md)** - Autenticação, SSO e MFA
- **[02-authorization-policy.md](./02-authorization-policy.md)** - RBAC e permissões
- **[03-encryption-policy.md](./03-encryption-policy.md)** - Criptografia e hashing
- **[04-lgpd-compliance-policy.md](./04-lgpd-compliance-policy.md)** - Compliance LGPD
- **[05-access-control-policy.md](./05-access-control-policy.md)** - Controle de acesso e auditoria

---

**Última atualização:** 2026-01-14
