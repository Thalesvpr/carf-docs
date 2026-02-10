---
type: readme
status: review
description: "README usa listas/tabelas ao inves de prosa densa com links inline."
updated: 2026-02-08
---

# REURBCAD - Features

Funcionalidades do aplicativo mobile REURBCAD para coleta de dados cadastrais em campo com suporte offline-first.

## Stack Tecnologica

React Native 0.74, Expo SDK 51, TypeScript strict, Zustand (UI state), TanStack Query (server state), WatermelonDB (SQLite offline), Expo Router (navegacao), React Hook Form + Zod (formularios), expo-location (GPS), expo-camera (fotos), react-native-maps (mapas).

## Features Implementadas

- **[01-field-collection.md](./01-field-collection.md)** - Coleta em campo: wizard multi-step (info basica, endereco, area, geolocalizacao, fotos), validacao Zod, persistencia WatermelonDB, queue de sync
- **[02-holder-management.md](./02-holder-management.md)** - Gestao de titulares: CRUD mobile, validacao CPF/RG, vinculacao a unidades (many-to-many), upload de documentos, sync offline
- **[03-offline-sync.md](./03-offline-sync.md)** - Sincronizacao bidirecional: pull/push changes, conflict resolution (last-write-wins), retry com backoff, WatermelonDB sync adapter, background fetch
- **[04-shapefile-import.md](./04-shapefile-import.md)** - Importacao de shapefiles: Expo Document Picker, validacao de topologia e CRS, mapeamento de atributos, preview no mapa, upload async
- **[05-team-management.md](./05-team-management.md)** - Gestao de equipes: visualizacao readonly de teams, membros e lider, comunidades atribuidas, filtragem de unidades por equipe

## Arquitetura Offline-First

O device e a source of truth primaria. Dados sao persistidos localmente no WatermelonDB e sincronizados com a GEOAPI quando ha conexao. A fila de sync garante zero perda de dados mesmo apos semanas offline. Conflitos sao resolvidos via last-write-wins comparando timestamps com suporte a merge manual quando necessario.

## Relacionamento com Workflow

Operacoes de campo seguem o [WORKFLOW-MESTRE PARTE 3](../../../../CENTRAL/WORKFLOW-MESTRE/03-operacao-campo/).

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisao

- ○ [[PROJECTS/REURBCAD/DOCS/FEATURES/01-field-collection.md|Field Collection - Coleta em Campo]]
- ○ [[PROJECTS/REURBCAD/DOCS/FEATURES/02-holder-management.md|Holder Management - Gestao de Titulares]]
- ○ [[PROJECTS/REURBCAD/DOCS/FEATURES/03-offline-sync.md|Offline Sync - Sincronizacao]]
- ○ [[PROJECTS/REURBCAD/DOCS/FEATURES/04-shapefile-import.md|Shapefile Import - Importacao]]
- ○ [[PROJECTS/REURBCAD/DOCS/FEATURES/05-team-management.md|Team Management - Gestao de Equipes]]

<!-- CARF-INDEX-END -->
