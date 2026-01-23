---
id: UC-001-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-001-FA-002: Importar Geometria de GPS

Fluxo alternativo do UC-001 para importar geometria de coordenadas coletadas externamente.

## Condicao

No passo 5 do UC-001, usuario possui coordenadas previamente coletadas via GPS externo ou levantamento.

## Fluxo

1. Usuario clica em Importar Coordenadas
2. Sistema abre modal com textarea e seletor de formato
3. Usuario seleciona formato (GeoJSON, WKT, KML ou coordenadas textuais)
4. Usuario cola string com coordenadas
5. Sistema valida sintaxe e converte para formato interno
6. Sistema renderiza poligono no mapa com destaque visual
7. Sistema exibe preview (area, vertices, bbox)
8. Usuario confirma clicando Aceitar

## Validacoes

- Poligono fechado (primeiro ponto igual ao ultimo)
- Minimo 3 vertices unicos
- Sem auto-intersecoes
- Coordenadas dentro do Brasil
- Area minima 10m²

## Retorno

Volta ao passo 6 do UC-001 com geometria importada e validada.
