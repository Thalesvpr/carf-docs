import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates that documents aren't stale (not updated for too long)
 */
export class StaleValidator extends LocalValidator {
  readonly id = "stale";
  readonly nameKey = "validators.stale.name";
  readonly descriptionKey = "validators.stale.description";
  readonly defaultSeverity = Severity.INFO;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);

    // Get threshold from config (default 180 days)
    const validatorConfig = ctx.config.validators[this.id];
    const thresholdDays = (validatorConfig?.thresholdDays as number) ?? 180;

    // Use updated date from frontmatter, or fall back to file mtime
    const daysSinceUpdate = doc.daysSinceUpdated ?? doc.daysSinceModified;

    if (daysSinceUpdate > thresholdDays) {
      issues.push(new Issue(
        doc.file,
        this.id,
        severity,
        "validators.stale.outdated",
        {
          days: daysSinceUpdate,
          threshold: thresholdDays
        },
        undefined,
        null,
        "validators.stale.outdated_suggestion"
      ));
    }

    return issues;
  }
}
