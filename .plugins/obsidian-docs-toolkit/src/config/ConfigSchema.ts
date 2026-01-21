import { Severity } from "../core/Severity";

/**
 * Main configuration schema for .docslint.yaml
 */
export interface DocsLinterConfig {
  /** Extends a preset or another config file */
  extends?: string | string[];

  /** Language for messages (e.g., "en", "pt-BR", "es") */
  language: string;

  /** Path configuration */
  paths: PathsConfig;

  /** Document type definitions */
  documentTypes: Record<string, DocumentTypeConfig>;

  /** Validator configuration */
  validators: Record<string, ValidatorConfig>;

  /** Workflow configuration */
  workflow: WorkflowConfig;
}

/**
 * Path include/exclude configuration
 */
export interface PathsConfig {
  /** Glob patterns to include */
  include: string[];
  /** Glob patterns to exclude */
  exclude: string[];
}

/**
 * Document type configuration
 */
export interface DocumentTypeConfig {
  /** Human-readable name for this type */
  name: string;

  /** How to detect this document type */
  detection: DetectionConfig;

  /** Frontmatter validation rules */
  frontmatter?: FrontmatterConfig;

  /** Title validation rules */
  title?: TitleConfig;

  /** Required sections */
  sections?: SectionsConfig;

  /** Template file that provides validation rules */
  template?: string;
}

/**
 * Document type detection configuration
 */
export interface DetectionConfig {
  /** Regex pattern for filename */
  filename?: string;
  /** Glob pattern for path */
  path?: string;
  /** Frontmatter field to check (e.g., "type: adr") */
  frontmatterField?: {
    field: string;
    value: string;
  };
}

/**
 * Frontmatter validation configuration
 */
export interface FrontmatterConfig {
  /** Required fields */
  required?: string[];
  /** Field-specific validation */
  fields?: Record<string, FieldConfig>;
}

/**
 * Field validation configuration
 */
export interface FieldConfig {
  /** Regex pattern to match */
  pattern?: string;
  /** Allowed values */
  enum?: string[];
  /** Expected type */
  type?: "string" | "number" | "boolean" | "array" | "object";
  /** For array types, validation of items */
  items?: {
    enum?: string[];
    pattern?: string;
  };
  /** Minimum value (for numbers) or length (for strings/arrays) */
  min?: number;
  /** Maximum value (for numbers) or length (for strings/arrays) */
  max?: number;
}

/**
 * Title validation configuration
 */
export interface TitleConfig {
  /** Regex pattern the title must match */
  pattern?: string;
  /** Whether title is required */
  required?: boolean;
}

/**
 * Section validation configuration
 */
export interface SectionsConfig {
  /** Required section names */
  required?: string[];
  /** Forbidden section names */
  forbidden?: string[];
}

/**
 * Individual validator configuration
 */
export interface ValidatorConfig {
  /** Whether validator is enabled */
  enabled: boolean;
  /** Severity override */
  severity?: Severity;
  /** Additional validator-specific options */
  [key: string]: unknown;
}

/**
 * Workflow configuration
 */
export interface WorkflowConfig {
  /** Available statuses */
  statuses: Record<string, StatusConfig>;
}

/**
 * Status configuration
 */
export interface StatusConfig {
  /** Display name */
  name: string;
  /** Icon name (lucide icon) */
  icon: string;
  /** Color (hex) */
  color: string;
}

/**
 * Template validation configuration (from template frontmatter)
 */
export interface TemplateValidation {
  /** Maximum words in document */
  max_words?: number;
  /** Maximum words per section */
  max_words_per_section?: number;
  /** Required sections */
  required_sections?: string[];
  /** Forbidden patterns (regex) */
  forbidden?: string[];
  /** Minimum word count */
  min_words?: number;
}

/**
 * Template frontmatter structure
 */
export interface TemplateFrontmatter {
  type: "template";
  template_for: string;
  validation?: TemplateValidation;
}

/**
 * Default configuration
 */
export const DEFAULT_CONFIG: DocsLinterConfig = {
  language: "en",
  paths: {
    include: ["**/*.md"],
    exclude: [".obsidian/**", ".git/**", "node_modules/**", ".plugins/**"]
  },
  documentTypes: {},
  validators: {
    frontmatter: { enabled: true, severity: Severity.ERROR },
    sections: { enabled: true, severity: Severity.WARNING },
    naming: { enabled: true, severity: Severity.ERROR },
    title: { enabled: true, severity: Severity.WARNING },
    "broken-links": { enabled: true, severity: Severity.ERROR },
    orphans: { enabled: true, severity: Severity.WARNING },
    stale: { enabled: true, severity: Severity.INFO, thresholdDays: 180 },
    "forbidden-patterns": { enabled: true, severity: Severity.WARNING },
    "word-count": { enabled: true, severity: Severity.INFO },
    "empty-folders": { enabled: true, severity: Severity.INFO }
  },
  workflow: {
    statuses: {
      review: { name: "In Review", icon: "refresh-cw", color: "#f0ad4e" },
      approved: { name: "Approved", icon: "check", color: "#5cb85c" },
      rejected: { name: "Rejected", icon: "x", color: "#d9534f" }
    }
  }
};

/**
 * Check if frontmatter represents a template
 */
export function isTemplateFrontmatter(fm: unknown): fm is TemplateFrontmatter {
  if (!fm || typeof fm !== "object") return false;
  const obj = fm as Record<string, unknown>;
  return obj.type === "template" && typeof obj.template_for === "string";
}
