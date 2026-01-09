# API

Contratos de API REST organizados por domínio de negócio: AUTHENTICATION (schemas de login, refresh token, logout, validação JWT), UNITS (unidades habitacionais com CRUD, validação geográfica, cálculo de área), HOLDERS (titulares com validação CPF, vinculação a unidades, histórico), COMMUNITIES (comunidades com agregação de unidades, relatórios demográficos), REPORTS (geração de relatórios PDF/Excel, exportação GeoJSON/Shapefile), e LEGITIMATION (processos de legitimação fundiária com workflow de aprovação). Cada domínio contém schemas JSON de request/response, validações de payload, códigos HTTP esperados, headers obrigatórios, paginação, filtros, ordenação, e exemplos de uso. Segue padrões RESTful com versionamento via header (api-version), HATEOAS para navegação, e rate limiting por tenant.

---

**Última atualização:** 2025-12-29
