---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: units
---

# RF-127: Criar Camada (Layer)

Este requisito estabelece que administradores devem poder criar camadas GIS personalizadas para organizar e visualizar diferentes conjuntos de dados geoespaciais no sistema, onde cada camada representa coleção lógica de features geográficas do mesmo tipo compartilhando schema de atributos e estilo visual. O formulário de criação deve permitir definir nome descritivo da camada e tipo de geometria que features desta camada terão, onde tipos suportados incluem Point para marcadores pontuais, LineString para linhas e trajetos, e Polygon para áreas e polígonos, garantindo que todas features adicionadas posteriormente à camada respeitem tipo de geometria configurado. O sistema deve permitir configuração de estilo visual padrão da camada incluindo cor de preenchimento fill color para polígonos, cor de borda stroke color, espessura de linha stroke width, opacidade e ícone específico para camadas de pontos, onde estilo configurado é aplicado automaticamente a todas features da camada ao renderizar no mapa. A interface deve incluir campo de visibilidade padrão configurando se camada deve estar visível ou oculta quando usuário carrega mapa inicialmente, permitindo controle sobre quais informações são apresentadas imediatamente versus sob demanda. Camadas criadas são específicas do tenant e opcionalmente de comunidade específica dentro do tenant. A funcionalidade deve estar disponível nos módulos GEOWEB através de interface administrativa e GEOAPI via endpoint POST de criação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
