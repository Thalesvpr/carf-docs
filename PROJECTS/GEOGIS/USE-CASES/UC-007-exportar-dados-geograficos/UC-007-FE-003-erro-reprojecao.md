---
id: UC-007-FE-003
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-007-FE-003: Erro de Reprojecao

Fluxo de excecao do UC-007 quando conversao de sistema de coordenadas falha.

## Condicao

Durante processamento do UC-007, sistema nao consegue converter coordenadas para SRID solicitado.

## Fluxo

1. Sistema tenta reprojetar geometrias
2. Sistema detecta falha na conversao
3. Sistema aplica fallback mantendo SRID original
4. Sistema adiciona metadado informando SRID real
5. Sistema marca job como concluido com ressalvas
6. Sistema notifica usuario sobre limitacao

## Causas Comuns

- SRID desconhecido no banco de dados
- Parametros de datum ausentes
- Corrupcao de metadados de projecao

## Fallback

- Geometrias mantidas no SRID original
- Arquivo .prj atualizado com SRID real
- Usuario pode reprojetar manualmente em QGIS

## Retorno

Arquivo gerado com SRID original. Warning informando que reprojecao nao foi aplicada.

## Pos-condicoes

- Arquivo valido com coordenadas no sistema original
- Usuario orientado sobre reprojecao manual
