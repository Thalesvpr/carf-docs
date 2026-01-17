---
modules: [GEOAPI]
epic: performance
---

# US-061: Ver Sobreposições Visuais

Como analista, quero visualizar unidades com sobreposições geométricas destacadas no mapa para que erros de cadastramento sejam identificados e corrigidos, onde a funcionalidade deve renderizar polígonos que se sobrepõem em cor vermelha diferenciada para destaque visual imediato, garantindo que tooltip ao passar mouse sobre área de sobreposição exiba informações sobre as unidades envolvidas e tamanho da área sobreposta em metros quadrados, permitindo ativação de filtro específico "Apenas sobreposições" que oculta unidades sem problemas geométricos focando análise apenas em casos problemáticos. Esta funcionalidade é implementada pelo módulo GEOWEB com visualização especial de overlaps consumindo GEOAPI através do endpoint GET /api/units/overlaps que utiliza queries PostGIS ST_Overlaps para detectar sobreposições, integrada ao RF-069 (Detecção de Sobreposições Geométricas) para validação de qualidade de dados. Os critérios de aceitação incluem identificação automática de unidades cujas geometrias se sobrepõem através de análise espacial no backend, renderização diferenciada de polígonos com sobreposição destacados em cor vermelha ou laranja no mapa, exibição de tooltip ao hover mostrando códigos das unidades envolvidas na sobreposição e área sobreposta em m², disponibilidade de filtro toggle "Mostrar apenas sobreposições" que oculta unidades sem problemas, listagem lateral opcional mostrando todas sobreposições detectadas com links para navegação rápida no mapa, cálculo preciso de área de interseção utilizando PostGIS ST_Area ST_Intersection, atualização automática de detecção de sobreposições quando geometrias são editadas, e indicação quantitativa de gravidade baseada em percentual de área sobreposta versus área total da unidade. A rastreabilidade conecta esta user story ao RF-069 (Validação de Sobreposições) e ao endpoint GET /api/units/overlaps, garantindo controle de qualidade geométrica dos dados cadastrados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
