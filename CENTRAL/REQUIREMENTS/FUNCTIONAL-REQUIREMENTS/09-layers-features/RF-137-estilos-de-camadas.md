---
modules: [GEOWEB, GEOGIS]
epic: performance
---

# RF-137: Estilos de Camadas

Este requisito estabelece que cada camada GIS deve suportar configuração detalhada de estilos visuais controlando como features são renderizadas no mapa permitindo diferenciação visual entre layers e adequação a contextos específicos de visualização, onde estilos incluem propriedades de cor espessura opacidade e simbologia. O sistema deve permitir configuração de fill color definindo cor de preenchimento para polígonos através de seletor de cores ou código hexadecimal RGB, stroke color especificando cor das bordas de polígonos e cor de linhas em features LineString, e stroke width configurando espessura de bordas e linhas em pixels garantindo que elementos sejam visíveis sem sobrecarregar visualização. A interface deve incluir controle de opacidade configurável para fill e stroke permitindo criar overlays semitransparentes que revelam camadas subjacentes, útil para análises que requerem visualização simultânea de múltiplas informações espaciais sobrepostas. Para camadas de pontos Point layers, o sistema deve permitir seleção de ícones de biblioteca predefinida ou upload de ícones customizados, onde ícones são renderizados como marcadores no mapa em tamanho configurável. Os estilos configurados devem ser armazenados como JSON no modelo da camada e aplicados consistentemente em toda renderização. A funcionalidade deve estar disponível nos módulos GEOWEB através de interface de configuração visual e GEOAPI armazenando estilos no modelo de camadas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
