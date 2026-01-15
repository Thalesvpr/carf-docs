---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: units
---

# RF-075: Vincular Unidade a Lote

O sistema deve permitir vinculação de unidades habitacionais a lotes específicos através de foreign key (plot_id) no modelo de unidade, onde relacionamento estabelece hierarquia territorial quadra-lote-unidade útil em contextos de parcelamento formal do solo. A vinculação deve incluir validação de pertencimento garantindo que unidade só pode ser associada a lote da mesma quadra à qual a unidade pertence, evitando inconsistências hierárquicas onde unidade de uma quadra fosse vinculada a lote de outra quadra criando estrutura territorial inválida. O sistema oferece filtros por lote nas interfaces de listagem e consulta de unidades, permitindo visualização segmentada de todas as unidades pertencentes a determinado lote facilitando análises e operações em escopo de parcela específica. Implementado no módulo GEOAPI com prioridade Could-have, este recurso é opcional mas valioso em projetos de regularização fundiária com parcelamento planejado, onde gestores precisam organizar cadastro segundo subdivisões formais do território, garantindo rastreabilidade entre parcelas registradas ou a registrar e unidades edificadas ou a edificar sobre cada lote individualizado.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
