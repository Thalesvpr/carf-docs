# SECURITY

Políticas de segurança e compliance do sistema CARF.

A autenticação usa Keycloak com SSO OAuth2/OIDC e MFA obrigatório para roles elevados. A autorização implementa RBAC com cinco níveis hierárquicos e permissões granulares por tipo de recurso. O isolamento multi-tenant usa Row-Level Security no PostgreSQL com tenant_id extraído dos claims JWT.

O compliance LGPD inclui consentimento explícito, portabilidade de dados, direito ao esquecimento com anonimização, DPO designado e notificação de breach à ANPD em 72 horas conforme Lei 13.709/2018.

A criptografia usa AES-256 para dados em repouso, TLS 1.3 para dados em trânsito e bcrypt com salt rounds 12 para hashing de senhas. A auditoria registra todos os acessos e alterações com retenção de 5 anos.

As [políticas](./POLICIES/README.md) definem regras de autenticação, autorização, criptografia e LGPD. Os [procedimentos de incidentes](./INCIDENTS/README.md) cobrem classificação, resposta, contenção e post-mortem.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (9 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Incidents](./INCIDENTS/README.md) | 4 |
|  | [Policies](./POLICIES/README.md) | 5 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
