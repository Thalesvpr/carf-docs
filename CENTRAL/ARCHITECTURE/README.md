# ARCHITECTURE

Documentação da arquitetura sistêmica do CARF organizada em DEPLOYMENT (estratégias multi-ambiente dev/staging/prod, containerização, orquestração Kubernetes, CI/CD, mobile deployment, static sites), PATTERNS (padrões arquiteturais como Clean Architecture, CQRS, Repository/UoW, Domain Events, frontend patterns React, offline-first mobile, GIS spatial patterns), e ADRs (Architecture Decision Records documentando decisões críticas polyrepo, Keycloak auth, RLS multi-tenancy, offline-first). Define princípios arquiteturais separation of concerns, dependency inversion, single responsibility, e fail-fast com circuit breakers aplicados nos cinco projetos (GEOAPI, GEOWEB, REURBCAD, GEOGIS, WEBDOCS). Para implementação técnica detalhada de cada projeto consulte PROJECTS/*/DOCS/ contendo guias práticos por camada, conceitos específicos, e how-tos de desenvolvimento (exemplo: PROJECTS/GEOAPI/DOCS/LAYERS/ documenta Domain/Application/Infrastructure em .NET).

---

**Última atualização:** 2025-12-29
