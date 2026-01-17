# API

Contratos de API REST do CARF organizados por domínio de negócio. Cada domínio contém schemas JSON de request/response, validações de payload, códigos HTTP esperados, headers obrigatórios, paginação, filtros e exemplos de uso.

A API de [autenticação](./AUTHENTICATION/README.md) define schemas para login, refresh token, logout e validação JWT via Keycloak. A API de [unidades](./UNITS/README.md) cobre CRUD de unidades habitacionais com validação geográfica e cálculo de área. A API de [titulares](./HOLDERS/README.md) gerencia pessoas físicas com validação de CPF e vinculação a unidades.

A API de [comunidades](./COMMUNITIES/README.md) agrega unidades geograficamente e gera dados demográficos. A API de [legitimação](./LEGITIMATION/README.md) implementa o workflow de aprovação conforme Lei 13.465/2017. E a API de [relatórios](./REPORTS/README.md) gera exports em PDF, Excel, GeoJSON e Shapefile.

Segue padrões RESTful com versionamento via header, HATEOAS para navegação e rate limiting por tenant.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Authentication](./AUTHENTICATION/README.md) | 0 |
|  | [Communities](./COMMUNITIES/README.md) | 0 |
|  | [Holders](./HOLDERS/README.md) | 0 |
|  | [Legitimation](./LEGITIMATION/README.md) | 0 |
|  | [Reports](./REPORTS/README.md) | 0 |
|  | [Units](./UNITS/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
