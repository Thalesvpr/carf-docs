import { TFile } from "obsidian";
import { Severity, SEVERITY_ORDER } from "./Severity";
import { FixAction } from "./FixAction";

/**
 * Represents a validation issue found in a document
 */
export class Issue {
  file: TFile;
  validator: string;
  severity: Severity;
  messageKey: string;
  messageParams: Record<string, unknown>;
  line: number | null;
  column: number | null;
  suggestionKey: string | null;
  suggestionParams: Record<string, unknown>;
  fixes: FixAction[];

  constructor(
    file: TFile,
    validator: string,
    severity: Severity,
    messageKey: string,
    messageParams: Record<string, unknown> = {},
    line: number | null = null,
    column: number | null = null,
    suggestionKey: string | null = null,
    suggestionParams: Record<string, unknown> = {},
    fixes: FixAction[] = []
  ) {
    this.file = file;
    this.validator = validator;
    this.severity = severity;
    this.messageKey = messageKey;
    this.messageParams = messageParams;
    this.line = line;
    this.column = column;
    this.suggestionKey = suggestionKey;
    this.suggestionParams = suggestionParams;
    this.fixes = fixes;
  }

  /**
   * Create an error issue
   */
  static error(
    file: TFile,
    validator: string,
    messageKey: string,
    messageParams?: Record<string, unknown>,
    line?: number,
    suggestionKey?: string,
    suggestionParams?: Record<string, unknown>,
    fixes?: FixAction[]
  ): Issue {
    return new Issue(
      file,
      validator,
      Severity.ERROR,
      messageKey,
      messageParams || {},
      line ?? null,
      null,
      suggestionKey ?? null,
      suggestionParams || {},
      fixes || []
    );
  }

  /**
   * Create a warning issue
   */
  static warning(
    file: TFile,
    validator: string,
    messageKey: string,
    messageParams?: Record<string, unknown>,
    line?: number,
    suggestionKey?: string,
    suggestionParams?: Record<string, unknown>,
    fixes?: FixAction[]
  ): Issue {
    return new Issue(
      file,
      validator,
      Severity.WARNING,
      messageKey,
      messageParams || {},
      line ?? null,
      null,
      suggestionKey ?? null,
      suggestionParams || {},
      fixes || []
    );
  }

  /**
   * Create an info issue
   */
  static info(
    file: TFile,
    validator: string,
    messageKey: string,
    messageParams?: Record<string, unknown>,
    line?: number,
    suggestionKey?: string,
    suggestionParams?: Record<string, unknown>,
    fixes?: FixAction[]
  ): Issue {
    return new Issue(
      file,
      validator,
      Severity.INFO,
      messageKey,
      messageParams || {},
      line ?? null,
      null,
      suggestionKey ?? null,
      suggestionParams || {},
      fixes || []
    );
  }

  /**
   * Get formatted location string
   */
  get location(): string {
    if (this.line !== null) {
      return `${this.file.name}:${this.line}`;
    }
    return this.file.name;
  }

  /**
   * Get severity icon
   */
  get icon(): string {
    switch (this.severity) {
      case Severity.ERROR:
        return "\u2717"; // ✗
      case Severity.WARNING:
        return "\u26A0"; // ⚠
      case Severity.INFO:
        return "\u2139"; // ℹ
    }
  }

  /**
   * Get severity class for styling
   */
  get severityClass(): string {
    return `docs-${this.severity}`;
  }

  /**
   * Compare issues for sorting (errors first, then warnings, then info)
   */
  static compare(a: Issue, b: Issue): number {
    const severityDiff = SEVERITY_ORDER[a.severity] - SEVERITY_ORDER[b.severity];
    if (severityDiff !== 0) return severityDiff;

    // Same severity - sort by validator name
    const validatorDiff = a.validator.localeCompare(b.validator);
    if (validatorDiff !== 0) return validatorDiff;

    // Same validator - sort by file path
    const fileDiff = a.file.path.localeCompare(b.file.path);
    if (fileDiff !== 0) return fileDiff;

    // Same file - sort by line number
    return (a.line || 0) - (b.line || 0);
  }
}

/**
 * Summary of issues by severity
 */
export interface IssueSummary {
  total: number;
  errors: number;
  warnings: number;
  info: number;
}

/**
 * Calculate issue summary from list of issues
 */
export function calculateIssueSummary(issues: Issue[]): IssueSummary {
  return {
    total: issues.length,
    errors: issues.filter(i => i.severity === Severity.ERROR).length,
    warnings: issues.filter(i => i.severity === Severity.WARNING).length,
    info: issues.filter(i => i.severity === Severity.INFO).length
  };
}
