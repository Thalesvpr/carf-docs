import { App } from "obsidian";
import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { DocsLinterConfig, DocumentTypeConfig, TemplateValidation } from "../../config/ConfigSchema";

/**
 * Context passed to validators during validation
 */
export interface ValidatorContext {
  /** Obsidian App instance */
  app: App;

  /** Full configuration */
  config: DocsLinterConfig;

  /** Document type configuration (if document has a detected type) */
  documentTypeConfig: DocumentTypeConfig | null;

  /** Template validation rules (if document has a template) */
  templateValidation: TemplateValidation | null;

  /** Translation function */
  t: (key: string, params?: Record<string, unknown>) => string;

  /** All documents in the vault (for global validators) */
  allDocuments?: Document[];
}

/**
 * Base interface for all validators
 */
export interface Validator {
  /** Unique identifier for this validator */
  readonly id: string;

  /** i18n key for the validator name */
  readonly nameKey: string;

  /** i18n key for the validator description */
  readonly descriptionKey: string;

  /** Whether this validator needs all documents (global) or just one (local) */
  readonly isGlobal: boolean;

  /** Default severity for issues from this validator */
  readonly defaultSeverity: Severity;

  /**
   * Validate a single document (for local validators)
   * @param doc The document to validate
   * @param ctx Validation context
   * @returns Array of issues found
   */
  validate?(doc: Document, ctx: ValidatorContext): Promise<Issue[]>;

  /**
   * Validate all documents (for global validators)
   * @param docs All documents
   * @param ctx Validation context
   * @returns Array of issues found
   */
  validateAll?(docs: Document[], ctx: ValidatorContext): Promise<Issue[]>;
}

/**
 * Abstract base class for local validators (single document)
 */
export abstract class LocalValidator implements Validator {
  abstract readonly id: string;
  abstract readonly nameKey: string;
  abstract readonly descriptionKey: string;
  readonly isGlobal = false;
  abstract readonly defaultSeverity: Severity;

  abstract validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]>;
}

/**
 * Abstract base class for global validators (all documents)
 */
export abstract class GlobalValidator implements Validator {
  abstract readonly id: string;
  abstract readonly nameKey: string;
  abstract readonly descriptionKey: string;
  readonly isGlobal = true;
  abstract readonly defaultSeverity: Severity;

  abstract validateAll(docs: Document[], ctx: ValidatorContext): Promise<Issue[]>;
}

/**
 * Helper to get configured severity or default
 */
export function getConfiguredSeverity(
  validatorId: string,
  config: DocsLinterConfig,
  defaultSeverity: Severity
): Severity {
  const validatorConfig = config.validators[validatorId];
  if (validatorConfig?.severity) {
    return validatorConfig.severity;
  }
  return defaultSeverity;
}

/**
 * Helper to check if validator is enabled
 */
export function isValidatorEnabled(
  validatorId: string,
  config: DocsLinterConfig
): boolean {
  const validatorConfig = config.validators[validatorId];
  return validatorConfig?.enabled !== false;
}
