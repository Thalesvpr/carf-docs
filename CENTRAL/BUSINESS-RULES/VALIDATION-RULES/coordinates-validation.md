# Coordinates Validation

Regra de validação de coordenadas geográficas garantindo que pontos estão dentro de bounds válidos do Brasil e sistemas de coordenadas corretos onde validação inclui verificação de latitude (-33.75 a +5.27 graus cobrindo extremos do território brasileiro), longitude (-73.99 a -28.84 graus), sistema de coordenadas (WGS84 padrão GPS ou SIRGAS2000 oficial Brasil), e transformação entre sistemas quando necessário preservando precisão. Coordenadas podem ser fornecidas em graus decimais (formato padrão -23.550520 -46.633308) ou graus minutos segundos convertidos para decimal antes de armazenamento e cálculos espaciais. Validação de bounds Brasil considera margem de segurança de 1 grau em cada direção para acomodar ilhas oceânicas e zonas econômicas exclusivas evitando rejeição de coordenadas válidas em extremidades do território. Datum de referência oficial brasileiro é SIRGAS2000 (Sistema de Referência Geocêntrico para as Américas) compatível com WGS84 usado por GPS comerciais com diferença menor que 1 metro na maioria dos casos permitindo uso intercambiável para aplicações de regularização fundiária urbana onde precisão de metros é suficiente.

**Bounds válidos Brasil (com margem):**
- Latitude: -34.0° a +6.0° (extremos: Arroio Chuí RS +5.27° até Monte Caburaí RR)
- Longitude: -75.0° a -28.0° (extremos: Nascente Rio Moa AC -73.99° até Ponta do Seixas PB -34.79°)

**Sistemas de coordenadas aceitos:**
- WGS84 (World Geodetic System 1984) - Padrão GPS internacional
- SIRGAS2000 (Sistema de Referência Geocêntrico para as Américas) - Oficial Brasil desde 2015
- Compatibilidade: WGS84 ≈ SIRGAS2000 com diferença < 1m para Brasil

**Formato aceito:**
- Graus decimais: -23.550520, -46.633308 (preferido)
- Graus minutos segundos: 23°33'01.9"S 46°37'59.9"W (converter para decimal)

**Conversão DMS → Decimal:**

Fórmula calcula decimal igual graus mais minutos dividido por sessenta mais segundos dividido por três mil e seiscentos aplicando sinal negativo se direção for S sul ou W oeste convertendo coordenadas de graus minutos segundos para decimal necessário em cálculos espaciais.

**Exemplo:** 23°33'01.9"S 46°37'59.9"W
- Latitude: -(23 + 33/60 + 1.9/3600) = -23.550527°
- Longitude: -(46 + 37/60 + 59.9/3600) = -46.633305°

**Validações aplicadas:**

1. **Bounds check:**
   - lat >= -34.0 AND lat <= 6.0
   - lng >= -75.0 AND lng <= -28.0

2. **Formato numérico:**
   - Latitude e longitude são números válidos (não NaN, não infinito)
   - Precisão máxima 8 casas decimais (~1mm precisão suficiente)

3. **Ordem correta:**
   - Latitude sempre primeiro, longitude segundo
   - Evitar inversão comum (lng, lat) de algumas bibliotecas

4. **Sistema de coordenadas:**
   - Especificar EPSG:4326 (WGS84) ou EPSG:4674 (SIRGAS2000)
   - Assumir WGS84 se não especificado

**Transformação entre sistemas:**
- WGS84 → SIRGAS2000: Diferença desprezível para Brasil (< 1m)
- UTM → Lat/Lng: Usar biblioteca de transformação (Proj4, GDAL)
- Lat/Lng → UTM: Determinar fuso correto para Brasil (18-25)

**Casos especiais:**

Coordenadas offshore (plataforma continental):
- Aceitar até 200 milhas náuticas da costa
- Validar caso a caso se contexto é territorial

Ilhas oceânicas:
- Fernando de Noroha: -3.8°, -32.4°
- Atol das Rocas: -3.8°, -33.8°
- Trindade: -20.5°, -29.3°
- Ampliar bounds se necessário

**Precisão esperada:**

| Contexto | Precisão | Casas decimais |
|----------|----------|----------------|
| Mobile GPS handheld | ±5-10m | 5 casas |
| Survey GPS pós-processado | ±0.01-0.05m | 7 casas |
| Ortofoto/imagem | ±0.5-2m | 6 casas |

**Mensagens de erro:**
- "Coordenada inválida: latitude fora dos limites do Brasil"
- "Coordenada inválida: longitude fora dos limites do Brasil"
- "Coordenada inválida: formato numérico incorreto"
- "Sistema de coordenadas não suportado: use WGS84 ou SIRGAS2000"

**Validações adicionais contextuais:**

Unidade dentro de Community:
- Validar que coordenada está dentro do boundary da Community
- Calcular distância ao centroide para detectar outliers
- Alertar se unidade está a mais de 1km do centroide

Múltiplos pontos (perímetro):
- Validar que formam polígono fechado
- Primeiro ponto = último ponto
- Mínimo 3 pontos distintos (triângulo)

---

## 🔗 Relacionado

**Domain Model:**
- `../DOMAIN-MODEL/VALUE-OBJECTS/07-geo-point.md` - Value Object implementando validação
- `../DOMAIN-MODEL/ENTITIES/01-unit.md` - Entity usando coordenadas validadas

**IBGE:**
- Sistema de referência SIRGAS2000
- Bounds oficiais do território brasileiro

**Implementações:**
- (caminho de implementação) - Backend .NET
- (caminho de implementação) - Frontend React
- (caminho de implementação) - Mobile React Native

---

**Última atualização:** 2025-01-06
