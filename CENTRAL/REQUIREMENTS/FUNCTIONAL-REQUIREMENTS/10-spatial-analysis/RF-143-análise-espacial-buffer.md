---
modules: [GEOAPI]
epic: units
---

# RF-143: Análise Espacial: Buffer

Este requisito estabelece que o sistema deve fornecer funcionalidade de criação de buffer zona de influência ao redor de features permitindo análise de proximidade e identificação de áreas afetadas por elemento geográfico, onde buffer é polígono que engloba todos os pontos a distância especificada ou menor da geometria original. A ferramenta deve aceitar parâmetro de distância em metros especificando raio do buffer a ser criado, onde usuário informa valor numérico e sistema aplica operação de buffer utilizando funções espaciais do PostGIS como ST_Buffer que gera geometria expandida considerando sistema de coordenadas e projeção apropriados para cálculos métricos precisos. O sistema deve gerar polígono buffer como nova geometria que pode ser visualizada temporariamente no mapa para análise visual ou salva como nova feature permanente em camada de destino conforme escolha do usuário, onde opção de salvar cria registro completo com geometria buffer e atributos que podem referenciar feature original. A ferramenta deve suportar aplicação de buffer a features individuais selecionadas ou em lote sobre múltiplas features simultaneamente, onde buffers podem ser unidos em geometria única através de dissolve ou mantidos como polígonos separados conforme necessidade analítica. O resultado deve ser renderizado no mapa com estilo diferenciado permitindo distinguir zona de buffer de features originais. A funcionalidade deve estar disponível nos módulos GEOWEB através de ferramenta de análise e GEOAPI via endpoint de processamento espacial.

---

**Última atualização:** 2025-12-30