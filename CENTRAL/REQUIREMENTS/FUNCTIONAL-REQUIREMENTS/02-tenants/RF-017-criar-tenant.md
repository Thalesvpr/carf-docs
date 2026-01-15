---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# RF-017: Criar Tenant

Usuários com role SUPER_ADMIN devem poder criar novos tenants no sistema onde formulário de criação inclui campos obrigatórios como nome do tenant (ex: "Prefeitura de São Paulo") domínio único identificador (slug ex: "pmsp") configurações iniciais de personalização (logo cores tema) e parâmetros técnicos de infraestrutura, validação de unicidade de domínio implementada garantindo que slug de tenant seja único em toda plataforma prevenindo conflitos de identificação onde tentativa de criar tenant com domínio duplicado retorna erro descritivo solicitando escolha de identificador alternativo, criação de schema ou namespace isolado no banco de dados PostgreSQL utilizando schemas separados ou particionamento lógico garantindo isolamento físico de dados entre tenants e facilitando operações de backup restore e migração específicas por tenant, implementação em módulos GEOWEB para interface administrativa e GEOAPI para processamento backend incluindo criação automática de estruturas de banco de dados configuração de recursos padrão (roles básicas categorias iniciais) e provisionamento de ambiente completo pronto para uso imediato.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
