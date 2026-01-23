---
type: readme
status: draft
updated: 2026-01-22
---

# SECURITY

Politicas de seguranca e compliance do sistema CARF.

A [estrategia de seguranca](./STRATEGY/README.md) define defesa em profundidade com sete camadas de protecao: brute force, rate limiting, politica de senha, isolamento admin, criptografia TLS/JWT, audit logging e headers HTTP. A [autenticacao e autorizacao](./AUTH/README.md) usa Keycloak com SSO OAuth2/OIDC, MFA para roles elevados e RBAC com cinco niveis hierarquicos.

O [compliance](./COMPLIANCE/README.md) atende LGPD com consentimento explicito, portabilidade de dados, direito ao esquecimento, DPO designado e notificacao de breach a ANPD em 72 horas. As [politicas](./POLICIES/README.md) detalham regras de autenticacao, autorizacao, criptografia e controle de acesso. Os [procedimentos de incidentes](./INCIDENTS/README.md) cobrem classificacao, resposta, contencao e post-mortem.

A criptografia usa AES-256 para dados em repouso, TLS 1.3 para dados em transito e bcrypt com salt rounds 12 para hashing de senhas. O isolamento multi-tenant usa Row-Level Security no PostgreSQL com tenant_id extraido dos claims JWT.
