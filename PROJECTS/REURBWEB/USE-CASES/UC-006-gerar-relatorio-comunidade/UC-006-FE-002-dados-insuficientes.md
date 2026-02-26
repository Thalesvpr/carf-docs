---
id: UC-006-FE-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-006-FE-002: Dados Insuficientes

Fluxo de excecao do UC-006 quando comunidade nao possui dados no periodo.

## Condicao

Durante busca de dados do UC-006, sistema detecta que nao ha unidades cadastradas no periodo selecionado.

## Fluxo

1. Sistema executa busca de dados
2. Sistema detecta resultado vazio
3. Sistema cancela geracao do relatorio
4. Sistema notifica usuario com diagnostico
5. Sistema oferece sugestoes de acao

## Causas Comuns

- Comunidade recem-criada sem levantamento
- Periodo selecionado muito restrito
- Unidades cadastradas em outra comunidade

## Sugestoes ao Usuario

- Ajustar periodo para intervalo maior
- Verificar se levantamento foi realizado
- Verificar se comunidade correta foi selecionada

## Retorno

Job cancelado. Usuario notificado com diagnostico e sugestoes de acao.
