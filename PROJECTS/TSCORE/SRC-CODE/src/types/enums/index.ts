/**
 * Enums Module
 *
 * Domain enumerations for CARF system.
 */

export {
  Role,
  RoleHierarchy,
  hasRolePermission,
  getRolesWithMinimumLevel
} from './role.js'

export {
  UnitStatus,
  UnitStatusTransitions,
  isValidStatusTransition,
  isFinalStatus
} from './unit-status.js'

export {
  LegitimationStatus,
  LegitimationStatusTransitions,
  isValidLegitimationTransition,
  isFinalLegitimationStatus
} from './legitimation-status.js'
