# CENTRAL - Fonte Única de Verdade

Documentação central do CARF servindo como fonte única de verdade para requisitos, decisões arquiteturais e modelo de domínio compartilhados entre todos os projetos do sistema, organizados em estrutura plana facilitando navegação e descoberta conforme [conventions](../README.md) estabelecidas.

## Áreas Principais

Especificação de produto e negócio organizada em [REQUIREMENTS/](./REQUIREMENTS/README.md) contendo casos de uso user stories e requisitos funcionais/não-funcionais do sistema, [ARCHITECTURE/](./ARCHITECTURE/README.md) documentando ADRs com decisões arquiteturais e padrões de design, [DOMAIN-MODEL/](./DOMAIN-MODEL/README.md) definindo entities aggregates value objects e workflows de negócio seguindo DDD tactical patterns, e [BUSINESS-RULES/](./BUSINESS-RULES/README.md) especificando regras de validação e workflows de aprovação conforme Lei 13465/2017 REURB.

Fluxos e processos documentados em [WORKFLOWS/](./WORKFLOWS/README.md) descrevendo end-to-end workflows do sistema de legitimação fundiária. Integrações técnicas cobrem [INTEGRATION/](./INTEGRATION/README.md) especificando conexões externas Keycloak OAuth2 e PostgreSQL+PostGIS, [API/](./API/README.md) definindo contratos REST JSON entre componentes, e [OPERATIONS/](./OPERATIONS/README.md) detalhando monitoring logging maintenance e troubleshooting. Políticas e padrões incluem SECURITY com conformidade LGPD, TESTING com estratégia test pyramid, VERSIONING com Git workflow e semantic versioning, e TEMPLATES provendo modelos padronizados para documentação consistente.

Para implementação técnica específica por projeto, consulte PROJECTS (GEOAPI backend .NET, GEOWEB portal web React, REURBCAD mobile React Native, GEOGIS plugin QGIS, WEBDOCS site documentação).

---

**Última atualização:** 2026-01-10
