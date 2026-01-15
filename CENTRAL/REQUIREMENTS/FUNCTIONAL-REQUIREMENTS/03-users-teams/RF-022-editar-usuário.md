---
modules: [GEOWEB]
epic: security
---

# RF-022: Editar Usuário

Usuários com role ADMIN podem editar dados de usuários pertencentes ao mesmo tenant onde atualização inclui modificação de nome completo email role atribuída status ativo/inativo vinculação a equipes e outras informações de perfil preservando histórico de alterações para auditoria, validação de permissões garante que ADMIN só edite usuários do próprio tenant impedindo modificação cross-tenant e que alterações de role respeitem hierarquia onde ADMIN não pode criar ou promover usuários para role SUPER_ADMIN, log detalhado de alterações registra timestamp usuário responsável pela modificação campos alterados valores anteriores e novos valores permitindo rastreabilidade completa de mudanças em dados sensíveis de usuários e facilitando troubleshooting de problemas de acesso ou permissões, implementação em módulos GEOWEB e GEOAPI com formulário de edição pré-preenchido validações em tempo real sincronização com Keycloak para alterações que afetam autenticação (email role) e confirmação visual de salvamento bem-sucedido.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
