# CARF - Sistema de Regularização Fundiária Urbana

Sistema completo para gestão de processos de regularização fundiária urbana (REURB) conforme Lei 13.465/2017.

## Visão Geral

O CARF é um ecossistema integrado de aplicações para digitalização e automação dos processos de regularização fundiária urbana, permitindo que prefeituras municipais gerenciem de forma eficiente todo o ciclo da REURB - desde o cadastramento de unidades habitacionais em campo até a emissão de títulos de legitimação.

### Características Principais

- **Multi-tenancy**: Suporte a múltiplas prefeituras isoladas por RLS (Row-Level Security)
- **Offline-first**: Coleta de dados em campo sem conectividade
- **Geoespacial**: Integração PostGIS + QGIS para análises espaciais
- **SSO**: Single Sign-On via Keycloak entre todas as aplicações
- **Polyrepo**: Arquitetura modular com 7 repositórios independentes
- **Clean Architecture**: DDD, CQRS, Event Sourcing no backend

## Arquitetura Polyrepo

O projeto CARF segue arquitetura **polyrepo** com 7 repositórios Git independentes:

| Repositório | Descrição | Tecnologia | URL |
|-------------|-----------|------------|-----|
| **carf-docs** | Documentação central (SSOT) | Markdown | [github.com/Thalesvpr/carf-docs](https://github.com/Thalesvpr/carf-docs) |
| **carf-tscore** | Biblioteca TypeScript compartilhada | TypeScript + Bun | [github.com/Thalesvpr/carf-tscore](https://github.com/Thalesvpr/carf-tscore) |
| **carf-geoapi** | Backend API REST | .NET 9 + PostgreSQL + PostGIS | [github.com/Thalesvpr/carf-geoapi](https://github.com/Thalesvpr/carf-geoapi) |
| **carf-geoweb** | Frontend web | React 18 + TypeScript + Tailwind | [github.com/Thalesvpr/carf-geoweb](https://github.com/Thalesvpr/carf-geoweb) |
| **carf-reurbcad** | App mobile | React Native + WatermelonDB | [github.com/Thalesvpr/carf-reurbcad](https://github.com/Thalesvpr/carf-reurbcad) |
| **carf-geogis** | Plugin QGIS | Python + PyQGIS | [github.com/Thalesvpr/carf-geogis](https://github.com/Thalesvpr/carf-geogis) |
| **carf-webdocs** | Portal de documentação | VitePress + Vue 3 | [github.com/Thalesvpr/carf-webdocs](https://github.com/Thalesvpr/carf-webdocs) |
| **carf-admin** | Console administrativo | Next.js 14 + React 18 | [github.com/Thalesvpr/carf-admin](https://github.com/Thalesvpr/carf-admin) |

## Estrutura do Repositório carf-docs

Este repositório contém a **documentação centralizada** (SSOT - Single Source of Truth) do projeto CARF:

```
CARF/
├── CENTRAL/                    # Documentação centralizada (SSOT)
│   ├── API/                    # Especificações de API
│   ├── ARCHITECTURE/           # Decisões arquiteturais (ADRs)
│   ├── BUSINESS-RULES/         # Regras de negócio REURB
│   ├── DOMAIN-MODEL/           # Modelo de domínio
│   ├── INTEGRATION/            # Integrações externas
│   │   └── KEYCLOAK/          # Keycloak OAuth2/OIDC
│   ├── OPERATIONS/             # DevOps, CI/CD, Monitoramento
│   ├── REQUIREMENTS/           # Requisitos funcionais e não-funcionais
│   ├── SECURITY/               # Políticas de segurança
│   ├── TEMPLATES/              # Templates de documentação
│   ├── TESTING/                # Estratégias de teste
│   ├── VERSIONING/             # Git, Branching, Releases
│   └── WORKFLOWS/              # Processos REURB (Lei 13.465)
│
└── PROJECTS/                   # Documentação por projeto
    ├── GEOAPI/
    │   ├── DOCS/               # Docs específicas do backend
    │   └── SRC-CODE/          # → Link para carf-geoapi repo
    ├── GEOWEB/
    │   ├── DOCS/
    │   └── SRC-CODE/          # → Link para carf-geoweb repo
    ├── REURBCAD/
    │   ├── DOCS/
    │   └── SRC-CODE/          # → Link para carf-reurbcad repo
    ├── GEOGIS/
    │   ├── DOCS/
    │   └── SRC-CODE/          # → Link para carf-geogis repo
    ├── WEBDOCS/
    │   └── SRC-CODE/          # → Link para carf-webdocs repo
    └── ADMIN/
        ├── DOCS/
        └── SRC-CODE/          # → Link para carf-admin repo
```

## Setup Inicial

### 1. Clonar este repositório (documentação)

```bash
git clone https://github.com/Thalesvpr/carf-docs.git CARF
cd CARF
```

### 2. Clonar repositórios de código

Clone apenas os repositórios necessários dentro de `PROJECTS/*/SRC-CODE/`:

```bash
# Backend .NET
cd PROJECTS/GEOAPI
git clone https://github.com/Thalesvpr/carf-geoapi.git SRC-CODE

# Frontend React
cd ../GEOWEB
git clone https://github.com/Thalesvpr/carf-geoweb.git SRC-CODE

# Mobile React Native
cd ../REURBCAD
git clone https://github.com/Thalesvpr/carf-reurbcad.git SRC-CODE

# Plugin QGIS
cd ../GEOGIS
git clone https://github.com/Thalesvpr/carf-geogis.git SRC-CODE

# Portal de Docs VitePress
cd ../WEBDOCS
git clone https://github.com/Thalesvpr/carf-webdocs.git SRC-CODE

# Admin Console Next.js
cd ../ADMIN
git clone https://github.com/Thalesvpr/carf-admin.git SRC-CODE
```

### 3. Infraestrutura Local (Docker)

```bash
# PostgreSQL + PostGIS
cd CENTRAL/INTEGRATION/DATABASE
docker-compose up -d

# Keycloak + PostgreSQL
cd ../KEYCLOAK
docker-compose up -d
```

Acesse:
- Keycloak Admin Console: http://localhost:8080 (admin/admin)
- PostgreSQL: localhost:5432 (postgres/postgres)

### 4. Rodar Aplicações

Ver instruções específicas em cada `PROJECTS/*/DOCS/HOW-TO/01-setup-local.md`.

## Documentação

### Portal de Documentação

Acesse a documentação completa em: **https://thalesvpr.github.io/carf-webdocs/**

### Documentação Local

Toda documentação está em markdown neste repositório:

- **CENTRAL/**: Documentação centralizada (arquitetura, requisitos, APIs)
- **PROJECTS/*/DOCS/**: Documentação específica de cada projeto

### Índices Principais

- [Arquitetura](./CENTRAL/ARCHITECTURE/README.md) - Decisões arquiteturais (ADRs)
- [Requisitos](./CENTRAL/REQUIREMENTS/README.md) - Requisitos funcionais e não-funcionais
- [API Reference](./CENTRAL/API/README.md) - Endpoints REST
- [Regras de Negócio](./CENTRAL/BUSINESS-RULES/README.md) - Processos REURB (Lei 13.465)
- [Keycloak](./CENTRAL/INTEGRATION/KEYCLOAK/README.md) - Autenticação OAuth2/OIDC
- [Database](./CENTRAL/INTEGRATION/DATABASE/README.md) - PostgreSQL + PostGIS
- [Versionamento](./CENTRAL/VERSIONING/README.md) - Git, Branching, Releases

## Stack Tecnológica

### Backend
- **.NET 9** - Framework backend
- **PostgreSQL 16** - Banco de dados relacional
- **PostGIS 3.4** - Extensão geoespacial
- **Keycloak 24** - Autenticação e autorização
- **Entity Framework Core** - ORM
- **MediatR** - CQRS pattern
- **FluentValidation** - Validações
- **Serilog** - Logging estruturado

### Frontend Web
- **React 18** - Biblioteca UI
- **TypeScript 5** - Type safety
- **Vite** - Build tool
- **TanStack Query (React Query)** - Data fetching
- **Tailwind CSS** - Styling
- **Leaflet** - Mapas interativos
- **Zustand** - State management

### Mobile
- **React Native** - Framework mobile
- **TypeScript** - Type safety
- **WatermelonDB** - Banco offline
- **React Navigation** - Navegação
- **React Native Maps** - Mapas nativos
- **NetInfo** - Detecção de conectividade

### QGIS Plugin
- **Python 3.11** - Linguagem
- **PyQGIS** - API QGIS
- **Shapely** - Geometrias
- **requests** - HTTP client

### Admin Console
- **Next.js 14** - Framework React SSR
- **React 18** - UI
- **TypeScript** - Type safety
- **TanStack Query** - Data fetching
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **@keycloak/keycloak-admin-client** - Keycloak Admin API

### Docs Portal
- **VitePress** - Static site generator
- **Vue 3** - Framework
- **Markdown** - Conteúdo
- **Mermaid** - Diagramas

## Legislação

- **Lei 13.465/2017** - Regularização Fundiária Urbana (REURB)
- **Lei 10.257/2001** - Estatuto da Cidade
- **Decreto 9.310/2018** - Regulamentação REURB

Ver [CENTRAL/WORKFLOWS/](./CENTRAL/WORKFLOWS/) para processos detalhados.

## Contribuindo

1. Fork o repositório apropriado (carf-docs, carf-geoapi, etc.)
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit seguindo [Conventional Commits](./CENTRAL/VERSIONING/GIT/03-commit-conventions.md)
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

Ver [CENTRAL/VERSIONING/GIT/04-pr-guidelines.md](./CENTRAL/VERSIONING/GIT/04-pr-guidelines.md) para guidelines completos.

## Licença

Copyright © 2024-2026 - Sistema CARF

## Suporte

- **Documentação**: https://thalesvpr.github.io/carf-webdocs/
- **Issues**: Abrir no repositório correspondente
- **Troubleshooting**: Ver `PROJECTS/*/DOCS/HOW-TO/` de cada projeto

---

**Última atualização:** 2026-01-09
**Versão:** v1.0.0 MVP
