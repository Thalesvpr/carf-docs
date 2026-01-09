# Geometry Validation

Regra de validação de geometrias espaciais garantindo que polígonos representando unidades habitacionais comunidades e blocos são válidos topologicamente e compatíveis com requisitos de regularização fundiária onde validação inclui verificação de polígono fechado (primeiro ponto igual ao último), ausência de auto-interseção (arestas não se cruzam), sentido de rotação correto (anti-horário para exterior horário para buracos), área calculada dentro de limites legais (REURB-S até 250m² REURB-E até 500m²), perímetro coerente com área, e detecção de sobreposição entre geometrias adjacentes. Geometrias podem ser fornecidas em formatos padrão WKT (Well-Known Text) ou GeoJSON sendo convertidas internamente para representação canônica antes de validação e armazenamento. Cálculo de área utiliza fórmula de Shoelace (método do determinante) para polígonos simples em coordenadas planas projetadas considerando que para áreas pequenas (< 1km²) distorção de projeção é desprezível, caso contrário transformar para projeção equivalente ou usar cálculo esférico. Validação de overlap entre unidades detecta sobreposição de polígonos indicando conflito fundiário ou erro de cadastro onde overlap maior que threshold de tolerância (tipicamente 1m² ou 1% da menor área) dispara alerta para revisão manual.

**Tipos de geometria suportados:**
- Polygon (polígono simples sem buracos) - Caso mais comum para unidades
- MultiPolygon (múltiplos polígonos) - Propriedades não contíguas
- Polygon with holes (polígono com buracos internos) - Edificações com pátios

**Validações topológicas obrigatórias:**

1. **Polígono fechado:**
   - Primeiro ponto = último ponto (mesmas coordenadas)
   - Mínimo 4 pontos (3 vértices + fechamento)

2. **Sem auto-interseção:**
   - Nenhuma aresta cruza outra aresta do mesmo polígono
   - Algoritmo: Verificar interseção de cada par de arestas não adjacentes

3. **Sentido de rotação:**
   - Anel exterior: anti-horário (CCW - counter-clockwise)
   - Anéis interiores (buracos): horário (CW - clockwise)
   - Determinar sentido: Somar (x2-x1)(y2+y1) para cada aresta, se negativo = CCW

4. **Área válida:**
   - Área > 0 (não degenerado)
   - Área >= área mínima (ex: 20m² para construção habitável)
   - Área <= área máxima (250m² REURB-S, 500m² REURB-E)

5. **Vértices distintos:**
   - Nenhum vértice duplicado exceto primeiro/último
   - Distância entre vértices consecutivos > threshold (ex: 0.1m)

**Cálculo de área (Fórmula de Shoelace):**

Para polígono com n vértices (x₁,y₁), (x₂,y₂), ..., (xₙ,yₙ):

```
Área = |½ × Σ(xᵢ × yᵢ₊₁ - xᵢ₊₁ × yᵢ)| para i=1 até n-1
```

Onde coordenadas estão em metros (projetadas) para resultado em m²

**Transformação para cálculo:**
- Lat/Lng (EPSG:4326) → UTM zona apropriada (metros)
- Brasil: Fusos UTM 18-25, escolher fuso do centroide
- Exemplo: São Paulo = UTM zona 23S (EPSG:31983)

**Cálculo de perímetro:**

```
Perímetro = Σ distância(vᵢ, vᵢ₊₁) para i=1 até n-1
```

Validar razão área/perímetro² (índice de circularidade) para detectar polígonos muito irregulares

**Detecção de overlap:**

1. **Overlap entre Units:**
   - Calcular interseção de geometrias
   - Área de overlap > threshold (1m² ou 1% menor área)
   - Alertar analista para revisão

2. **Unit fora de Community boundary:**
   - Validar que Unit.geometry está contido em Community.boundary
   - Tolerância: aceitar < 1% da área fora (erro de GPS)

3. **Unit fora de Block (se aplicável):**
   - Validar que Unit.geometry está contido em Block.geometry
   - Mesmo critério de tolerância

**Validações de qualidade:**

Relação área/perímetro:
- Detectar polígonos muito alongados ou irregulares
- Índice de circularidade = 4π × área / perímetro²
- Valores próximos a 1 = circular, < 0.1 = muito irregular

Número de vértices:
- Mínimo: 4 (triângulo + fechamento)
- Máximo razoável: 100 (simplificar se muito complexo)
- Alerta se > 50 vértices (provável digitalização detalhada desnecessária)

Ângulos internos:
- Evitar ângulos muito agudos (< 15°)
- Indicam erro de digitalização ou vértices redundantes

**Formatos de entrada:**

WKT (Well-Known Text):
```
POLYGON((-46.633 -23.550, -46.632 -23.550, -46.632 -23.551, -46.633 -23.551, -46.633 -23.550))
```

GeoJSON:
```json
{
  "type": "Polygon",
  "coordinates": [[
    [-46.633, -23.550],
    [-46.632, -23.550],
    [-46.632, -23.551],
    [-46.633, -23.551],
    [-46.633, -23.550]
  ]]
}
```

**Mensagens de erro:**
- "Geometria inválida: polígono não está fechado"
- "Geometria inválida: auto-interseção detectada"
- "Geometria inválida: sentido de rotação incorreto"
- "Área inválida: excede limite de 250m² para REURB-S"
- "Área inválida: menor que 20m² (área mínima habitável)"
- "Sobreposição detectada com unidade adjacente: 5.2m² (revisar)"
- "Unidade fora do perímetro da comunidade: 12% da área externa"

**Exceções e casos especiais:**

Propriedades não contíguas:
- Usar MultiPolygon ao invés de Polygon
- Cada parte validada individualmente
- Somar áreas de todas partes

Edificações com pátio interno:
- Polygon with holes (anel exterior + anéis interiores)
- Validar sentido de cada anel
- Área = área externa - área buracos

Correção automática:
- Inverter sentido de rotação se incorreto
- Remover vértices duplicados
- Simplificar geometria (reduzir vértices mantendo forma)

---

## 🔗 Relacionado

**Domain Model:**
- `../DOMAIN-MODEL/VALUE-OBJECTS/11-geo-polygon.md` - Value Object implementando validação
- `../DOMAIN-MODEL/ENTITIES/01-unit.md` - Entity usando geometria validada

**LEGITIMATION-RULES:**
- `../LEGITIMATION-RULES/reurb-s-requirements.md` - Limite 250m² área
- `../LEGITIMATION-RULES/reurb-e-requirements.md` - Limite 500m² área

**Implementações:**
- `PROJECTS/GEOAPI/LAYERS/DOMAIN/VALIDATORS/GeometryValidator.cs` - Backend .NET (NetTopologySuite)
- `PROJECTS/GEOWEB/UTILS/validators/geometryValidator.ts` - Frontend React (Turf.js)
- `PROJECTS/GEOGIS/validators/geometry.py` - Plugin QGIS (Shapely)

---

**Última atualização:** 2025-01-06
