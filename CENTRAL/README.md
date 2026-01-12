# CENTRAL

Documentação central CARF servindo fonte única verdade requisitos decisões arquiteturais modelo domínio compartilhados todos projetos sistema organizados estrutura plana facilitando navegação descoberta especificação produto negócio organizada REQUIREMENTS contendo quatrocentos cinquenta e sete arquivos casos uso user stories requisitos funcionais não-funcionais sistema estabelecendo rastreabilidade bidirecional UC RF US RNF entre specification implementation PROJECTS FEATURES ARCHITECTURE documentando ADRs Architecture Decision Records registrando decisões críticas polyrepo Keycloak auth RLS multi-tenancy offline-first além padrões design Clean Architecture CQRS Repository UoW Domain Events frontend patterns React offline-first mobile GIS spatial patterns aplicados cinco projetos GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS DOMAIN-MODEL definindo entities aggregates value objects workflows negócio seguindo DDD tactical patterns UnitAggregate root coordenando Unit UnitHolders Documents Annotations encapsulando invariantes negócio validações server-side BUSINESS-RULES especificando regras validação workflows aprovação conforme Lei 13465/2017 REURB implementando state machine transitions DRAFT PENDING APPROVED REJECTED holder-validation CPF único LGPD compliance unit-validation geometria válida sem overlaps spatial queries PostGIS fluxos processos documentados WORKFLOWS descrevendo end-to-end workflows sistema legitimação fundiária field data collection workflow coleta campo mobile offline-first WatermelonDB sync bidirectional analyst validation workflow correção massa QGIS desktop ortofotos WMS topologia topography workflow levantamento GNSS RTK precisão centímetros memorial descritivo monografia técnica assinado responsável técnico CREA integrações técnicas cobrem INTEGRATION especificando conexões externas Keycloak OAuth2 OIDC SSO multi-tenancy realm único carf clients pré-configurados SPA PKCE Mobile Bearer-only PostgreSQL PostGIS persistence RLS policies isolando dados tenant API definindo contratos REST JSON schemas endpoints CRUD units holders communities legitimation paginação filtros ordenação HATEOAS versionamento header OPERATIONS detalhando monitoring Prometheus metrics logging Serilog estruturado maintenance troubleshooting health checks deployment strategies políticas padrões incluem SECURITY conformidade LGPD consentimento direito esquecimento portabilidade DPO registro processamento ANPD criptografia AES-256 dados repouso TLS 1.3 dados trânsito bcrypt hashing senhas auditoria completa retention cinco anos MFA obrigatório roles elevados TESTING estratégia test pyramid unit tests coverage oitenta por cento integration tests Testcontainers e2e tests Playwright VERSIONING Git workflow trunk-based development Conventional Commits semantic versioning branching strategy PR guidelines LIBRARIES documentando bibliotecas compartilhadas TypeScript carf tscore validações CPF CNPJ formatações carf ui componentes React shadcn Tailwind carf geoapi-client SDK HTTP TypeScript type-safe facilitando reuso código consistência cross-project reduzindo duplicação bugs.

## Estrutura

- **[REQUIREMENTS/](./REQUIREMENTS/README.md)** - Casos uso requisitos funcionais user stories
- **[ARCHITECTURE/](./ARCHITECTURE/README.md)** - ADRs padrões arquiteturais deployment
- **[DOMAIN-MODEL/](./DOMAIN-MODEL/README.md)** - Entities aggregates value objects workflows DDD
- **[BUSINESS-RULES/](./BUSINESS-RULES/README.md)** - Regras validação workflows Lei 13465/2017
- **[API/](./API/README.md)** - Contratos REST schemas JSON endpoints
- **[INTEGRATION/](./INTEGRATION/README.md)** - Integrações Keycloak PostgreSQL DATABASE
- **[SECURITY/](./SECURITY/README.md)** - Políticas segurança LGPD compliance
- **[TESTING/](./TESTING/README.md)** - Estratégia testes pyramid coverage
- **[OPERATIONS/](./OPERATIONS/README.md)** - Monitoring logging maintenance troubleshooting
- **[VERSIONING/](./VERSIONING/README.md)** - Git workflow versionamento semantic
- **[WORKFLOWS/](./WORKFLOWS/README.md)** - Workflows end-to-end sistema legitimação
- **[LIBRARIES/](./LIBRARIES/README.md)** - Bibliotecas compartilhadas TypeScript React

---

**Última atualização:** 2026-01-11
