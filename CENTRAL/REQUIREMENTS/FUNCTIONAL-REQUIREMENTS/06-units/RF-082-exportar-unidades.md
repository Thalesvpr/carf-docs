---
modules: [GEOWEB, REURBCAD, GEOGIS]
epic: reliability
---

# RF-082: Exportar Unidades

O sistema deve permitir exportação de unidades selecionadas ou filtradas em múltiplos formatos (SHAPEFILE KML GEOJSON CSV EXCEL) atendendo diferentes casos de uso incluindo integração com GIS externo, compartilhamento de dados territoriais e análises em ferramentas de planilha. A exportação respeita filtros ativos aplicados na interface de listagem garantindo que apenas unidades visíveis conforme critérios de seleção sejam incluídas no arquivo exportado, evitando exportações acidentais de todo dataset quando intenção é extrair subconjunto específico. Interface oferece opção de incluir fotos e documentos anexados às unidades no pacote de exportação, onde seleção desta opção gera arquivo compactado (ZIP) contendo dados tabulares ou geográficos principais mais pasta de anexos organizados por código de unidade facilitando correlação entre registros e mídias associadas. Implementado nos módulos GEOWEB e GEOAPI com prioridade Should-have, este recurso suporta workflows de intercâmbio de dados com stakeholders externos, backup descentralizado de informações cadastrais, preparação de bases para análises offline e integração com sistemas legados que não possuem conectividade direta com APIs, garantindo que dados capturados no sistema possam circular livremente conforme necessidades institucionais de compartilhamento e interoperabilidade.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
