import { App } from "obsidian";
import { Document } from "../core/Document";
import { Issue, IssueSummary, calculateIssueSummary } from "../core/Issue";
import { DocsLinterConfig } from "../config/ConfigSchema";
import { ValidatorRegistry } from "../validators/ValidatorRegistry";
import { ValidatorContext } from "../validators/base/Validator";
import { createValidatorContext } from "../validators/base/ValidatorContext";
import { TemplateService } from "./TemplateService";
import { I18nService } from "../i18n/I18nService";
import { TypeRegistry } from "./TypeRegistry";

/**
 * Validation result for a single document
 */
export interface DocumentValidationResult {
  document: Document;
  issues: Issue[];
}

/**
 * Validation result for all documents
 */
export interface ValidationResult {
  documentResults: Map<string, DocumentValidationResult>;
  allIssues: Issue[];
  summary: IssueSummary;
}

/**
 * Service for running validation across documents
 */
export class ValidationService {
  private app: App;
  private registry: ValidatorRegistry;
  private templateService: TemplateService;
  private i18n: I18nService;
  private typeRegistry: TypeRegistry;

  constructor(
    app: App,
    registry: ValidatorRegistry,
    templateService: TemplateService,
    i18n: I18nService,
    typeRegistry: TypeRegistry
  ) {
    this.app = app;
    this.registry = registry;
    this.templateService = templateService;
    this.i18n = i18n;
    this.typeRegistry = typeRegistry;
  }

  /**
   * Validate all documents
   */
  async validateAll(
    documents: Document[],
    config: DocsLinterConfig
  ): Promise<ValidationResult> {
    const documentResults = new Map<string, DocumentValidationResult>();
    const allIssues: Issue[] = [];

    // Run local validators on each document
    const localValidators = this.registry.getEnabledLocalValidators(config);

    for (const doc of documents) {
      const docIssues: Issue[] = [];

      // Get template validation for this document
      const templateValidation = this.templateService.getTemplateValidation(doc);

      // Create context for this document
      const ctx = createValidatorContext(
        this.app,
        config,
        doc,
        (key, params) => this.i18n.t(key, params),
        templateValidation,
        documents,
        this.typeRegistry
      );

      // Run each local validator
      for (const validator of localValidators) {
        if (validator.validate) {
          try {
            const issues = await validator.validate(doc, ctx);
            docIssues.push(...issues);
          } catch (e) {
            console.error(`Validator ${validator.id} failed on ${doc.file.path}:`, e);
          }
        }
      }

      documentResults.set(doc.file.path, { document: doc, issues: docIssues });
      allIssues.push(...docIssues);
    }

    // Run global validators
    const globalValidators = this.registry.getEnabledGlobalValidators(config);

    for (const validator of globalValidators) {
      if (validator.validateAll) {
        try {
          // Create a generic context for global validators
          const ctx: ValidatorContext = {
            app: this.app,
            config,
            documentTypeConfig: null,
            templateValidation: null,
            t: (key, params) => this.i18n.t(key, params),
            allDocuments: documents
          };

          const issues = await validator.validateAll(documents, ctx);

          // Distribute issues to their respective documents
          for (const issue of issues) {
            const result = documentResults.get(issue.file.path);
            if (result) {
              result.issues.push(issue);
            }
            allIssues.push(issue);
          }
        } catch (e) {
          console.error(`Global validator ${validator.id} failed:`, e);
        }
      }
    }

    // Sort all issues
    allIssues.sort(Issue.compare);

    return {
      documentResults,
      allIssues,
      summary: calculateIssueSummary(allIssues)
    };
  }

  /**
   * Validate a single document
   */
  async validateDocument(
    doc: Document,
    config: DocsLinterConfig,
    allDocuments?: Document[]
  ): Promise<Issue[]> {
    const issues: Issue[] = [];
    const localValidators = this.registry.getEnabledLocalValidators(config);

    // Get template validation
    const templateValidation = this.templateService.getTemplateValidation(doc);

    // Create context
    const ctx = createValidatorContext(
      this.app,
      config,
      doc,
      (key, params) => this.i18n.t(key, params),
      templateValidation,
      allDocuments,
      this.typeRegistry
    );

    // Run validators
    for (const validator of localValidators) {
      if (validator.validate) {
        try {
          const validatorIssues = await validator.validate(doc, ctx);
          issues.push(...validatorIssues);
        } catch (e) {
          console.error(`Validator ${validator.id} failed on ${doc.file.path}:`, e);
        }
      }
    }

    issues.sort(Issue.compare);
    return issues;
  }
}
