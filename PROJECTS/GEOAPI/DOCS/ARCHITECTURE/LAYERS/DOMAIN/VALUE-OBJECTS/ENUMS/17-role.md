---
type: leaf
status: review
updated: 2026-01-12
---

# Role

Value object enum representando papel de usuário no sistema definindo conjunto de permissões e acesso a funcionalidades conforme hierarquia organizacional. Valores possíveis são SUPER_ADMIN (administrador do sistema com acesso total a todos os tenants), ADMIN (administrador do tenant com acesso completo dentro de seu cliente), MANAGER (gerente coordenando múltiplas equipes com permissão de aprovar/rejeitar unidades e visualizar dashboards), ANALYST (analista técnico responsável por analisar solicitações de legitimação e emitir pareceres), FIELD_COORDINATOR (coordenador de campo que supervisiona equipe de cadastradores com menu mobile completo e visualização de dados da equipe), e FIELD_CADASTRATOR (cadastrador de campo que tem acesso restrito apenas a mapa e formulários sem menu completo).

Métodos incluem GetPermissions() retornando lista de permissões do papel, CanAccessTenant(tenantId) verificando acesso multi-tenant (apenas SUPER_ADMIN pode trocar), CanApproveUnits() retornando true para MANAGER/ANALYST, CanManageUsers() retornando true para SUPER_ADMIN/ADMIN, IsFieldRole() verificando se é papel de campo (FIELD_COORDINATOR ou FIELD_CADASTRATOR), e CompareTo(Role other) implementando hierarquia para validações.

Usado em Account.Role definindo permissões do usuário, validado em authorization policies via IPermissionChecker, integra com Keycloak onde roles são sincronizadas via claims JWT, e determina UI exibida (FIELD_CADASTRATOR vê apenas mapa e formulários sem menu, FIELD_COORDINATOR vê menu mobile completo com dados da equipe, ANALYST vê backoffice análise, ADMIN vê configurações).
