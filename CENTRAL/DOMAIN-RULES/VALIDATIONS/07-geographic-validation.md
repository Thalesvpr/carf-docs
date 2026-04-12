---
type: leaf
status: approved
updated: 2026-01-25
---

# Geographic Validation

Validacoes geograficas do CARF implementadas via funcoes espaciais do banco de dados. Coordenadas devem estar dentro de limites validos com latitude entre -90 e +90, longitude entre -180 e +180, e ponto contido no poligono de fronteira do Brasil.

Poligonos devem ter topologia valida sem auto-intersecao, buracos corretamente definidos, e anel externo em sentido horario. Area minima de 20 metros quadrados e maxima de 250 metros quadrados para REURB-S ou 500 metros quadrados para REURB-E. Deteccao de sobreposicao retorna conflitos entre poligonos com tolerancia de 0.5 metros quadrados para pequenos gaps. Validacao topologica verifica gaps entre unidades adjacentes, slivers e dangles.
