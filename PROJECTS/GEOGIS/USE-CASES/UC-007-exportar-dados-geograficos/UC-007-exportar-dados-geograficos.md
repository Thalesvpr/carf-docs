---
id: UC-007
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-24
---

# UC-007: Exportar Dados Geograficos

> **Contexto no Workflow:** UC pos-operacional. Exportacao de dados ocorre apos o workflow completo, para integracao com outros sistemas ou analise externa. Ver [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## Atores

- Primario: ANALYST, MANAGER, TECHNICAL_USER
- Secundario: Sistema de filas, Object storage

## Pre-condicoes

- Usuario autenticado com permissao de exportacao
- Dados existentes para exportar

## Fluxo Principal

1. Usuario acessa lista de unidades
2. Usuario aplica filtros desejados (comunidade, status, periodo)
3. Sistema exibe resultados filtrados com contador
4. Usuario clica em Exportar
5. Sistema exibe modal com opcoes de exportacao
6. Usuario seleciona formato (Shapefile, GeoJSON, KML, CSV, Excel)
7. Usuario seleciona sistema de coordenadas
8. Usuario seleciona campos a incluir
9. Usuario confirma exportacao
10. Sistema valida quantidade de registros
11. Sistema cria job de exportacao assincrona
12. Sistema processa dados e gera arquivo
13. Sistema armazena arquivo e gera URL temporaria
14. Sistema notifica usuario quando pronto
15. Usuario baixa arquivo gerado

## Fluxos Alternativos

- FA-001: Exportacao rapida (poucos dados)
- FA-002: Exportar selecao

## Fluxos de Excecao

- FE-001: Limite de registros excedido
- FE-002: Geometrias invalidas
- FE-003: Erro de reprojecao

## Pos-condicoes

- Arquivo exportado disponivel para download
- URL temporaria valida por 24 horas
- Log de exportacao registrado
