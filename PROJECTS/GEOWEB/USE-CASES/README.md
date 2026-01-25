---
type: readme
status: review
updated: 2026-01-24
---

# USE-CASES - GEOWEB

Casos de uso do portal web GEOWEB para gestao, relatorios e configuracoes do sistema.

## Referencia

Todos os UCs sao complementares ao [WORKFLOW-MESTRE](../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## Casos de Uso por Contexto

### Pre-requisito (antes do workflow)

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-010](./UC-010-configurar-camadas-wms/README.md) | Configurar Camadas WMS | Configuracao de camadas de mapa |

### Administrativo

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-011](./UC-011-gerenciar-equipes-tecnicas/README.md) | Gerenciar Equipes | Gestao de equipes e designacoes |

### Pos-workflow (apos PARTE 3)

| UC | Nome | Descricao |
|----|------|-----------|
| [UC-006](./UC-006-gerar-relatorio-comunidade/README.md) | Gerar Relatorios | Relatorios agregados por comunidade |

## Relacionamentos

- **GEOAPI**: Backend que fornece dados e processa operacoes
- **REURBCAD**: App mobile que coleta dados (PARTE 3)
- **GEOGIS**: Plugin QGIS para georreferenciamento (PARTE 2)
