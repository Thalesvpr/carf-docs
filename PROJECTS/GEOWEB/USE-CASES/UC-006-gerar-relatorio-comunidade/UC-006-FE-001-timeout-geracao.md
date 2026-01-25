---
id: UC-006-FE-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-006-FE-001: Timeout de Geracao

Fluxo de excecao do UC-006 quando geracao excede tempo limite.

## Condicao

Durante processamento assincrono do UC-006, job excede timeout configurado (10 minutos).

## Fluxo

1. Sistema monitora tempo de execucao do job
2. Sistema detecta timeout excedido
3. Sistema cancela job em execucao
4. Sistema registra erro para debug
5. Sistema notifica usuario sobre falha
6. Sistema oferece sugestoes de ajuste

## Causas Comuns

- Comunidade muito grande (mais de 5000 unidades)
- Secao de mapa com muitas geometrias
- Recursos do servidor sobrecarregados

## Sugestoes ao Usuario

- Reduzir periodo selecionado
- Desmarcar secoes complexas (Mapa)
- Tentar novamente em horario de menor uso

## Retorno

Job cancelado. Usuario notificado com sugestoes de ajuste para nova tentativa.
