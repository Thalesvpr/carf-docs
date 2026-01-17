---
modules: [GEOWEB]
epic: communities
---

# RF-036: Desativar Comunidade

Usuários com role ADMIN podem desativar comunidade utilizando soft delete onde comunidade marcada como inativa através de flag is_active=false sem exclusão física de dados, unidades vinculadas à comunidade desativada são preservadas integralmente mantendo referência para comunidade através de foreign key permitindo consultas históricas e relatórios completos de dados mesmo após desativação, comunidade inativa não aparece em listagens padrão de interface de usuário sendo filtrada automaticamente através de cláusula WHERE is_active = true em queries regulares mas permanece visível em contextos administrativos específicos ou quando filtro "mostrar inativos" explicitamente ativado, implementação em módulos GEOWEB e GEOAPI com confirmação de desativação solicitando razão/motivo registrando em log de auditoria validando se usuário possui permissão adequada e exibindo aviso sobre impacto em visualizações e relatórios após confirmação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
