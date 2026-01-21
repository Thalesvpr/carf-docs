import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates word count limits based on template validation rules
 */
export class WordCountValidator extends LocalValidator {
  readonly id = "word-count";
  readonly nameKey = "validators.wordCount.name";
  readonly descriptionKey = "validators.wordCount.description";
  readonly defaultSeverity = Severity.INFO;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const templateValidation = ctx.templateValidation;

    // Skip if no template validation rules
    if (!templateValidation) {
      return issues;
    }

    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);
    const totalWords = doc.countWords();

    // Check max_words
    if (templateValidation.max_words !== undefined) {
      if (totalWords > templateValidation.max_words) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.wordCount.exceeds_max",
          {
            count: totalWords,
            max: templateValidation.max_words
          }
        ));
      }
    }

    // Check min_words
    if (templateValidation.min_words !== undefined) {
      if (totalWords < templateValidation.min_words) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.wordCount.below_min",
          {
            count: totalWords,
            min: templateValidation.min_words
          }
        ));
      }
    }

    // Check max_words_per_section
    if (templateValidation.max_words_per_section !== undefined) {
      for (const sectionName of doc.getSectionNames()) {
        const sectionWords = doc.countWordsInSection(sectionName);

        if (sectionWords > templateValidation.max_words_per_section) {
          issues.push(new Issue(
            doc.file,
            this.id,
            severity,
            "validators.wordCount.section_exceeds_max",
            {
              section: sectionName,
              count: sectionWords,
              max: templateValidation.max_words_per_section
            }
          ));
        }
      }
    }

    return issues;
  }
}
