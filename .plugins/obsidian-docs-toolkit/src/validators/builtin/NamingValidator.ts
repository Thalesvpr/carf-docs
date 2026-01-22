import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates file naming conventions based on document type detection patterns
 */
export class NamingValidator extends LocalValidator {
  readonly id = "naming";
  readonly nameKey = "validators.naming.name";
  readonly descriptionKey = "validators.naming.description";
  readonly defaultSeverity = Severity.ERROR;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);

    // Skip if no document type detected or no filename detection config
    if (!ctx.documentTypeConfig?.detection?.filename) {
      return issues;
    }

    const filenameConfig = ctx.documentTypeConfig.detection.filename;

    // Check exact match first
    if (filenameConfig.exact) {
      if (doc.file.name !== filenameConfig.exact) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.naming.pattern_mismatch",
          {
            filename: doc.file.name,
            pattern: filenameConfig.exact,
            typeName: ctx.documentTypeConfig.name
          },
          undefined,
          null,
          "validators.naming.pattern_mismatch_suggestion",
          { pattern: filenameConfig.exact }
        ));
      }
      return issues;
    }

    // Check pattern match
    if (filenameConfig.pattern) {
      try {
        const regex = new RegExp(filenameConfig.pattern);

        if (!regex.test(doc.file.name)) {
          issues.push(new Issue(
            doc.file,
            this.id,
            severity,
            "validators.naming.pattern_mismatch",
            {
              filename: doc.file.name,
              pattern: filenameConfig.pattern,
              typeName: ctx.documentTypeConfig.name
            },
            undefined,
            null,
            "validators.naming.pattern_mismatch_suggestion",
            { pattern: filenameConfig.pattern }
          ));
        }
      } catch (e) {
        console.error(`Invalid regex pattern for naming validator: ${filenameConfig.pattern}`, e);
      }
    }

    return issues;
  }
}
