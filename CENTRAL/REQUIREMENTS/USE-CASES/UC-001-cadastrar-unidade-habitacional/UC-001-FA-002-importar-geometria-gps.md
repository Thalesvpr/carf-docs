---
modules: [GEOWEB, REURBCAD]
epic: compatibility
---

# UC-001-FA-002: Importar Geometria de GPS

Fluxo alternativo do UC-001 Cadastrar Unidade Habitacional desviando no passo 5 (desenho de geometria) quando usuário possui coordenadas geográficas previamente coletadas via receptor GPS externo, topografia, ou levantamento anterior exportado em formato padrão, onde ao invés de desenhar polígono manualmente usuário clica em botão Importar Coordenadas abrindo modal com textarea grande para colar dados e dropdown seletor de formato suportado (GeoJSON WKT KML Coordenadas Textuais), usuário cola string contendo geometria no formato selecionado como GeoJSON válido estruturado `{"type":"Polygon","coordinates":[[[lng,lat],[lng,lat],...]]}` ou WKT texto `POLYGON((lng lat, lng lat, ...))` ou coordenadas textuais simples uma por linha no formato `latitude longitude` ou `longitude,latitude` com detecção automática de ordem, sistema parsing valida sintaxe do formato detectando erros comuns (vírgulas faltando parênteses não fechados coordenadas fora de range -90/90 lat -180/180 lng ordem invertida lat/lng vs lng/lat), converte internamente para GeoJSON canônico reprojetando se necessário de coordenadas geográficas (EPSG:4326) para projeção do mapa, renderiza polígono importado no mapa com destaque visual (borda azul grossa) centralizando viewport automaticamente para enquadrar geometria completa, exibe prévia de metadados calculados (área número de vértices bbox centro geométrico), e usuário confirma importação clicando Aceitar fechando modal e preenchendo campo geometry do formulário com GeoJSON validado ou cancela descartando importação e retornando para opções de desenho manual. Validações aplicadas incluem polígono deve ser fechado (primeiro ponto igual ao último), mínimo 3 vértices únicos formando área não-degenerada, sem auto-interseções detectadas via algoritmo Bentley-Ottmann, coordenadas dentro de bounds geográficos válidos do Brasil (aproximadamente -34/-5 lat -74/-34 lng), área resultante maior que 10m² conforme regra de negócio RN-003, e se múltiplos polígonos detectados (MultiPolygon) sistema aceita mas exibe warning sugerindo split em unidades separadas.

**Ponto de Desvio:** Passo 5 do UC-001 (desenho de geometria)

**Formatos Suportados:**
- GeoJSON (Polygon ou MultiPolygon)
- WKT (Well-Known Text)
- KML (Keyhole Markup Language Google Earth)
- Coordenadas textuais (lat lng ou lng,lat uma por linha)

**Validações:**
- Sintaxe do formato (parsing sem erros)
- Polígono fechado (primeiro = último ponto)
- Mínimo 3 vértices únicos
- Sem auto-interseções
- Coordenadas em range válido
- Área ≥ 10m²

**Retorno:** Volta ao passo 6 do UC-001 (cálculo de área) com geometria importada validada

---

**Última atualização:** 2025-12-30
