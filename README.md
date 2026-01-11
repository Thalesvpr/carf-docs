# CARF - Sistema de Regularização Fundiária Urbana

Sistema completo para gestão de processos de regularização fundiária urbana (REURB) conforme Lei 13.465/2017 permitindo prefeituras municipais gerenciarem todo ciclo desde cadastramento de unidades habitacionais em campo até emissão de títulos de legitimação implementando arquitetura polyrepo com sete repositórios Git independentes (GEOAPI backend .NET 9 + PostgreSQL + PostGIS, GEOWEB frontend React 18 + Vite, REURBCAD mobile React Native + WatermelonDB offline-first, GEOGIS plugin QGIS Python para análises espaciais, ADMIN console React SPA consumindo Keycloak Admin API via backend seguro, WEBDOCS portal VitePress documentação interativa, e TSCORE biblioteca TypeScript compartilhada com value objects CPF/CNPJ validações hooks React/Vue) orquestrados em estrutura monorepo de documentação centralizada em CENTRAL/ servindo como Single Source of Truth para arquitetura ADRs requisitos funcionais domain model DDD entidades aggregates value objects business rules workflows REURB APIs REST documentadas integrações Keycloak OAuth2/OIDC SSO multi-tenancy PostgreSQL RLS isolamento por tenant policies segurança LGPD testing strategy deployment CI/CD GitHub Actions, enquanto cada PROJECTS/[PROJETO]/DOCS/ contém documentação específica de implementação técnica do projeto (ARCHITECTURE decisões Keycloak integration Clean Architecture CQRS, CONCEPTS autenticação protected routes state management offline-first, HOW-TO guias práticos setup build deploy troubleshooting, LAYERS estrutura código AuthContext services repositories controllers) seguindo padrão híbrido em camadas onde CENTRAL documenta O QUE sistema faz perspectiva produto/negócio sem mencionar tecnologias específicas e PROJECTS documenta COMO cada projeto implementa perspectiva técnica/engenharia linkando de volta para CENTRAL criando navegação bidirecional conceitual.

## Documentação

Ver [CENTRAL/README.md](./CENTRAL/README.md) para índice completo da documentação centralizada incluindo [Arquitetura ADRs](./CENTRAL/ARCHITECTURE/README.md) decisões técnicas cross-project, [Requirements](./CENTRAL/REQUIREMENTS/README.md) casos de uso requisitos funcionais user stories, [Domain Model](./CENTRAL/DOMAIN-MODEL/00-INDEX.md) entidades DDD aggregates value objects eventos domínio, [Business Rules](./CENTRAL/BUSINESS-RULES/README.md) regras REURB Lei 13465/2017, [API Specification](./CENTRAL/API/README.md) endpoints REST schemas JSON, [Keycloak Integration](./CENTRAL/INTEGRATION/KEYCLOAK/README.md) OAuth2/OIDC SSO multi-tenancy, [Database](./CENTRAL/INTEGRATION/DATABASE/README.md) PostgreSQL PostGIS RLS, [Security](./CENTRAL/SECURITY/README.md) políticas LGPD, [Testing](./CENTRAL/TESTING/README.md) pirâmide testes, [Versioning](./CENTRAL/VERSIONING/README.md) Git workflows, e [Workflows](./CENTRAL/WORKFLOWS/README.md) processos REURB legitimação fundiária.

## Projetos

Cada projeto tem repositório Git independente em PROJECTS/[PROJETO]/SRC-CODE/carf-[projeto]/ com documentação específica em PROJECTS/[PROJETO]/DOCS/:

**Backend:** [GEOAPI](./PROJECTS/GEOAPI/DOCS/README.md) - API REST .NET 9 implementando Clean Architecture + DDD + CQRS + Event Sourcing com camadas Domain/Application/Infrastructure/Presentation consumindo PostgreSQL + PostGIS via Entity Framework Core aplicando Row-Level Security multi-tenancy autenticação Keycloak OAuth2 validação tokens JWT autorização role-based políticas super-admin/admin/manager/analyst/field-agent background jobs Hangfire processamento assíncrono relatórios shapefiles sincronização mobile logging Serilog metrics Prometheus tracing OpenTelemetry deployment Docker Kubernetes health checks.

**Frontend Web:** [GEOWEB](./PROJECTS/GEOWEB/DOCS/README.md) - Portal React 18 + Vite + TypeScript consumindo GEOAPI via @carf/geoapi-client HTTP client tipado implementando autenticação Keycloak PKCE flow protected routes role-based access tenant switcher multi-tenancy server state TanStack Query client state Zustand UI shadcn/ui + Radix + Tailwind mapas Leaflet WMS layers ortofotos forms React Hook Form + Zod validation deployment Vercel edge functions CDN.

**Mobile:** [REURBCAD](./PROJECTS/REURBCAD/DOCS/README.md) - App React Native + Expo offline-first WatermelonDB SQLite persistência local coleta campo GPS camera fotos georreferenciadas desenho polígonos sincronização bidirecional GEOAPI conflict detection merge strategies autenticação Keycloak deep linking OAuth callback secure storage expo-secure-store Keychain iOS KeyStore Android biometric unlock build EAS Build deploy APK/IPA.

**Plugin GIS:** [GEOGIS](./PROJECTS/GEOGIS/DOCS/README.md) - Plugin QGIS Python 3.11 + PyQGIS integrando GEOAPI WFS/WMS endpoints autenticação JWT token storage QSettings encrypted análises espaciais buffer intersection validation topologia export Shapefile GeoJSON Processing algorithms batch operations.

**Console Admin:** [ADMIN](./PROJECTS/ADMIN/DOCS/README.md) - Console React SPA consumindo GEOAPI endpoints /api/admin/* que chamam Keycloak Admin Client API backend confidential protegendo client_secret implementando gestão usuários tenants roles via backend .NET isolado garantindo sete camadas segurança OAuth2 JWT role-based authorization tenant validation rate limiting CORS auditoria completa.

**Portal Docs:** [WEBDOCS](./PROJECTS/WEBDOCS/DOCS/README.md) - Portal VitePress + Vue 3 documentação interativa exemplos código API endpoints features requisitos roadmap.

**Biblioteca Shared:** [TSCORE](./PROJECTS/LIB/TS/TSCORE/DOCS/README.md) - Biblioteca TypeScript compartilhada @carf/tscore publicada GitHub Packages contendo value objects CPF CNPJ Email Phone validações brasileiras types entities enums DTOs sincronizados backend .NET hooks React useAuth useKeycloak ProtectedRoute composables Vue initAuth autenticação Keycloak OAuth2 token management role checking eliminando duplicação código entre GEOWEB REURBCAD ADMIN WEBDOCS.

## Stack Tecnológica

**Backend:** .NET 9 + ASP.NET Core + PostgreSQL 16 + PostGIS 3.4 + Entity Framework Core + Keycloak 24 OAuth2/OIDC + MediatR CQRS + FluentValidation + Serilog + Hangfire background jobs + Docker + Kubernetes.

**Frontend:** React 18 + TypeScript 5 + Vite + TanStack Query server state + Zustand client state + Tailwind CSS + shadcn/ui components + Leaflet mapas + React Hook Form + Zod validation + Vercel deployment.

**Mobile:** React Native + Expo SDK + WatermelonDB SQLite offline + React Navigation + expo-camera + expo-location GPS + expo-secure-store + EAS Build.

**GIS:** Python 3.11 + PyQGIS + GDAL/OGR + Shapely + requests HTTP + QSettings encrypted storage.

**Shared:** TypeScript + Bun runtime + React 18 hooks + Vue 3 composables publicado NPM @carf/tscore.

## Setup Rápido

Subir infraestrutura local PostgreSQL + PostGIS em CENTRAL/INTEGRATION/DATABASE via docker-compose up -d e Keycloak + PostgreSQL em CENTRAL/INTEGRATION/KEYCLOAK via docker-compose up -d acessando Admin Console http://localhost:8080 com credenciais admin/admin importando realm-export.json configuração completa clients roles users. Rodar backend navegando PROJECTS/GEOAPI/SRC-CODE/carf-geoapi executando dotnet restore && dotnet ef database update && dotnet run. Rodar frontend navegando PROJECTS/GEOWEB/SRC-CODE/carf-geoweb executando npm install && npm run dev acessando http://localhost:5173. Ver instruções detalhadas em cada PROJECTS/[PROJETO]/SRC-CODE/carf-[projeto]/README.md e guias HOW-TO em PROJECTS/[PROJETO]/DOCS/HOW-TO/ para setup desenvolvimento build deploy troubleshooting específico de cada projeto.

## Legislação

Sistema implementa requisitos Lei 13.465/2017 Regularização Fundiária Urbana (REURB) distinguindo modalidades REURB-S interesse social população baixa renda área até 250m² gratuito documentação simplificada e REURB-E interesse específico área até 500m² taxa cobrada documentação completa licenças ambientais, Estatuto da Cidade Lei 10.257/2001, e Decreto 9.310/2018 regulamentação REURB com workflows documentados CENTRAL/WORKFLOWS/ detalhando processos legitimação fundiária cadastramento aprovação notificação edital contestações decisão emissão certidões conforme legislação vigente.

## Contribuindo

Identificar repositório apropriado PROJECTS/[PROJETO]/SRC-CODE/carf-[projeto]/ criar branch feature/nome-feature commits seguindo [Conventional Commits](./CENTRAL/VERSIONING/GIT/03-commit-conventions.md) formato feat(escopo): descrição push origin feature/nome-feature abrir Pull Request seguindo [PR Guidelines](./CENTRAL/VERSIONING/GIT/04-pr-guidelines.md) processo review approval checklist e [Branching Strategy](./CENTRAL/VERSIONING/GIT/02-branching-strategy.md) trunk-based development. Documentação compartilhada editar CENTRAL/ documentação específica editar PROJECTS/[PROJETO]/DOCS/ código-fonte editar PROJECTS/[PROJETO]/SRC-CODE/carf-[projeto]/ cada repo Git independente com CI/CD próprio.

---

**Versão:** v1.0.0 MVP
**Status:** 🚧 Em desenvolvimento
**Licença:** UNLICENSED (Proprietário)
**Última atualização:** 2026-01-10
