---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: reliability
---

# RF-051: Excluir Unidade

Usuários com role ADMIN podem excluir unidade utilizando soft delete onde registro marcado como deletado através de flag deleted_at timestamp indicando momento da exclusão sem remoção física de dados do banco garantindo preservação para auditoria e compliance, preservação de dados para auditoria mantém registro completo incluindo geometria atributos alfanuméricos titulares vinculados documentos anexados e histórico de alterações permitindo consultas históricas e recuperação se exclusão foi acidental ou prematura, remoção de visualização padrão implementada através de filtros automáticos WHERE deleted_at IS NULL em todas queries regulares excluindo unidades deletadas de listagens mapas relatórios e estatísticas mas mantendo acessibilidade em contextos administrativos específicos ou quando filtro "mostrar deletados" explicitamente ativado, implementação em módulos GEOWEB e GEOAPI com confirmação de exclusão solicitando justificativa ou motivo validação de permissão ADMIN registro em log de auditoria e opção de restauração (undelete) reverter flag deleted_at para NULL se necessário.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
