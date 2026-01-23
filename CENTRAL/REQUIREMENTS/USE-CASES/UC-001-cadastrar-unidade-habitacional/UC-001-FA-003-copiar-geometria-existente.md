---
id: UC-001-FA-003
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-001-FA-003: Copiar Geometria de Unidade Existente

Fluxo alternativo do UC-001 para criar unidade copiando geometria de unidade proxima.

## Condicao

No passo 5 do UC-001, usuario deseja criar unidade adjacente ou similar a uma ja cadastrada.

## Fluxo

1. Usuario clica em Copiar de Unidade Existente
2. Sistema exibe lista de unidades proximas (raio 500m, max 20)
3. Usuario filtra por codigo, endereco ou status se necessario
4. Usuario seleciona unidade desejada
5. Sistema destaca geometria selecionada no mapa
6. Usuario confirma clicando Copiar Geometria
7. Sistema duplica coordenadas aplicando offset para evitar sobreposicao
8. Sistema renderiza geometria copiada no mapa
9. Usuario ajusta vertices manualmente se necessario
10. Usuario aceita copia

## Retorno

Volta ao passo 6 do UC-001 com geometria copiada e ajustada.
