/**
 * Issue severity levels
 */
export enum Severity {
  ERROR = "error",
  WARNING = "warning",
  INFO = "info"
}

/**
 * Severity order for sorting (lower = more severe)
 */
export const SEVERITY_ORDER: Record<Severity, number> = {
  [Severity.ERROR]: 0,
  [Severity.WARNING]: 1,
  [Severity.INFO]: 2
};
