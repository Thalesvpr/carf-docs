---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: reliability
---

# RF-129: Excluir Camada

Este requisito estabelece que administradores devem poder excluir camadas GIS através de processo controlado que garante integridade de dados e previne remoções acidentais, onde exclusão é implementada via soft delete marcando camada como excluída sem remoção física imediata. Antes de permitir exclusão, o sistema deve verificar se existem features vinculadas à camada, onde se features existem interface apresenta aviso claro informando quantidade de features que serão afetadas e solicitando confirmação explícita da exclusão, permitindo que administrador compreenda impacto completo da operação. O sistema deve implementar soft delete através de campo deleted_at ou similar que marca camada como excluída preservando dados para auditoria e possível recuperação, onde camadas soft-deleted não aparecem em listagens normais mas podem ser acessadas através de interfaces administrativas de recuperação. A exclusão deve exigir confirmação adicional através de diálogo ou modal que previne remoções acidentais, particularmente importante quando camada contém features que também serão marcadas como excluídas em cascata. O sistema deve registrar operação no log de auditoria incluindo identificação do administrador timestamp e contexto. A funcionalidade deve estar disponível nos módulos GEOWEB através de interface administrativa e GEOAPI via endpoint DELETE com validações rigorosas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
