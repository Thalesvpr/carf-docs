---
modules: [GEOWEB]
epic: security
---

# RF-007: SUPER_ADMIN - Acesso Total

Usuários com role SUPER_ADMIN devem ter acesso irrestrito a todas funcionalidades e recursos do sistema transcendendo limitações de tenant onde podem criar editar excluir qualquer recurso (tenants usuários comunidades unidades documentos configurações) em qualquer tenant sem restrições de isolamento de dados, capacidade de acessar múltiplos tenants implementada através de claim especial no JWT ou flag is_super_admin permitindo que queries de banco de dados ignorem filtros automáticos de tenant_id quando usuário possui esta role, permissão para gerenciar configurações globais de sistema incluindo parâmetros de infraestrutura integrações externas políticas de segurança backups e outras configurações administrativas críticas que não são expostas para roles inferiores, implementação em módulos GEOWEB e GEOAPI com interface administrativa específica acessível apenas para SUPER_ADMIN exibindo painéis de controle gerencial listagens cross-tenant e ferramentas de troubleshooting avançadas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
