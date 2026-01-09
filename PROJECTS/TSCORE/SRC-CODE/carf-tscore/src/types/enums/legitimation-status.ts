/**
 * LegitimationStatus - Legitimation Request Workflow Status
 *
 * 11-state workflow for REURB legitimation process according to Lei 13.465/2017.
 *
 * @see CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/22-legitimation-status.md
 * @see CENTRAL/BUSINESS-RULES/WORKFLOW-RULES/legitimation-status-transitions.md
 */

export enum LegitimationStatus {
  /**
   * Draft - Request being prepared
   */
  DRAFT = 'DRAFT',

  /**
   * Submitted - Request submitted for analysis
   */
  SUBMITTED = 'SUBMITTED',

  /**
   * Under Analysis - Technical analysis in progress
   */
  UNDER_ANALYSIS = 'UNDER_ANALYSIS',

  /**
   * Pending Documentation - Waiting for additional documents
   */
  PENDING_DOCUMENTATION = 'PENDING_DOCUMENTATION',

  /**
   * In Public Notice - Public notification period (edital)
   */
  IN_PUBLIC_NOTICE = 'IN_PUBLIC_NOTICE',

  /**
   * Under Contestation - Contestation received, under review
   */
  UNDER_CONTESTATION = 'UNDER_CONTESTATION',

  /**
   * Approved - Request approved, certificate being prepared
   */
  APPROVED = 'APPROVED',

  /**
   * Certificate Issued - Legitimation certificate issued
   */
  CERTIFICATE_ISSUED = 'CERTIFICATE_ISSUED',

  /**
   * Rejected - Request rejected
   */
  REJECTED = 'REJECTED',

  /**
   * Cancelled - Request cancelled by requester
   */
  CANCELLED = 'CANCELLED',

  /**
   * Expired - Request expired due to deadline
   */
  EXPIRED = 'EXPIRED'
}

/**
 * Valid status transitions
 */
export const LegitimationStatusTransitions: Record<LegitimationStatus, LegitimationStatus[]> = {
  [LegitimationStatus.DRAFT]: [LegitimationStatus.SUBMITTED, LegitimationStatus.CANCELLED],
  [LegitimationStatus.SUBMITTED]: [LegitimationStatus.UNDER_ANALYSIS, LegitimationStatus.REJECTED],
  [LegitimationStatus.UNDER_ANALYSIS]: [
    LegitimationStatus.PENDING_DOCUMENTATION,
    LegitimationStatus.IN_PUBLIC_NOTICE,
    LegitimationStatus.REJECTED
  ],
  [LegitimationStatus.PENDING_DOCUMENTATION]: [
    LegitimationStatus.UNDER_ANALYSIS,
    LegitimationStatus.EXPIRED,
    LegitimationStatus.CANCELLED
  ],
  [LegitimationStatus.IN_PUBLIC_NOTICE]: [
    LegitimationStatus.UNDER_CONTESTATION,
    LegitimationStatus.APPROVED
  ],
  [LegitimationStatus.UNDER_CONTESTATION]: [
    LegitimationStatus.APPROVED,
    LegitimationStatus.REJECTED
  ],
  [LegitimationStatus.APPROVED]: [LegitimationStatus.CERTIFICATE_ISSUED],
  [LegitimationStatus.CERTIFICATE_ISSUED]: [], // Final state
  [LegitimationStatus.REJECTED]: [], // Final state
  [LegitimationStatus.CANCELLED]: [], // Final state
  [LegitimationStatus.EXPIRED]: [] // Final state
}

/**
 * Checks if a status transition is valid
 * @param from - Current status
 * @param to - Target status
 * @returns true if transition is allowed
 */
export function isValidLegitimationTransition(from: LegitimationStatus, to: LegitimationStatus): boolean {
  return LegitimationStatusTransitions[from].includes(to)
}

/**
 * Checks if a status is final (no further transitions)
 * @param status - Status to check
 * @returns true if status is final
 */
export function isFinalLegitimationStatus(status: LegitimationStatus): boolean {
  return LegitimationStatusTransitions[status].length === 0
}
