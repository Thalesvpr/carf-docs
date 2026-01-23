---
id: UC-003-FE-003
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-003-FE-003: Soma de Percentuais Excedida

Fluxo de excecao do UC-003 quando soma de percentuais ultrapassa 100%.

## Condicao

No passo 11 do UC-003, soma dos percentuais de todos titulares incluindo novo vinculo ultrapassa 100%.

## Fluxo

1. Sistema calcula soma dos percentuais existentes
2. Sistema detecta que soma com novo percentual excede 100%
3. Sistema exibe modal com calculo visual
4. Sistema mostra titulares atuais com percentuais
5. Sistema informa percentual maximo permitido
6. Usuario escolhe acao

## Acoes Disponiveis

- **Ajustar Automaticamente**: Sistema preenche com percentual maximo permitido
- **Editar Manualmente**: Usuario informa novo valor
- **Redistribuir Percentuais**: Abre tela para ajustar todos titulares
- **Cancelar**: Aborta operacao

## Retorno

Usuario ajusta percentual e tenta novamente, ou cancela operacao.
