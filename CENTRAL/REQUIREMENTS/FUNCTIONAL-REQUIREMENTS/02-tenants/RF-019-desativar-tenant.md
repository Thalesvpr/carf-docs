---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: security
---

# RF-019: Desativar Tenant

Usuários com role SUPER_ADMIN podem desativar tenant utilizando soft delete onde tenant é marcado como inativo através de flag booleano is_active=false em tabela de tenants sem exclusão física de dados, usuários vinculados ao tenant desativado não conseguem mais realizar login onde tentativa de autenticação retorna mensagem específica "Tenant inativo. Contate o administrador do sistema." bloqueando acesso completo a recursos e funcionalidades, dados do tenant preservados integralmente para fins de auditoria compliance e possível reativação futura onde informações históricas permanecem disponíveis para consultas administrativas por SUPER_ADMIN mas são completamente invisíveis e inacessíveis para usuários regulares, implementação em módulos GEOWEB e GEOAPI incluindo filtro global que exclui automaticamente tenants inativos de listagens e queries regulares adicionando cláusula WHERE is_active = true exceto em contextos administrativos específicos onde visualização de tenants desativados é necessária para gestão e troubleshooting.

---

**Última atualização:** 2025-12-30
