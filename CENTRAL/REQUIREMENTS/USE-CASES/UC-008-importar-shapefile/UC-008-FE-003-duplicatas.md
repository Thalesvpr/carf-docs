---
id: UC-008-FE-003
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-008-FE-003: Duplicatas Detectadas

Fluxo de excecao do UC-008 quando codigo de unidade ja existe no sistema.

## Condicao

Durante processamento do UC-008, sistema detecta que codigo da unidade ja esta cadastrado.

## Fluxo

1. Sistema tenta criar unidade
2. Sistema verifica unicidade do codigo
3. Sistema detecta codigo ja existente
4. Sistema preserva registro original
5. Sistema pula criacao do duplicado
6. Sistema registra ocorrencia no log
7. Sistema continua com proximos registros
8. Sistema exibe estatisticas ao final

## Causas Comuns

- Reimportacao de arquivo ja processado
- Sobreposicao parcial com dados existentes
- Multiplas equipes cadastrando mesma area

## Comportamento

- Dados existentes nunca sao sobrescritos
- Duplicatas sao ignoradas silenciosamente
- Log permite identificar registros pulados
- Usuario pode reconciliar manualmente

## Retorno

Duplicatas ignoradas. Importacao continua com registros unicos. Log disponivel com detalhes.
