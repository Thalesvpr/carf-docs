import { TFile } from "obsidian";
import { Severity } from "./types";

/**
 * Represents a validation issue found in a document
 */
export class Issue {
  file: TFile;
  validator: string;
  severity: Severity;
  message: string;
  line: number | null;
  column: number | null;
  suggestion: string | null;

  constructor(
    file: TFile,
    validator: string,
    severity: Severity,
    message: string,
    line: number | null = null,
    column: number | null = null,
    suggestion: string | null = null
  ) {
    this.file = file;
    this.validator = validator;
    this.severity = severity;
    this.message = message;
    this.line = line;
    this.column = column;
    this.suggestion = suggestion;
  }

  /**
   * Create an error issue
   */
  static error(
    file: TFile,
    validator: string,
    message: string,
    line?: number,
    suggestion?: string
  ): Issue {
    return new Issue(file, validator, Severity.ERROR, message, line, null, suggestion);
  }

  /**
   * Create a warning issue
   */
  static warning(
    file: TFile,
    validator: string,
    message: string,
    line?: number,
    suggestion?: string
  ): Issue {
    return new Issue(file, validator, Severity.WARNING, message, line, null, suggestion);
  }

  /**
   * Create an info issue
   */
  static info(
    file: TFile,
    validator: string,
    message: string,
    line?: number,
    suggestion?: string
  ): Issue {
    return new Issue(file, validator, Severity.INFO, message, line, null, suggestion);
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
        return "✗";
      case Severity.WARNING:
        return "⚠";
      case Severity.INFO:
        return "ℹ";
    }
  }

  /**
   * Get severity class for styling
   */
  get severityClass(): string {
    return `carf-${this.severity}`;
  }

  /**
   * Compare issues for sorting (errors first, then warnings, then info)
   */
  static compare(a: Issue, b: Issue): number {
    const severityOrder = {
      [Severity.ERROR]: 0,
      [Severity.WARNING]: 1,
      [Severity.INFO]: 2
    };

    const severityDiff = severityOrder[a.severity] - severityOrder[b.severity];
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
