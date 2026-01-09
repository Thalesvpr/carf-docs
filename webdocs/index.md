---
layout: home

hero:
  name: CARF
  text: Sistema de Regularização Fundiária Urbana
  tagline: Documentação completa para toda a equipe
  actions:
    - theme: brand
      text: 📋 Área Product/Business
      link: /docs/
    - theme: alt
      text: 💻 Área Desenvolvedores
      link: /dev/

features:
  - icon: 📋
    title: Para Product Owners
    details: Requisitos, funcionalidades, roadmap e processos REURB
    link: /docs/
  - icon: 💻
    title: Para Desenvolvedores
    details: Setup, arquitetura, API, database e guias técnicos
    link: /dev/
  - icon: 🏗️
    title: Arquitetura Polyrepo
    details: 6 repositórios independentes com documentação centralizada
  - icon: 🔐
    title: Multi-Tenancy Seguro
    details: Row-Level Security (RLS) com PostgreSQL + Keycloak OAuth2
  - icon: 📱
    title: Mobile Offline-First
    details: Sincronização incremental com WatermelonDB
  - icon: 🗺️
    title: Integração GIS
    details: PostGIS + Plugin QGIS Python para operações geoespaciais
---

## Visão Geral

O CARF é um sistema completo para gestão de processos de regularização fundiária urbana (REURB) conforme a Lei 13.465/2017. O projeto segue arquitetura polyrepo com:

- **GEOAPI**: Backend .NET 9 com Clean Architecture e CQRS
- **GEOWEB**: Frontend React com TypeScript e Feature-Sliced Design
- **REURBCAD**: Mobile React Native com estratégia offline-first
- **GEOGIS**: Plugin QGIS Python para operações geoespaciais
- **WEBDOCS**: Portal de documentação VitePress (você está aqui!)

## Repositórios

| Repositório | Descrição | URL |
|-------------|-----------|-----|
| **carf-docs** | Documentação central (SSOT) | [GitHub](https://github.com/Thalesvpr/carf-docs) |
| **carf-geoapi** | Backend .NET 9 | [GitHub](https://github.com/Thalesvpr/carf-geoapi) |
| **carf-geoweb** | Frontend React | [GitHub](https://github.com/Thalesvpr/carf-geoweb) |
| **carf-reurbcad** | Mobile React Native | [GitHub](https://github.com/Thalesvpr/carf-reurbcad) |
| **carf-geogis** | Plugin QGIS Python | [GitHub](https://github.com/Thalesvpr/carf-geogis) |
| **carf-webdocs** | Portal de documentação | [GitHub](https://github.com/Thalesvpr/carf-webdocs) |

## Início Rápido

```bash
# Clone a documentação
git clone https://github.com/Thalesvpr/carf-docs.git CARF
cd CARF

# Clone os projetos que você precisa
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE
```

Consulte a [documentação completa](https://github.com/Thalesvpr/carf-docs) para mais detalhes.
