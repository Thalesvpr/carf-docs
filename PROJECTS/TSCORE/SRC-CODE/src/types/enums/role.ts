/**
 * Role - User Role Enum
 *
 * 5-level access control hierarchy for CARF system.
 *
 * @see CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/24-role.md
 * @see CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-006-5-niveis-de-acesso-roles.md
 */

export enum Role {
  /**
   * Super Administrator - Full system access across all tenants
   */
  SUPER_ADMIN = 'SUPER_ADMIN',

  /**
   * Administrator - Full access within tenant (manage users, teams, etc.)
   */
  ADMIN = 'ADMIN',

  /**
   * Manager - Approve workflows and manage assignments
   */
  MANAGER = 'MANAGER',

  /**
   * Analyst - Create and edit data (units, holders, documents)
   */
  ANALYST = 'ANALYST',

  /**
   * Field Agent - Collect data in field (mobile only)
   */
  FIELD_AGENT = 'FIELD_AGENT'
}

/**
 * Role hierarchy levels (higher = more permissions)
 */
export const RoleHierarchy: Record<Role, number> = {
  [Role.SUPER_ADMIN]: 5,
  [Role.ADMIN]: 4,
  [Role.MANAGER]: 3,
  [Role.ANALYST]: 2,
  [Role.FIELD_AGENT]: 1
}

/**
 * Checks if a role has at least the required permission level
 * @param userRole - User's current role
 * @param requiredRole - Required minimum role
 * @returns true if user has sufficient permissions
 */
export function hasRolePermission(userRole: Role, requiredRole: Role): boolean {
  return RoleHierarchy[userRole] >= RoleHierarchy[requiredRole]
}

/**
 * Gets all roles with level equal or higher than given role
 * @param role - Minimum role level
 * @returns Array of roles with sufficient permissions
 */
export function getRolesWithMinimumLevel(role: Role): Role[] {
  const minLevel = RoleHierarchy[role]
  return Object.entries(RoleHierarchy)
    .filter(([, level]) => level >= minLevel)
    .map(([r]) => r as Role)
}
