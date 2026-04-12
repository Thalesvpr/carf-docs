---
type: readme
status: review
updated: 2026-02-07
---

# ARCHITECTURE

Arquitetura de customizacao do Keycloak CARF baseada em tres pilares: temas Keycloakify (React/TypeScript) para UI de login, account e email reutilizando componentes @carf/ui, SPIs Java para logica server-side como validadores e event listeners, e realm configuration versionada em JSON para declarar clients, roles e mappers. Stack usa Keycloak 24 Quarkus com PostgreSQL 16, Docker image customizada empacotando temas em /themes/carf/ e extensions em /providers/.

A [estrategia de customizacao](./01-customization-strategy.md) documenta trade-offs entre themes, fork e proxy. A [arquitetura de temas](./02-theme-architecture.md) cobre heranca, hot reload e estrutura de pastas login/account/email. As extensoes Java estao documentadas em tres arquivos: [estrutura Maven](./03a-extension-structure.md) com modulos e dependencias, [SPIs implementadas](./03b-extension-spis.md) com Authenticator, Event Listener e Protocol Mapper, e [deploy e testes](./03c-extension-deploy.md) com Docker, ativacao e estrategia de testes.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (5)

| Documento | Status |
|-----------|--------|
| [Estratégia de Customização do Keycloak](./01-customization-strategy.md) | ⚠ |
| [Arquitetura de Temas Keycloak](./02-theme-architecture.md) | ⚠ |
| [Estrutura de Extensões Keycloak](./03a-extension-structure.md) | ⚠ |
| [SPIs Keycloak CARF](./03b-extension-spis.md) | ⚠ |
| [Deploy e Testes de Extensões](./03c-extension-deploy.md) | ⚠ |

<!-- CARF-INDEX-END -->
