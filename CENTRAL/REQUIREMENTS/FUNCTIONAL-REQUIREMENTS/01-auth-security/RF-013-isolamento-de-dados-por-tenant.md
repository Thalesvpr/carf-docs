---
modules: [GEOAPI]
epic: security
---

# RF-013: Isolamento de Dados por Tenant

Usuários só podem acessar dados pertencentes ao seu tenant implementado através de Row Level Security (RLS) onde queries de banco de dados filtram automaticamente resultados por tenant_id extraído de claim presente no JWT do usuário autenticado garantindo isolamento lógico completo entre tenants compartilhando mesma infraestrutura de banco de dados, impossibilidade de acessar dados de outro tenant via API garantida através de validação obrigatória de tenant_id em todas operações de leitura escrita atualização e exclusão onde tentativas de manipular parâmetros de requisição para acessar tenant_id diferente são bloqueadas com retorno HTTP 403 Forbidden, exceção implementada para SUPER_ADMIN que pode trocar contexto de tenant através de claim especial ou header HTTP customizado permitindo administração cross-tenant para fins de suporte técnico troubleshooting e gestão global de plataforma, implementação em módulo GEOAPI utilizando interceptors ou filtros globais que injetam automaticamente cláusula WHERE tenant_id = :current_tenant_id em todas queries ORM garantindo consistência e prevenindo vazamento acidental de dados entre tenants.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
