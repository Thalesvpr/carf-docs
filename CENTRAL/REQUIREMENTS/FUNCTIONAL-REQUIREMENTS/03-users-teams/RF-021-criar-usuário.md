---
modules: [GEOAPI, GEOWEB]
epic: teams
---

# RF-021: Criar Usuário

Usuários com roles ADMIN e SUPER_ADMIN podem criar novos usuários no tenant onde formulário de criação inclui campos obrigatórios nome completo email único role inicial (MANAGER ANALYST FIELD_AGENT) e opcionalmente telefone departamento equipe vinculada e foto de perfil, validação de email único implementada verificando inexistência de email em base de usuários do tenant retornando erro descritivo "Email já cadastrado" caso duplicidade detectada impedindo criação de múltiplas contas com mesmo endereço eletrônico, envio automático de email de boas-vindas após criação bem-sucedida contendo link para ativação de conta definição de senha inicial instruções de primeiro acesso e informações de contato de suporte técnico, implementação em módulos GEOWEB para interface de cadastro e GEOAPI para processamento backend incluindo criação de registro em Keycloak sincronização de dados entre sistema local e Identity Provider atribuição automática de tenant_id baseado em contexto do administrador criador e geração de credenciais temporárias seguras.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
