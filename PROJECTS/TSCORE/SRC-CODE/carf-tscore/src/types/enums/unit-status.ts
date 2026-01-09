/**
 * UnitStatus - Unit Workflow Status Enum
 *
 * Workflow states for housing unit cadastre and approval process.
 *
 * @see CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/03-unit-status.md
 */

export enum UnitStatus {
  /**
   * Draft - Initial state, being created
   */
  DRAFT = 'DRAFT',

  /**
   * Pending - Submitted for review
   */
  PENDING = 'PENDING',

  /**
   * In Review - Being reviewed by manager/analyst
   */
  IN_REVIEW = 'IN_REVIEW',

  /**
   * Approved - Unit approved, ready for legitimation
   */
  APPROVED = 'APPROVED',

  /**
   * Rejected - Unit rejected, cannot proceed
   */
  REJECTED = 'REJECTED',

  /**
   * Requires Changes - Unit needs corrections before approval
   */
  REQUIRES_CHANGES = 'REQUIRES_CHANGES'
}

/**
 * Valid status transitions
 */
export const UnitStatusTransitions: Record<UnitStatus, UnitStatus[]> = {
  [UnitStatus.DRAFT]: [UnitStatus.PENDING],
  [UnitStatus.PENDING]: [UnitStatus.IN_REVIEW, UnitStatus.DRAFT],
  [UnitStatus.IN_REVIEW]: [UnitStatus.APPROVED, UnitStatus.REJECTED, UnitStatus.REQUIRES_CHANGES],
  [UnitStatus.APPROVED]: [], // Final state
  [UnitStatus.REJECTED]: [], // Final state
  [UnitStatus.REQUIRES_CHANGES]: [UnitStatus.PENDING]
}

/**
 * Checks if a status transition is valid
 * @param from - Current status
 * @param to - Target status
 * @returns true if transition is allowed
 */
export function isValidStatusTransition(from: UnitStatus, to: UnitStatus): boolean {
  return UnitStatusTransitions[from].includes(to)
}

/**
 * Checks if a status is final (no further transitions)
 * @param status - Status to check
 * @returns true if status is final
 */
export function isFinalStatus(status: UnitStatus): boolean {
  return UnitStatusTransitions[status].length === 0
}
