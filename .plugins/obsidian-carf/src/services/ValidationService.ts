import { App, TFile, TFolder } from "obsidian";
import { Document } from "../models/Document";
import { Issue, IssueSummary, calculateIssueSummary } from "../models/Issue";
import { Validator } from "../validators/Validator";
import { MetadataService } from "./MetadataService";

// Import all validators
import { BrokenLinksValidator } from "../validators/BrokenLinksValidator";
import { FrontmatterValidator } from "../validators/FrontmatterValidator";
import { OrphansValidator } from "../validators/OrphansValidator";
import { StructureValidator } from "../validators/StructureValidator";
import { TitleValidator } from "../validators/TitleValidator";
import { StaleValidator } from "../validators/StaleValidator";
import { EmptyFoldersValidator } from "../validators/EmptyFoldersValidator";
import { NamingValidator } from "../validators/NamingValidator";

/**
 * Result of a validation run
 */
export interface ValidationResult {
  issues: Issue[];
  summary: IssueSummary;
  documents: Document[];
  timestamp: Date;
}

/**
 * Service that orchestrates all validators
 */
export class ValidationService {
  private app: App;
  private metadataService: MetadataService;
  private validators: Map<string, Validator>;
  private enabledValidators: Set<string>;
  private lastResult: ValidationResult | null = null;

  constructor(app: App, metadataService: MetadataService) {
    this.app = app;
    this.metadataService = metadataService;
    this.validators = new Map();
    this.enabledValidators = new Set();

    // Register all validators
    this.registerValidators();
  }

  /**
   * Register all available validators
   */
  private registerValidators(): void {
    const validators: Validator[] = [
      new BrokenLinksValidator(),
      new FrontmatterValidator(),
      new OrphansValidator(),
      new StructureValidator(),
      new TitleValidator(),
      new StaleValidator(),
      new EmptyFoldersValidator(),
      new NamingValidator()
    ];

    for (const validator of validators) {
      this.validators.set(validator.id, validator);
      this.enabledValidators.add(validator.id); // Enable all by default
    }
  }

  /**
   * Enable or disable a validator
   */
  setValidatorEnabled(id: string, enabled: boolean): void {
    if (!this.validators.has(id)) return;

    if (enabled) {
      this.enabledValidators.add(id);
    } else {
      this.enabledValidators.delete(id);
    }
  }

  /**
   * Get all registered validators
   */
  getValidators(): Validator[] {
    return Array.from(this.validators.values());
  }

  /**
   * Get enabled validators
   */
  getEnabledValidators(): Validator[] {
    return Array.from(this.validators.values())
      .filter(v => this.enabledValidators.has(v.id));
  }

  /**
   * Validate a single file
   */
  async validateFile(file: TFile): Promise<Issue[]> {
    if (!file.name.endsWith(".md")) return [];
    if (!Document.isInCARFPath(file.path)) return [];

    const document = await this.metadataService.parseDocument(file);
    const issues: Issue[] = [];

    // Run local validators
    for (const validator of this.getEnabledValidators()) {
      if (!validator.isGlobal && validator.validateFile) {
        const validatorIssues = await validator.validateFile(document, this.app);
        issues.push(...validatorIssues);
      }
    }

    return issues;
  }

  /**
   * Validate all files in the vault
   */
  async validateAll(): Promise<ValidationResult> {
    const files = this.getCARFFiles();
    const documents: Document[] = [];
    const issues: Issue[] = [];

    // Parse all documents
    for (const file of files) {
      const document = await this.metadataService.parseDocument(file);
      documents.push(document);
    }

    // Run local validators on each document
    for (const document of documents) {
      for (const validator of this.getEnabledValidators()) {
        if (!validator.isGlobal && validator.validateFile) {
          const validatorIssues = await validator.validateFile(document, this.app);
          issues.push(...validatorIssues);
        }
      }
    }

    // Run global validators
    for (const validator of this.getEnabledValidators()) {
      if (validator.isGlobal && validator.validateAll) {
        const validatorIssues = await validator.validateAll(documents, this.app);
        issues.push(...validatorIssues);
      }
    }

    // Sort issues
    issues.sort(Issue.compare);

    const result: ValidationResult = {
      issues: issues,
      summary: calculateIssueSummary(issues),
      documents: documents,
      timestamp: new Date()
    };

    this.lastResult = result;
    return result;
  }

  /**
   * Get the last validation result
   */
  getLastResult(): ValidationResult | null {
    return this.lastResult;
  }

  /**
   * Get all markdown files in vault (except .obsidian, .git, node_modules)
   */
  private getCARFFiles(): TFile[] {
    const ignorePaths = [".obsidian", ".git", "node_modules", ".plugins", ".scripts"];

    return this.app.vault.getMarkdownFiles().filter(file => {
      return !ignorePaths.some(p => file.path.startsWith(p + "/") || file.path.startsWith(p));
    });
  }

  /**
   * Get documents by status
   */
  getDocumentsByStatus(documents: Document[]): {
    review: Document[];
    approved: Document[];
    rejected: Document[];
  } {
    return {
      review: documents.filter(d => d.status === "review"),
      approved: documents.filter(d => d.status === "approved"),
      rejected: documents.filter(d => d.status === "rejected")
    };
  }

  /**
   * Get issues grouped by validator
   */
  getIssuesByValidator(issues: Issue[]): Map<string, Issue[]> {
    const grouped = new Map<string, Issue[]>();

    for (const issue of issues) {
      const existing = grouped.get(issue.validator) || [];
      existing.push(issue);
      grouped.set(issue.validator, existing);
    }

    return grouped;
  }
}
