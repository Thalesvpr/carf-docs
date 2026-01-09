---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-083: Gerenciar Usuários do Tenant

Como administrador de tenant no sistema multi-inquilino, quero criar e gerenciar usuários da minha organização para que a equipe técnica tenha acesso controlado ao sistema conforme suas funções e responsabilidades, garantindo segregação de permissões e rastreabilidade de ações. A funcionalidade deve permitir cadastro completo de novos usuários fornecendo informações essenciais incluindo nome completo, endereço de email para autenticação, e atribuição inicial de role (perfil de acesso) que define permissões concedidas no sistema. O sistema deve oferecer capacidade de edição de roles de usuários existentes permitindo ajustes conforme mudanças organizacionais, funcionalidade de desativação de contas (soft delete) preservando histórico de atividades para auditoria, e listagem completa de todos os usuários vinculados ao tenant com informações de status, roles atribuídos e última atividade. Os critérios de aceitação incluem endpoint de criação de usuário aceitando nome, email e role inicial, funcionalidade de edição de role mantendo integridade referencial, desativação de usuário preservando dados históricos e impedindo novos acessos, e listagem paginada com filtros por status e role. Esta User Story está relacionada ao RF-033 e é implementada através dos endpoints POST /api/accounts, GET /api/accounts, PUT /api/accounts/{id} e DELETE /api/accounts/{id} no backend GEOAPI, com interface administrativa no frontend GEOWEB, pertencendo ao Epic 11: Administração. O status atual é implemented, com testes de unidade e integração validando controle de acesso baseado em roles e auditoria de operações administrativas.

---

**Última atualização:** 2025-12-30
