---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: compatibility
---

# RF-165: Ajustar Sistema de Coordenadas

O sistema permite configurar o SRID (Spatial Reference Identifier) do levantamento topográfico, possibilitando que o usuário selecione o sistema de referência espacial adequado através de códigos EPSG padronizados que definem projeção cartográfica, datum geodésico e zona UTM aplicáveis ao projeto. Ao alterar o SRID, o sistema executa automaticamente reprojeção de todas as coordenadas dos pontos topográficos utilizando transformações geodésicas precisas, garantindo consistência espacial entre dados coletados em diferentes sistemas de referência e assegurando integração adequada com bases cartográficas oficiais e outros dados geoespaciais. O mecanismo de validação implementado verifica a coerência das coordenadas após a transformação, identificando possíveis inconsistências resultantes de erros de parametrização ou uso de sistemas de referência incompatíveis, alertando o usuário sobre potenciais problemas antes da persistência definitiva dos dados. Esta funcionalidade é crítica em projetos cadastrais brasileiros onde frequentemente coexistem dados em diferentes sistemas de referência como SIRGAS2000 UTM, Córrego Alegre e sistemas locais arbitrários, sendo necessário harmonizar toda a base cartográfica em um sistema único para permitir análises espaciais confiáveis e geração de produtos cartográficos oficiais.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
