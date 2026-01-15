---
modules: [GEOWEB]
epic: holders
---

# RF-086: Excluir Titular

O sistema deve permitir que administradores (perfil ADMIN) excluam titulares da base de dados utilizando estratégia de soft delete que marca registro como inativo sem remoção física do banco, preservando integridade referencial e histórico de auditoria. Antes de permitir exclusão, sistema verifica existência de vínculos ativos com unidades habitacionais alertando administrador quando titular possui relacionamentos ativos que precisam ser removidos ou transferidos antes que exclusão possa prosseguir, prevenindo órfãos referenciais e inconsistências de dados. A interface apresenta modal de confirmação obrigatória exigindo que administrador confirme explicitamente intenção de excluir titular, incluindo aviso sobre consequências da ação e contagem de vínculos que serão afetados, garantindo que exclusões não ocorram acidentalmente por cliques involuntários. Implementado nos módulos GEOWEB e GEOAPI com prioridade Must-have, este recurso permite limpeza de cadastros duplicados ou errôneos mantendo rastreabilidade através de soft delete que possibilita eventual restauração de registros excluídos inadvertidamente, além de preservar histórico completo para auditorias futuras que possam requerer investigação de titulares previamente cadastrados e posteriormente removidos.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
