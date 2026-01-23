---
id: UC-008-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-008-FE-001: Arquivo Invalido

Fluxo de excecao do UC-008 quando arquivo uploadado nao e Shapefile valido.

## Condicao

No passo 5 do UC-008, sistema detecta que arquivo nao contem componentes obrigatorios.

## Fluxo

1. Sistema tenta extrair e validar arquivo
2. Sistema detecta problema de estrutura
3. Sistema bloqueia importacao
4. Sistema exibe modal com erro detalhado
5. Sistema oferece orientacoes de correcao
6. Usuario corrige arquivo e tenta novamente

## Problemas Detectados

- ZIP nao contem arquivo .shp
- ZIP nao contem arquivo .dbf
- Arquivos .shp e .dbf com nomes diferentes
- Magic number invalido (arquivo corrompido)
- Versao Shapefile nao suportada

## Orientacoes ao Usuario

- Incluir arquivos obrigatorios (.shp, .dbf, .shx)
- Verificar se arquivos pertencem ao mesmo Shapefile
- Reexportar do QGIS com todos componentes

## Retorno

Upload bloqueado. Usuario corrige arquivo e tenta novamente.
