import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates that documents don't contain forbidden patterns
 */
export class ForbiddenPatternsValidator extends LocalValidator {
  readonly id = "forbidden-patterns";
  readonly nameKey = "validators.forbiddenPatterns.name";
  readonly descriptionKey = "validators.forbiddenPatterns.description";
  readonly defaultSeverity = Severity.WARNING;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const templateValidation = ctx.templateValidation;

    // Skip if no forbidden patterns
    if (!templateValidation?.forbidden || templateValidation.forbidden.length === 0) {
      return issues;
    }

    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);
    const content = doc.bodyContent;
    const lines = content.split("\n");

    for (const pattern of templateValidation.forbidden) {
      try {
        // Try as regex first
        const regex = new RegExp(pattern, "gi");

        for (let lineNum = 0; lineNum < lines.length; lineNum++) {
          const line = lines[lineNum];
          let match;

          while ((match = regex.exec(line)) !== null) {
            issues.push(new Issue(
              doc.file,
              this.id,
              severity,
              "validators.forbiddenPatterns.found",
              { pattern, match: match[0] },
              lineNum + 1,
              match.index,
              "validators.forbiddenPatterns.found_suggestion",
              { pattern }
            ));

            // Prevent infinite loop for zero-length matches
            if (match[0].length === 0) {
              regex.lastIndex++;
            }
          }
        }
      } catch {
        // If not a valid regex, treat as literal string
        for (let lineNum = 0; lineNum < lines.length; lineNum++) {
          const line = lines[lineNum];
          let index = 0;

          while ((index = line.indexOf(pattern, index)) !== -1) {
            issues.push(new Issue(
              doc.file,
              this.id,
              severity,
              "validators.forbiddenPatterns.found",
              { pattern, match: pattern },
              lineNum + 1,
              index,
              "validators.forbiddenPatterns.found_suggestion",
              { pattern }
            ));
            index += pattern.length;
          }
        }
      }
    }

    return issues;
  }
}
