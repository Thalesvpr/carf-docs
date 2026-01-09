# POLICIES

Políticas de segurança do CARF. encryption-policy.md define criptografia dados em repouso (AES-256 para database, S3 server-side encryption para arquivos), dados em trânsito (TLS 1.3 mínimo, certificate pinning no mobile, HSTS headers), e hashing de senhas (bcrypt work factor 12, salt único por senha). password-policy.md especifica requisitos (mínimo 12 caracteres, mix maiúsculas/minúsculas/números/símbolos, não permitir senhas comuns do OWASP list, expiração 90 dias para roles administrativos, histórico 5 senhas anteriores). access-control-policy.md define RBAC (roles Administrador/Técnico/Fiscal/Cidadão com permissions granulares), princípio least privilege (usuários têm apenas permissions necessárias), MFA obrigatório para Administrador, session timeout 30min inatividade, e audit log de todas alterações de permissions. Políticas revisadas anualmente e após incidentes.

---

**Última atualização:** 2025-12-29
