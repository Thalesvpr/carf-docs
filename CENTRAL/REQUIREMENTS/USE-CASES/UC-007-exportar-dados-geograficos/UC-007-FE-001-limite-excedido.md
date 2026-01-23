---
id: UC-007-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-007-FE-001: Limite de Registros Excedido

Fluxo de excecao do UC-007 quando quantidade de registros ultrapassa limite maximo.

## Condicao

No passo 10 do UC-007, sistema detecta mais de 10.000 registros a exportar.

## Fluxo

1. Sistema conta registros a exportar
2. Sistema detecta limite excedido
3. Sistema bloqueia exportacao
4. Sistema exibe modal com erro e quantidade atual
5. Sistema oferece sugestoes para reduzir escopo
6. Usuario ajusta filtros e retenta

## Sugestoes ao Usuario

- Filtrar por comunidade especifica
- Reduzir periodo de tempo
- Filtrar por status (apenas aprovados)
- Dividir exportacao em lotes

## Retorno

Exportacao bloqueada. Usuario refina filtros ate respeitar limite.

## Pos-condicoes

- Nenhum recurso consumido com exportacao invalida
- Usuario orientado sobre como prosseguir
