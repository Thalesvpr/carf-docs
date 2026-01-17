# LIBRARIES

Bibliotecas TypeScript compartilhadas publicadas no GitHub Packages eliminando duplicação de código entre frontends GEOWEB, REURBCAD, ADMIN e WEBDOCS.

A biblioteca [@carf/tscore](./01-tscore.md) fornece a camada base com Value Objects, validações, types sincronizados com backend e hooks de autenticação Keycloak. A biblioteca [@carf/geoapi-client](./02-geoapi-client.md) provê SDK HTTP type-safe para comunicação com o backend GEOAPI incluindo retry logic, circuit breaker e suporte offline. A biblioteca [@carf/ui](./03-ui-components.md) oferece componentes React reutilizáveis baseados em shadcn/ui com Tailwind CSS, dark mode e acessibilidade WCAG 2.1 AA.

Arquitetura em camadas onde @carf/ui depende de @carf/geoapi-client que depende de @carf/tscore, garantindo consistência e reuso entre todas as aplicações frontend do ecossistema CARF.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-tscore](./01-tscore.md) | @carf/tscore |
| [02-geoapi-client](./02-geoapi-client.md) | @carf/geoapi-client |
| [03-ui-components](./03-ui-components.md) | @carf/ui |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
