import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates document titles based on document type configuration
 */
export class TitleValidator extends LocalValidator {
  readonly id = "title";
  readonly nameKey = "validators.title.name";
  readonly descriptionKey = "validators.title.description";
  readonly defaultSeverity = Severity.WARNING;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);
    const titleConfig = ctx.documentTypeConfig?.title;

    // Check if title exists
    if (!doc.title) {
      // Only report if title is required
      if (titleConfig?.required !== false) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.title.missing",
          {},
          undefined,
          null,
          "validators.title.missing_suggestion"
        ));
      }
      return issues;
    }

    // Validate pattern if configured
    if (titleConfig?.pattern) {
      try {
        const regex = new RegExp(titleConfig.pattern);
        const titleLine = this.findTitleLine(doc.content);

        if (!regex.test(titleLine)) {
          issues.push(new Issue(
            doc.file,
            this.id,
            severity,
            "validators.title.pattern_mismatch",
            {
              title: doc.title,
              pattern: titleConfig.pattern
            },
            this.findTitleLineNumber(doc.content),
            null,
            "validators.title.pattern_mismatch_suggestion",
            { pattern: titleConfig.pattern }
          ));
        }
      } catch (e) {
        console.error(`Invalid regex pattern for title validator: ${titleConfig.pattern}`, e);
      }
    }

    return issues;
  }

  /**
   * Find the title line in content
   */
  private findTitleLine(content: string): string {
    const match = content.match(/^#\s+(.+)$/m);
    return match ? match[0] : "";
  }

  /**
   * Find the line number of the title
   */
  private findTitleLineNumber(content: string): number {
    const lines = content.split("\n");
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].match(/^#\s+/)) {
        return i + 1;
      }
    }
    return 1;
  }
}
