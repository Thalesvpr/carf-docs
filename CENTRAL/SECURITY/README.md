---
type: readme
status: approved
updated: 2026-01-25
---

# SECURITY

Documentacao de seguranca e compliance do sistema CARF cobrindo estrategia de protecao e conformidade regulatoria.

A [estrategia de seguranca](./01-security-strategy.md) define defesa em profundidade com protecao contra brute force, rate limiting, politica de senha forte, isolamento do Admin Console via VPN, MFA obrigatorio para admins, criptografia TLS 1.3 com JWT RS256, e audit logging com retencao de 90 dias exportado para SIEM.

O [compliance LGPD](./02-lgpd-compliance.md) documenta os controles implementados para atender a Lei Geral de Protecao de Dados incluindo gestao de consentimento explicito, endpoints para direitos dos titulares como acesso, correcao, portabilidade e anonimizacao, DPO designado com prazo de resposta de 15 dias, retencao de 5 anos com anonimizacao automatica, e notificacao de breach a ANPD em 72 horas.

Decisoes arquiteturais relacionadas a seguranca estao documentadas em ARCHITECTURE/DECISIONS, incluindo autenticacao via Keycloak, multi-tenancy via Row-Level Security, e modelo RBAC com hierarquia de roles.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (2)

| Documento | Status |
|-----------|--------|
| [Estrategia de Seguranca](./01-security-strategy.md) | ⚠ |
| [LGPD Overview](./02-lgpd-compliance.md) | ⚠ |

<!-- CARF-INDEX-END -->
