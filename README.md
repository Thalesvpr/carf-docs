# CARF - Sistema de Regularização Fundiária Urbana

Sistema completo para gestão de processos de regularização fundiária urbana (REURB) conforme Lei 13.465/2017 permitindo prefeituras municipais gerenciarem todo ciclo desde cadastramento de unidades habitacionais em campo até emissão de títulos de legitimação implementando arquitetura polyrepo com sete repositórios Git independentes (GEOAPI backend .NET 9 + PostgreSQL + PostGIS, GEOWEB frontend React 18 + Vite, REURBCAD mobile React Native + WatermelonDB offline-first, GEOGIS plugin QGIS Python para análises espaciais, ADMIN console React SPA consumindo Keycloak Admin API via backend seguro, WEBDOCS portal VitePress documentação interativa, e TSCORE biblioteca TypeScript compartilhada com value objects CPF/CNPJ validações hooks React/Vue) orquestrados em estrutura monorepo de documentação centralizada em CENTRAL/ servindo como Single Source of Truth para arquitetura ADRs requisitos funcionais domain model DDD entidades aggregates value objects business rules workflows REURB APIs REST documentadas integrações Keycloak OAuth2/OIDC SSO multi-tenancy PostgreSQL RLS isolamento por tenant policies segurança LGPD testing strategy deployment CI/CD GitHub Actions, enquanto cada PROJECTS/[PROJETO]/DOCS/ contém documentação específica de implementação técnica do projeto (ARCHITECTURE decisões Keycloak integration Clean Architecture CQRS, CONCEPTS autenticação protected routes state management offline-first, HOW-TO guias práticos setup build deploy troubleshooting, LAYERS estrutura código AuthContext services repositories controllers) seguindo padrão híbrido em camadas onde CENTRAL documenta O QUE sistema faz perspectiva produto/negócio sem mencionar tecnologias específicas e PROJECTS documenta COMO cada projeto implementa perspectiva técnica/engenharia linkando de volta para CENTRAL criando navegação bidirecional conceitual.

## Documentação

- **[CENTRAL](./CENTRAL/README.md)** - Documentação centralizada cross-project
- **[PROJECTS](./PROJECTS/README.md)** - Projetos de implementação


---

**Versão:** v1.0.0 MVP
**Status:** 🚧 Em PLANEJAMENTO
**Licença:** UNLICENSED (Proprietário)
**Última atualização:** 2026-01-11
