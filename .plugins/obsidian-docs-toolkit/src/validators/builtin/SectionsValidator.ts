import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates that documents have required sections based on document type or template
 */
export class SectionsValidator extends LocalValidator {
  readonly id = "sections";
  readonly nameKey = "validators.sections.name";
  readonly descriptionKey = "validators.sections.description";
  readonly defaultSeverity = Severity.WARNING;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);

    // Get required sections from document type config
    const typeRequired = ctx.documentTypeConfig?.sections?.required || [];

    // Get required sections from template validation
    const templateRequired = ctx.templateValidation?.required_sections || [];

    // Combine both sources (unique)
    const requiredSections = [...new Set([...typeRequired, ...templateRequired])];

    if (requiredSections.length === 0) {
      return issues;
    }

    // Get existing section names
    const existingSections = doc.getSectionNames().map(s => Document.normalizeString(s));

    for (const required of requiredSections) {
      const normalizedRequired = Document.normalizeString(required);

      // Check for exact or partial match
      const found = existingSections.some(s =>
        s === normalizedRequired ||
        s.includes(normalizedRequired) ||
        normalizedRequired.includes(s)
      );

      if (!found) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.sections.missing_required",
          { section: required },
          undefined,
          null,
          "validators.sections.missing_required_suggestion",
          { section: required }
        ));
      }
    }

    // Check forbidden sections
    const forbidden = ctx.documentTypeConfig?.sections?.forbidden || [];
    for (const forbiddenSection of forbidden) {
      if (doc.hasSection(forbiddenSection)) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.sections.forbidden",
          { section: forbiddenSection },
          undefined
        ));
      }
    }

    return issues;
  }
}
