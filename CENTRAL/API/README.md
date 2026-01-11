# API

Contratos de API REST organizados por domínio de negócio: AUTHENTICATION (schemas de login, refresh token, logout, validação JWT), UNITS (unidades habitacionais com CRUD, validação geográfica, cálculo de área), HOLDERS (titulares com validação CPF, vinculação a unidades, histórico), COMMUNITIES (comunidades com agregação de unidades, relatórios demográficos), REPORTS (geração de relatórios PDF/Excel, exportação GeoJSON/Shapefile), e LEGITIMATION (processos de legitimação fundiária com workflow de aprovação). Cada domínio contém schemas JSON de request/response, validações de payload, códigos HTTP esperados, headers obrigatórios, paginação, filtros, ordenação, e exemplos de uso. Segue padrões RESTful com versionamento via header (api-version), HATEOAS para navegação, e rate limiting por tenant.

## Domínios de API

- **[AUTHENTICATION/](./AUTHENTICATION/README.md)** - Autenticação OAuth2/OIDC (login, refresh token, logout, validação JWT)
- **[UNITS/](./UNITS/README.md)** - Unidades habitacionais (CRUD, validação geográfica, cálculo de área)
- **[HOLDERS/](./HOLDERS/README.md)** - Titulares (validação CPF, vinculação a unidades, histórico)
- **[COMMUNITIES/](./COMMUNITIES/README.md)** - Comunidades (agregação de unidades, relatórios demográficos)
- **[LEGITIMATION/](./LEGITIMATION/README.md)** - Processos de legitimação fundiária (workflow de aprovação Lei 13465/2017)
- **[REPORTS/](./REPORTS/README.md)** - Geração de relatórios (PDF, Excel, GeoJSON, Shapefile)

---

**Última atualização:** 2025-12-29
