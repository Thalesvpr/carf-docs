# Tenant

Entidade representando cliente sistema (prefeitura órgão estadual empresa) em arquitetura multi-tenant isolamento completo dados via Row-Level Security PostgreSQL armazenando configurações específicas metadados organizacionais. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem Code string único curto (ITERJ HAB-RJ PMN) para URLs subdomínios, Name nome completo instituição, Document CNPJ formatado, ContactEmail comunicações oficiais, ContactPhone responsável e Address sede.

Campos personalização incluem Logo URL logotipo white-label relatórios certidões, PrimaryColor SecondaryColor hex codes tema, Settings JSONB configurações específicas campos customizados integrações limites, Subscription JSON plano contratado limites usuários/unidades/storage renovação, IsActive bool acesso global tenant e TrialEndsAt DateTime nullable período trial.

Relacionamentos incluem Account vinculados, Community do tenant, Unit cadastradas e AuditLog operações. Métodos incluem Activate()/Deactivate() bloqueando acesso todos usuários, UpdateSettings(json) validando schema, IsWithinLimits(resourceType currentCount) verificando Subscription e GetCustomFields() extraindo campos Settings. RLS filtra automaticamente queries tenant_id baseado claim JWT garantindo isolamento total dados clientes.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
