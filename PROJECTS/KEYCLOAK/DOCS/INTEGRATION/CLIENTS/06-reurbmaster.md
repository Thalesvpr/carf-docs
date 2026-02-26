---
type: leaf
status: review
updated: 2026-01-19
---

# Client REURBMASTER

Console administrativo Next.js para gestão de tenants e usuários configurado como public client com PKCE S256 e acesso à Keycloak Admin API.

Redirect URIs incluem http://localhost:3000/* para desenvolvimento e https://admin.carf.example.com/* para produção. Client roles específicos definidos: manage-users para CRUD de usuários via Admin API, manage-tenants para CRUD de tenants, e view-audit-logs para acesso read-only a logs de auditoria.

Integração com Admin API: como admin é public client (sem service account), operações na Keycloak Admin API devem ser proxeadas via GEOAPI que atua como backend confidential, ou usando token do usuário admin/super-admin logado diretamente via @keycloak/keycloak-admin-client no frontend (limitado às permissões do usuário). Operações incluem criar usuários, atribuir roles, atualizar atributos de tenant.

Apenas usuários com role super-admin ou client role manage-tenants podem acessar o console. UI específica REURB usa terminologia "Prefeituras" ao invés de "Tenants", formulários incluem validação de CNPJ, dashboard mostra métricas como unidades cadastradas por prefeitura e processos em andamento.
