---
type: readme
status: review
description: "README usa listas/tabelas ao inves de prosa densa com links inline."
updated: 2026-02-21
---

# API Reference - @carf/geoapi-client

## Overview

> **Nota:** Os endpoints abaixo sao auto-gerados pelo orval a partir do `swagger.json` da GEOAPI. Os 22 documentos individuais nesta pasta servem como **referencia de design** e serao gradualmente substituidos pelo swagger como fonte de verdade. Para a lista atualizada de endpoints, consulte o swagger da API em `http://localhost:5127/swagger`.

Referencia dos endpoints da GEOAPI organizados por dominio.

## Endpoints Documentados

| API | Arquivo | Descricao |
|:----|:--------|:----------|
| Units CRUD | [01a-units-crud-api.md](./01a-units-crud-api.md) | Listagem, busca por ID e criacao de unidades |
| Units Update | [01b-units-update-api.md](./01b-units-update-api.md) | Campos do DTO, update, patch e delete |
| Units Workflow | [01c-units-workflow-api.md](./01c-units-workflow-api.md) | Submit, approve, reject e exportacao |
| Units Holders | [01d-units-holders-api.md](./01d-units-holders-api.md) | Vincular, desvincular e atualizar titulares |
| Holders CRUD | [02a-holders-crud-api.md](./02a-holders-crud-api.md) | Listagem, busca, criacao, update e delete |
| Holders Search | [02b-holders-search-import-api.md](./02b-holders-search-import-api.md) | Campos do DTO, busca por CPF/CNPJ e importacao |
| Communities CRUD | [03a-communities-crud-api.md](./03a-communities-crud-api.md) | Listagem, busca, criacao, update e delete |
| Communities Stats | [03b-communities-stats-geo-api.md](./03b-communities-stats-geo-api.md) | Campos do DTO, estatisticas e geometria |
| Legitimation Endpoints | [04a-legitimation-endpoints.md](./04a-legitimation-endpoints.md) | Endpoints, listagem e busca por ID |
| Legitimation Workflow | [04b-legitimation-criacao-workflow.md](./04b-legitimation-criacao-workflow.md) | Criacao, acoes de workflow e fluxo de status |
| Legitimation Docs | [04c-legitimation-historico-documentos.md](./04c-legitimation-historico-documentos.md) | Historico, documentos e certificado |
| Documents Upload | [05a-documents-upload-download.md](./05a-documents-upload-download.md) | Upload, download e estrutura do Document |
| Documents Listagem | [05b-documents-listagem-tipos.md](./05b-documents-listagem-tipos.md) | Listagem, metadados, delete e tipos |
| Reports Exportacao | [06a-reports-exportacao.md](./06a-reports-exportacao.md) | Exportacao de unidades, posseiros e estatisticas |
| Reports Download | [06b-reports-status-download.md](./06b-reports-status-download.md) | Status, download, helpers e formatos de saida |
| Orthofotos | [07-orthofotos-api.md](./07-orthofotos-api.md) | Upload, processamento e gerenciamento de ortofotos |
| Sync | [08-sync-api.md](./08-sync-api.md) | Sincronizacao offline bidirecional |
| Packages | [09-packages-api.md](./09-packages-api.md) | Pacotes de campo para trabalho offline |
| Teams | [10-teams-api.md](./10-teams-api.md) | Gerenciamento de equipes de campo |
| Auth Keys | [11-auth-keys-api.md](./11-auth-keys-api.md) | Chaves de API para integracao server-to-server |
| Blocks | [12a-blocks-api.md](./12a-blocks-api.md) | Quadras - subdivisoes espaciais de comunidades |
| Plots | [12b-plots-api.md](./12b-plots-api.md) | Lotes - subdivisoes de quadras com vinculo a unidades |

## Configuracao do Cliente

O client e criado via `createApiClient({ baseURL, getToken, getTenantId })`. Hooks React Query e funcoes vanilla sao importados diretamente do pacote. Ver HOW-TO/01-getting-started para exemplos.

<!-- CARF-INDEX-START -->
> **Indice gerado automaticamente.** Nao edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (22)

| Documento | Status |
|-----------|--------|
| [Units API - Operacoes CRUD Basicas](./01a-units-crud-api.md) | review |
| [Units API - Criacao, Atualizacao e Remocao](./01b-units-update-api.md) | review |
| [Units API - Workflow e Exportacao](./01c-units-workflow-api.md) | review |
| [Units API - Gestao de Titulares na Unidade](./01d-units-holders-api.md) | review |
| [Holders API - Operacoes CRUD](./02a-holders-crud-api.md) | review |
| [Holders API - Campos, Busca e Importacao](./02b-holders-search-import-api.md) | review |
| [Communities API - Operacoes CRUD](./03a-communities-crud-api.md) | review |
| [Communities API - Campos, Estatisticas e Geometria](./03b-communities-stats-geo-api.md) | review |
| [Legitimation API - Endpoints e Consultas](./04a-legitimation-endpoints.md) | review |
| [Legitimation API - Criacao e Workflow](./04b-legitimation-criacao-workflow.md) | review |
| [Legitimation API - Historico e Documentos](./04c-legitimation-historico-documentos.md) | review |
| [Documents API - Upload e Download](./05a-documents-upload-download.md) | review |
| [Documents API - Listagem e Tipos](./05b-documents-listagem-tipos.md) | review |
| [Reports API - Solicitacao de Exportacao](./06a-reports-exportacao.md) | review |
| [Reports API - Status, Download e Formatos](./06b-reports-status-download.md) | review |
| [Orthofotos API - Gerenciamento de Ortofotos](./07-orthofotos-api.md) | review |
| [Sync API - Sincronizacao Offline](./08-sync-api.md) | review |
| [Field Packages API - Pacotes de Campo](./09-packages-api.md) | review |
| [Teams API - Gerenciamento de Equipes](./10-teams-api.md) | review |
| [Auth Keys API - Gerenciamento de Chaves de API](./11-auth-keys-api.md) | review |
| [Blocks API - Gerenciamento de Quadras](./12a-blocks-api.md) | review |
| [Plots API - Gerenciamento de Lotes](./12b-plots-api.md) | review |

<!-- CARF-INDEX-END -->
