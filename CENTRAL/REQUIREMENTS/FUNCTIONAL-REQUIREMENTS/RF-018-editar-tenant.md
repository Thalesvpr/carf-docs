---
modules: [GEOWEB]
epic: audit
---

# RF-018: Editar Tenant

Usuários com role SUPER_ADMIN e ADMIN do próprio tenant podem editar configurações do tenant onde atualização inclui modificação de nome oficial logo institucional cores de tema personalização de interface e parâmetros operacionais específicos como limites de usuários quotas de storage configurações de email e integrações externas, validação de dados obrigatórios garante integridade de informações onde campos críticos como nome e domínio não podem ser deixados vazios e modificações em identificador único (slug) são bloqueadas ou requerem confirmação adicional devido a impacto potencial em URLs e referências existentes, log de alterações registra histórico completo de modificações incluindo timestamp usuário responsável campos alterados valores anteriores e novos valores permitindo auditoria completa de mudanças em configurações críticas de tenant e possibilitando rollback se necessário, implementação em módulos GEOWEB e GEOAPI com interface de edição intuitiva exibindo formulário pré-preenchido com valores atuais validações em tempo real e confirmação visual após salvamento bem-sucedido.

---

**Última atualização:** 2025-12-30
