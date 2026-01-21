---
status: rejected
description: "Stub incompleto. Spec de API deve ter request/response schemas, exemplos, erros. Mover implementacao para PROJECTS/GEOAPI."
updated: 2026-01-15
---

# API

Contratos de API REST do CARF organizados por domínio de negócio. Cada domínio contém schemas JSON de request/response, validações de payload, códigos HTTP esperados, headers obrigatórios, paginação, filtros e exemplos de uso.

A API de [autenticação](./AUTHENTICATION/README.md) define schemas para login, refresh token, logout e validação JWT via Keycloak. A API de [unidades](./UNITS/README.md) cobre CRUD de unidades habitacionais com validação geográfica e cálculo de área. A API de [titulares](./HOLDERS/README.md) gerencia pessoas físicas com validação de CPF e vinculação a unidades.

A API de [comunidades](./COMMUNITIES/README.md) agrega unidades geograficamente e gera dados demográficos. A API de [legitimação](./LEGITIMATION/README.md) implementa o workflow de aprovação conforme Lei 13.465/2017. E a API de [relatórios](./REPORTS/README.md) gera exports em PDF, Excel, GeoJSON e Shapefile.

Segue padrões RESTful com versionamento via header, HATEOAS para navegação e rate limiting por tenant.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (14 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Authentication](./AUTHENTICATION/README.md) | 3 |
|  | [Communities](./COMMUNITIES/README.md) | 2 |
|  | [Holders](./HOLDERS/README.md) | 2 |
|  | [Legitimation](./LEGITIMATION/README.md) | 2 |
|  | [Reports](./REPORTS/README.md) | 2 |
|  | [Units](./UNITS/README.md) | 3 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/API/AUTHENTICATION/README|AUTHENTICATION]]
- [[CENTRAL/API/COMMUNITIES/README|COMMUNITIES]]
- [[CENTRAL/API/HOLDERS/README|HOLDERS]]
- [[CENTRAL/API/LEGITIMATION/README|LEGITIMATION]]
- [[CENTRAL/API/REPORTS/README|REPORTS]]
- [[CENTRAL/API/UNITS/README|UNITS]]

<!-- CARF-INDEX-END -->
