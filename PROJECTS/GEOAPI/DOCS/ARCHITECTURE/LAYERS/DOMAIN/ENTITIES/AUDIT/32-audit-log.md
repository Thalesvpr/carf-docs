# AuditLog

Entidade representando registro auditoria rastreando operações criação atualização exclusão executadas entidades domínio armazenando quem fez o quê quando qual entidade com valores antigos novos permitindo rastreabilidade completa conformidade LGPD investigação incidentes. Herda de BaseEntity fornecendo CreatedAt timestamp operação. Campos principais incluem TenantId Guid FK Tenant isolando logs RLS, AccountId Guid nullable FK Account usuário null se job automatizado, EntityType tipo entidade afetada e EntityId Guid permitindo histórico completo registro.

Campos operação incluem Operation string CREATE/UPDATE/DELETE, TableName string tabela banco, OldValues JSON nullable valores anteriores apenas UPDATE, NewValues JSON nullable novos valores, ChangedFields JSON nullable array campos modificados facilitando busca mudanças específicas, IpAddress UserAgent identificando cliente, RequestId correlation ID debugging e Reason string nullable justificativa operação.

Métodos incluem GetChanges() retornando dicionário mudanças campo por campo diff, WasFieldChanged(fieldName) verificando campo específico alterado, GetFieldChange(fieldName) retornando tupla oldValue newValue e FormatForDisplay() gerando texto legível. Métodos estáticos LogCreate()/LogUpdate()/LogDelete() registrando operações e GetEntityHistory(entityType entityId) retornando timeline ordenada.

Regra negócio AuditLog append-only nunca deletado atualizado garantindo imutabilidade, EntityType EntityId índice busca principal, OldValues null CREATE NewValues null DELETE padrão consistente. Integra EF Core interceptor capturando mudanças SaveChanges automaticamente, suporta queries auditoria filtros período AccountId Operation, participa conformidade LGPD trilha acessos modificações dados pessoais e permite investigação incidentes reconstruindo estado anterior aplicando mudanças reversas.

---

**Última atualização:** 2026-01-12
