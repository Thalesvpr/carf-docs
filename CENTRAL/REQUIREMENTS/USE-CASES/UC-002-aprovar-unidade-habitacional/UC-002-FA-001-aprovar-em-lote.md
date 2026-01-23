---
id: UC-002-FA-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-002-FA-001: Aprovar em Lote

Fluxo alternativo do UC-002 para aprovar multiplas unidades simultaneamente.

## Condicao

No passo 3 do UC-002, MANAGER deseja aprovar varias unidades de uma vez.

## Fluxo

1. MANAGER marca checkbox em multiplas unidades na lista (max 50)
2. Sistema exibe contador de unidades selecionadas
3. Sistema habilita botao Aprovar Selecionadas
4. MANAGER clica em Aprovar Selecionadas
5. Sistema exibe modal de confirmacao com lista resumida
6. MANAGER adiciona comentario opcional
7. MANAGER confirma aprovacao
8. Sistema processa cada unidade individualmente
9. Sistema coleta resultados de sucesso e falha
10. Sistema exibe resumo com estatisticas

## Resultado

- Unidades aprovadas sao removidas da lista
- Unidades com falha permanecem para retry individual
- Notificacoes agrupadas por criador

## Retorno

Atualiza lista removendo sucessos e mantendo falhas para tratamento individual.
