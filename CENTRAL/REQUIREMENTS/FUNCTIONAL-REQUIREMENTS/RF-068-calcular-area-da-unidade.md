---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# RF-068: Calcular Área da Unidade

O sistema deve calcular automaticamente a área de cada unidade habitacional a partir de sua geometria espacial, onde o cálculo é realizado no backend utilizando funções nativas do PostGIS (ST_Area) garantindo precisão e performance otimizada através de operações diretamente no banco de dados. A área é calculada em metros quadrados utilizando projeção adequada que preserve medidas de superfície evitando distorções causadas por cálculos em coordenadas geográficas não projetadas, onde configuração de SRID apropriado garante resultados precisos independente da região geográfica. O campo de área é atualizado automaticamente sempre que a geometria da unidade for criada ou modificada, através de triggers de banco de dados ou hooks de modelo que garantem sincronização perfeita entre geometria e área calculada sem necessidade de intervenção manual. O frontend exibe a área formatada com separador de milhares e duas casas decimais (exemplo: 1.234,56 m²) melhorando legibilidade e compreensão dos valores, onde apresentação consistente facilita comparações e análises quantitativas por parte de usuários e gestores durante cadastramento e consultas de unidades.

---

**Última atualização:** 2025-12-30
