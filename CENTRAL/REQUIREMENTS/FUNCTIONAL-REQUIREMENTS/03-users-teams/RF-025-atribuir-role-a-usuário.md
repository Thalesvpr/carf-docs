---
modules: [GEOWEB]
epic: audit
---

# RF-025: Atribuir Role a Usuário

Usuários com role ADMIN podem atribuir ou alterar role de usuários do tenant onde seleção de role ocorre via dropdown exibindo opções permitidas (MANAGER ANALYST FIELD_AGENT) excluindo SUPER_ADMIN que só pode ser atribuída por outro SUPER_ADMIN, validação de permissões garante que ADMIN não pode elevar privilégios além de seu próprio nível impedindo escalação de privilégios e que mudanças de role sejam registradas em log de auditoria para rastreabilidade, atualização imediata de permissões onde após salvamento role é sincronizada com Keycloak e próxima requisição do usuário já reflete novas permissões sem necessidade de logout/login através de renovação de token com claims atualizados, implementação em módulos GEOWEB e GEOAPI com interface de edição rápida permitindo mudança de role diretamente na listagem de usuários ou via modal de edição completa incluindo validação em tempo real e feedback visual de sucesso.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
