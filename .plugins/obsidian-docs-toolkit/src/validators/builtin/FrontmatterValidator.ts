import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";
import { FieldConfig } from "../../config/ConfigSchema";

/**
 * Validates frontmatter fields based on document type configuration
 */
export class FrontmatterValidator extends LocalValidator {
  readonly id = "frontmatter";
  readonly nameKey = "validators.frontmatter.name";
  readonly descriptionKey = "validators.frontmatter.description";
  readonly defaultSeverity = Severity.ERROR;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const typeConfig = ctx.documentTypeConfig;

    // Skip if no document type config
    if (!typeConfig?.frontmatter) {
      return issues;
    }

    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);
    const fmConfig = typeConfig.frontmatter;

    // Check if frontmatter exists
    if (!doc.hasFrontmatter) {
      issues.push(new Issue(
        doc.file,
        this.id,
        severity,
        "validators.frontmatter.missing",
        {},
        1,
        null,
        "validators.frontmatter.missing_suggestion"
      ));
      return issues;
    }

    // Check required fields
    if (fmConfig.required) {
      for (const field of fmConfig.required) {
        if (!doc.hasFrontmatterField(field)) {
          issues.push(new Issue(
            doc.file,
            this.id,
            severity,
            "validators.frontmatter.required_field",
            { field },
            1,
            null,
            "validators.frontmatter.required_field_suggestion",
            { field }
          ));
        }
      }
    }

    // Validate field configurations
    if (fmConfig.fields) {
      for (const [field, fieldConfig] of Object.entries(fmConfig.fields)) {
        const value = doc.getFrontmatterField(field);

        // Skip if field doesn't exist (handled by required check)
        if (value === undefined) continue;

        const fieldIssues = this.validateField(doc, field, value, fieldConfig, ctx, severity);
        issues.push(...fieldIssues);
      }
    }

    return issues;
  }

  /**
   * Validate a single field against its configuration
   */
  private validateField(
    doc: Document,
    field: string,
    value: unknown,
    config: FieldConfig,
    ctx: ValidatorContext,
    severity: Severity
  ): Issue[] {
    const issues: Issue[] = [];

    // Check type
    if (config.type) {
      const actualType = this.getValueType(value);
      if (actualType !== config.type) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.wrong_type",
          { field, expected: config.type, actual: actualType },
          1
        ));
        return issues; // Don't continue validation if type is wrong
      }
    }

    // Check pattern
    if (config.pattern && typeof value === "string") {
      const regex = new RegExp(config.pattern);
      if (!regex.test(value)) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.pattern_mismatch",
          { field, pattern: config.pattern, value },
          1
        ));
      }
    }

    // Check enum
    if (config.enum && typeof value === "string") {
      const normalizedValue = value.toLowerCase();
      const normalizedEnum = config.enum.map(e => e.toLowerCase());
      if (!normalizedEnum.includes(normalizedValue)) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.invalid_enum",
          { field, value, allowed: config.enum.join(", ") },
          1
        ));
      }
    }

    // Check array items
    if (config.items && Array.isArray(value)) {
      for (const item of value) {
        if (config.items.enum && typeof item === "string") {
          const normalizedItem = item.toUpperCase();
          const normalizedEnum = config.items.enum.map(e => e.toUpperCase());
          if (!normalizedEnum.includes(normalizedItem)) {
            issues.push(new Issue(
              doc.file,
              this.id,
              Severity.WARNING,
              "validators.frontmatter.invalid_array_item",
              { field, item, allowed: config.items.enum.join(", ") },
              1
            ));
          }
        }
        if (config.items.pattern && typeof item === "string") {
          const regex = new RegExp(config.items.pattern);
          if (!regex.test(item)) {
            issues.push(new Issue(
              doc.file,
              this.id,
              Severity.WARNING,
              "validators.frontmatter.array_item_pattern_mismatch",
              { field, item, pattern: config.items.pattern },
              1
            ));
          }
        }
      }
    }

    // Check min/max for numbers
    if (typeof value === "number") {
      if (config.min !== undefined && value < config.min) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.below_min",
          { field, value, min: config.min },
          1
        ));
      }
      if (config.max !== undefined && value > config.max) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.above_max",
          { field, value, max: config.max },
          1
        ));
      }
    }

    // Check min/max for strings (length)
    if (typeof value === "string") {
      if (config.min !== undefined && value.length < config.min) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.too_short",
          { field, length: value.length, min: config.min },
          1
        ));
      }
      if (config.max !== undefined && value.length > config.max) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.too_long",
          { field, length: value.length, max: config.max },
          1
        ));
      }
    }

    // Check min/max for arrays (length)
    if (Array.isArray(value)) {
      if (config.min !== undefined && value.length < config.min) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.array_too_short",
          { field, length: value.length, min: config.min },
          1
        ));
      }
      if (config.max !== undefined && value.length > config.max) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.frontmatter.array_too_long",
          { field, length: value.length, max: config.max },
          1
        ));
      }
    }

    return issues;
  }

  /**
   * Get the type of a value
   */
  private getValueType(value: unknown): string {
    if (Array.isArray(value)) return "array";
    if (value === null) return "null";
    return typeof value;
  }
}
