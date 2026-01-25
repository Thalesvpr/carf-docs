---
id: UC-008
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-24
workflow: pre-carregamento
---

# UC-008: Importar Shapefile

> **Contexto no Workflow:** UC de pre-carregamento. Importacao de shapefiles e usada para carregar dados iniciais ou complementar dados existentes antes do workflow principal. Ver [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## Atores

- Primario: ADMIN, TECHNICAL_USER
- Secundario: Sistema de filas

## Pre-condicoes

- Usuario autenticado com permissao de importacao
- Arquivo ZIP contendo componentes Shapefile validos

## Fluxo Principal

1. Usuario acessa menu Importar Dados
2. Usuario seleciona tipo de importacao (Unidades ou Features)
3. Sistema exibe wizard de importacao em 3 passos
4. Usuario faz upload de arquivo ZIP com Shapefile
5. Sistema valida componentes obrigatorios (.shp, .dbf, .shx)
6. Sistema exibe quantidade de registros encontrados
7. Usuario avanca para mapeamento de campos
8. Sistema detecta campos do arquivo e sugere mapeamento
9. Usuario ajusta mapeamentos e seleciona comunidade destino
10. Usuario avanca para preview
11. Sistema exibe amostra de dados e mapa com geometrias
12. Sistema valida todas geometrias em background
13. Usuario confirma importacao
14. Sistema cria job de importacao assincrona
15. Sistema processa cada feature validando e inserindo
16. Sistema notifica usuario quando concluido

## Fluxos Alternativos

- FA-001: Importar GeoJSON

## Fluxos de Excecao

- FE-001: Arquivo invalido
- FE-002: SRID desconhecido
- FE-003: Duplicatas detectadas
- FE-004: Geometrias invalidas

## Pos-condicoes

- Unidades criadas em status Draft
- Relatorio de importacao disponivel
- Log de erros para registros nao importados
