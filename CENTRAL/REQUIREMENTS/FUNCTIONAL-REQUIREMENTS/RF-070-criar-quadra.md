---
modules: [GEOWEB]
epic: units
---

# RF-070: Criar Quadra

O sistema deve permitir que usuários criem quadras representando agrupamentos lógicos e espaciais de unidades habitacionais, onde formulário de criação captura campos essenciais como código único identificador, nome descritivo e comunidade à qual a quadra pertence. A geometria da quadra é opcional permitindo cadastro inicial sem delimitação espacial quando informação geométrica ainda não está disponível, mas quando fornecida deve representar o contorno externo que engloba todas as unidades agrupadas na quadra. Durante ou após criação, usuários podem vincular unidades existentes à quadra estabelecendo hierarquia organizacional comunidade-quadra-unidade que facilita navegação, consultas agregadas e análises territoriais em diferentes níveis de granularidade. Este recurso é implementado nos módulos GEOWEB e GEOAPI suportando gestão hierárquica do território urbanizado, onde quadras funcionam como entidades intermediárias entre comunidades (nível macro) e unidades individuais (nível micro), permitindo organização compatível com nomenclaturas cadastrais tradicionais e facilitando comunicação com moradores que frequentemente se referenciam por quadra ao invés de coordenadas ou códigos técnicos de unidades.

---

**Última atualização:** 2025-12-30
