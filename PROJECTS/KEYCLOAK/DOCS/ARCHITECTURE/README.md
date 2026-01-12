# ARCHITECTURE

Arquitetura de customização Keycloak CARF baseada em três pilares: themes FreeMarker para UI login account email sem fork do source, SPIs Java para lógica server-side como validators e event listeners, e realm configuration versionada JSON para declarar clients roles mappers. Stack usa Keycloak 24 Quarkus distribution com PostgreSQL 16, Docker image customizada empacotando themes em /themes/carf/ e extensions em /providers/, CI/CD GitHub Actions buildando imagem testando via Playwright API e deployando rolling update Kubernetes.

## Arquivos

- **[01-customization-strategy.md](./01-customization-strategy.md)** - Estratégia customização themes vs fork vs proxy trade-offs
- **[02-theme-architecture.md](./02-theme-architecture.md)** - Arquitetura temas login account email herança hot reload
- **[03-extension-development.md](./03-extension-development.md)** - Desenvolvimento extensões Java SPIs Maven Arquillian

---

**Última atualização:** 2026-01-12
