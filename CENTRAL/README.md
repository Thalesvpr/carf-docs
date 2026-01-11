# CENTRAL - Fonte Única de Verdade

Documentação central do CARF servindo como fonte única de verdade para requisitos, decisões arquiteturais e modelo de domínio compartilhados entre todos os projetos do sistema, organizados em estrutura plana facilitando navegação e descoberta conforme [conventions](../README.md) estabelecidas.

## Áreas Principais

- **[REQUIREMENTS/](./REQUIREMENTS/README.md)** - Casos de uso, user stories e requisitos funcionais/não-funcionais do sistema
- **[ARCHITECTURE/](./ARCHITECTURE/README.md)** - ADRs documentando decisões arquiteturais e padrões de design
- **[DOMAIN-MODEL/](./DOMAIN-MODEL/README.md)** - Entities, aggregates, value objects e workflows de negócio seguindo DDD
- **[BUSINESS-RULES/](./BUSINESS-RULES/README.md)** - Regras de validação e workflows de aprovação conforme Lei 13.465/2017
- **[WORKFLOWS/](./WORKFLOWS/README.md)** - Fluxos de trabalho end-to-end do sistema
- **[INTEGRATION/](./INTEGRATION/README.md)** - Integrações externas (Keycloak OAuth2, PostgreSQL+PostGIS)
- **[API/](./API/README.md)** - Contratos REST JSON entre componentes
- **[OPERATIONS/](./OPERATIONS/README.md)** - Monitoring, logging, maintenance e troubleshooting
- **SECURITY** - Políticas de segurança e compliance LGPD
- **TESTING** - Estratégia test pyramid e coverage targets
- **VERSIONING** - Git workflow, semantic versioning e changelog
- **TEMPLATES** - Modelos padronizados para documentação

Para implementação técnica específica por projeto, consulte PROJECTS (GEOAPI backend .NET, GEOWEB portal web React, REURBCAD mobile React Native, GEOGIS plugin QGIS, WEBDOCS site documentação).

---

**Última atualização:** 2026-01-10
