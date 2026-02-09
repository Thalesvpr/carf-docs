---
type: readme
status: review
updated: 2026-02-07
---

# SECURITY

Praticas de seguranca e hardening do Keycloak para proteger autenticacao e autorizacao no ecossistema CARF. Documenta configuracoes obrigatorias para producao e medidas de protecao contra ataques comuns em sistemas de identidade.

As [boas praticas](./01-best-practices.md) cobrem configuracoes recomendadas incluindo HTTPS obrigatorio (sslRequired: external), password policy e audit logging. A [protecao contra ataques](./02-attack-protection.md) documenta defesas contra brute force (5 tentativas, lockout progressivo ate 15min, janela de 12h) e outros vetores. O [gerenciamento de secrets](./03-secrets-management.md) explica armazenamento seguro de client secrets (geogis e confidential) usando Kubernetes Secrets e rotacao periodica.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [Boas Práticas](./01-best-practices.md) | ⚠ |
| [Proteção Contra Ataques](./02-attack-protection.md) | ⚠ |
| [Gerenciamento de Secrets](./03-secrets-management.md) | ⚠ |

<!-- CARF-INDEX-END -->
