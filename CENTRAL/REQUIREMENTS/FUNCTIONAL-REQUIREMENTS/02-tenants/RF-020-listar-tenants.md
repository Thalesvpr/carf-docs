---
modules: [GEOWEB]
epic: usability
---

# RF-020: Listar Tenants

Usuários com role SUPER_ADMIN podem listar todos tenants cadastrados no sistema onde paginação de resultados implementada retornando subconjunto configurável (ex: 20 50 100 registros por página) com metadados de total de registros página atual e total de páginas permitindo navegação eficiente em grandes volumes de tenants, filtros disponíveis incluem status ativo/inativo permitindo visualizar apenas tenants operacionais ou incluir desativados filtro por nome com busca parcial case-insensitive facilitando localização rápida de tenant específico, ordenação personalizável por múltiplos critérios incluindo data de criação (padrão: mais recentes primeiro) nome alfabético última atualização ou outros campos relevantes onde direção de ordenação (ascendente descendente) configurável via interface ou parâmetros de query, implementação em módulos GEOWEB e GEOAPI com interface de listagem incluindo tabela responsiva com colunas essenciais (nome domínio status data criação quantidade usuários) controles de paginação filtros interativos e ações rápidas como editar visualizar detalhes ou desativar tenant.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
