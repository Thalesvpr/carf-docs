---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: cross-cutting
---

# RF-132: Criar Feature

Este requisito especifica que usuários autorizados devem poder criar features geográficas pontos linhas ou polígonos dentro de camadas GIS existentes para registrar elementos espaciais e seus atributos associados, onde processo de criação combina desenho de geometria no mapa com preenchimento de atributos descritivos. A interface deve fornecer ferramentas de desenho no mapa permitindo que usuário trace geometria diretamente sobre visualização cartográfica, onde ferramenta apropriada é ativada conforme tipo de geometria da camada selecionada, incluindo single-click para pontos, múltiplos cliques conectados para linhas, e sequência fechada de cliques para polígonos. Durante ou após desenho, o sistema deve apresentar formulário de atributos customizados específicos da camada permitindo preenchimento de propriedades definidas no schema da layer, onde campos podem incluir texto números datas ou enumerações conforme configuração estabelecida ao criar camada. O sistema deve validar geometria criada garantindo que seja válida conforme regras GIS incluindo ausência de auto-interseções em polígonos fechamento adequado de anéis e conformidade com tipo de geometria esperado pela camada. Após confirmação, feature criada é persistida no banco de dados com geometria em formato PostGIS e atributos em campo JSONB, sendo imediatamente renderizada no mapa com estilo configurado da camada. A funcionalidade deve estar disponível nos módulos GEOWEB através de ferramentas de desenho e GEOAPI via endpoint POST.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
