---
modules: [GEOWEB, GEOGIS]
epic: compatibility
---

# RF-034: Criar Comunidade

Usuários com role ADMIN podem criar novas comunidades no tenant onde formulário inclui campos obrigatórios nome descritivo tipo de comunidade (selecionado de enum predefinido) município e estado através de dropdowns hierárquicos população estimada área aproximada e informações complementares relevantes, geometria (polígono) opcional podendo ser definida posteriormente onde se fornecida usuário desenha boundary da comunidade diretamente no mapa interativo utilizando ferramentas de desenho (polígono livre circle rectangle) com snap e validações topológicas básicas garantindo polígono fechado e válido, upload de shapefile ou KML inicial como alternativa ao desenho manual onde arquivo importado é parseado convertido para GeoJSON validado geometricamente e armazenado como geometria oficial da comunidade facilitando migração de dados existentes ou integração com levantamentos externos, implementação em módulos GEOWEB e GEOAPI com wizard multi-step guiando através de etapas de dados básicos definição de geometria configurações avançadas e confirmação final com preview.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
