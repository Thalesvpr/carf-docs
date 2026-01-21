---
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# Catálogo de Repositórios

Catálogo completo dos repositórios Git do ecossistema CARF. Este documento é a fonte única de verdade para identificar todos os repositórios, seus propósitos e responsáveis. Atualmente o CARF utiliza **7 repositórios ativos** no GitHub, organizados em arquitetura polyrepo onde cada projeto tem deploy, versionamento e ownership independentes.

## Repositórios Ativos

| Repositório | Descrição | Stack | Ownership | Status |
|-------------|-----------|-------|-----------|--------|
| **carf-docs** | Documentação central SSOT com especificações, requisitos, arquitetura e padrões do sistema | Markdown, Obsidian | Tech Writers | Ativo |
| **carf-geoapi** | Backend .NET 9 com API REST geoespacial, autenticação JWT e integração PostGIS | .NET 9, PostgreSQL, PostGIS | Backend Team | Ativo |
| **carf-geoweb** | Portal web React para analistas com gestão de processos REURB e visualização de mapas | React, TypeScript, Leaflet | Frontend Team | Ativo |
| **carf-reurbcad** | App mobile React Native para coleta de dados em campo com suporte offline-first | React Native, TypeScript, SQLite | Mobile Team | Ativo |
| **carf-geogis** | Plugin QGIS Python para análises espaciais avançadas e integração com fluxo de trabalho GIS | Python, QGIS API | GIS Team | Ativo |
| **carf-webdocs** | Portal público VitePress com documentação técnica e guias de usuário | VitePress, Vue, TypeScript | Docs Team | Ativo |
| **carf-keycloak** | Customizações Keycloak incluindo temas PT-BR, validação CPF e configuração de realm OAuth2 | Keycloak, FreeMarker, Java, Docker | Backend Team | Ativo |

## Repositórios Planejados

| Repositório | Descrição | Stack | Ownership | Previsão |
|-------------|-----------|-------|-----------|----------|
| **carf-tscore** | Biblioteca TypeScript compartilhada com value objects, validações e tipos do domínio CARF | TypeScript, Bun | Frontend Team | Q1 2026 |
| **carf-admin** | Console administrativo Next.js para gestão de usuários, tenants e configurações do sistema | Next.js, TypeScript | Admin Team | Q2 2026 |

## URLs dos Repositórios

Todos os repositórios estão hospedados na organização GitHub do projeto.

| Repositório | URL | Visibilidade |
|-------------|-----|--------------|
| carf-docs | https://github.com/Thalesvpr/carf-docs | Privado |
| carf-geoapi | https://github.com/Thalesvpr/carf-geoapi | Privado |
| carf-geoweb | https://github.com/Thalesvpr/carf-geoweb | Privado |
| carf-reurbcad | https://github.com/Thalesvpr/carf-reurbcad | Privado |
| carf-geogis | https://github.com/Thalesvpr/carf-geogis | Privado |
| carf-webdocs | https://github.com/Thalesvpr/carf-webdocs | Privado |
| carf-keycloak | https://github.com/Thalesvpr/carf-keycloak | Privado |

## Estrutura Local

Cada repositório de código deve ser clonado na pasta SRC-CODE correspondente dentro de PROJECTS/ no repositório carf-docs. Esta estrutura mantém documentação e código organizados permitindo trabalho simultâneo em múltiplos projetos.

| Projeto | Caminho Local | Repositório |
|---------|---------------|-------------|
| Backend API | PROJECTS/GEOAPI/SRC-CODE/carf-geoapi | carf-geoapi |
| Frontend Web | PROJECTS/GEOWEB/SRC-CODE/carf-geoweb | carf-geoweb |
| Mobile App | PROJECTS/REURBCAD/SRC-CODE/carf-reurbcad | carf-reurbcad |
| Plugin QGIS | PROJECTS/GEOGIS/SRC-CODE/carf-geogis | carf-geogis |
| Portal Docs | PROJECTS/WEBDOCS/SRC-CODE/carf-webdocs | carf-webdocs |
| Auth Keycloak | PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak | carf-keycloak |
| Lib TypeScript | PROJECTS/LIB/TS/TSCORE/SRC-CODE/carf-tscore | carf-tscore |
| Admin Console | PROJECTS/ADMIN/SRC-CODE/carf-admin | carf-admin |

## Dependências entre Repositórios

O diagrama de dependências mostra como os repositórios se relacionam. carf-geoapi é consumido por carf-geoweb, carf-reurbcad e carf-geogis via API REST. carf-keycloak fornece autenticação OAuth2 para todos os frontends. carf-tscore (quando publicado) será consumido por carf-geoweb, carf-reurbcad, carf-admin e carf-webdocs como biblioteca NPM compartilhada.

## Versionamento

Cada repositório segue Semantic Versioning independente. A compatibilidade entre versões é documentada em RELEASES/03-compatibility-matrix.md. Para detalhes sobre a estratégia polyrepo e justificativas, consulte RELEASES/01-polyrepo-strategy.md.
