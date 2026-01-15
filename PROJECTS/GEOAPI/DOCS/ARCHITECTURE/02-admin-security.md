# Admin Security

Endpoints /api/admin/* do GEOAPI implementam 7 camadas segurança protegendo operações administrativas sensíveis gerenciamento tenants usuários configurações sistema consumidas pelo ADMIN Console. Decisão de não usar Next.js para admin foi tomada por segurança pois API Routes Next.js com Keycloak Admin Client requerem client_secret confidencial que pode vazar bundled client-side ou expostos environment variables browser, solução segura usa SPA React Vite com PKCE flow sem client_secret conectando GEOAPI backend .NET 9 onde /api/admin/* endpoints usam Keycloak Admin Client confidential com client_secret isolado backend nunca exposto frontend.

Estrutura no GEOAPI organiza Gateway/Controllers/AdminController.cs endpoints /api/admin/*, Application/Admin/Commands CreateTenantCommand CreateUserCommand AssignRolesCommand e Queries GetTenantsQuery GetUsersQuery, Infrastructure/Keycloak KeycloakAdminService wrapper Keycloak Admin Client e KeycloakAdminConfig configuração confidencial. Fluxo requisição inicia carf-admin SPA POST /api/admin/users com Authorization Bearer JWT token, AdminController Authorize Roles super-admin admin valida token JWT Keycloak valida role valida tenant admin só vê próprio tenant, MediatR Handler CreateUserCommand FluentValidation valida DTO, KeycloakAdminService usa client_secret confidencial POST /admin/realms/carf/users Keycloak Admin API, Response retorna carf-admin com auditoria registrada AdminActionLogger.

Sete camadas segurança incluem Autenticação OAuth2 JWT tokens Keycloak validados middleware, Autorização RBAC roles super-admin admin analyst field-agent verificadas policies, Isolamento Tenant admin vê apenas próprio tenant via RLS, Validação Entrada FluentValidation sanitização DTOs, Rate Limiting proteção força bruta endpoints sensíveis, Auditoria Completa todas ações admin registradas AuditLog com IP user timestamp action, e Criptografia TLS 1.3 trânsito secrets criptografados repouso.

Endpoints admin disponíveis incluem tenants GET POST PUT DELETE /api/admin/tenants gerenciamento multi-tenancy, users GET POST PUT DELETE /api/admin/users CRUD usuários Keycloak, roles GET POST DELETE /api/admin/users/{id}/roles atribuição roles, settings GET PUT /api/admin/settings configurações sistema, e audit GET /api/admin/audit-logs consulta logs auditoria. Apenas super-admin acessa todos tenants, admin acessa apenas próprio tenant, demais roles não têm acesso endpoints admin.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
