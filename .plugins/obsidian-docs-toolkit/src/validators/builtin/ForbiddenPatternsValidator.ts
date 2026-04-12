import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

interface MatchLocation {
  line: number;
  column: number;
  snippet: string;
}

/**
 * Validates that documents don't contain forbidden patterns
 *
 * Features:
 * - Ignores matches inside code blocks (``` ... ```)
 * - Ignores matches inside Markdown tables (lines with |)
 * - Aggregates issues per pattern (1 issue + count + examples)
 * - Calculates accurate line/column positions
 */
export class ForbiddenPatternsValidator extends LocalValidator {
  readonly id = "forbidden-patterns";
  readonly nameKey = "validators.forbiddenPatterns.name";
  readonly descriptionKey = "validators.forbiddenPatterns.description";
  readonly defaultSeverity = Severity.WARNING;

  // Max examples to include in aggregated issue
  private readonly MAX_EXAMPLES = 5;

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

    // Build a mask of lines to skip (code blocks and tables)
    const skipLines = this.buildSkipMask(lines);

    for (const pattern of templateValidation.forbidden) {
      const matches = this.findMatches(pattern, lines, skipLines);

      if (matches.length > 0) {
        // Create ONE aggregated issue per pattern
        const examples = matches.slice(0, this.MAX_EXAMPLES);
        const exampleSnippets = examples
          .map(m => `L${m.line}:${m.column} "${m.snippet}"`)
          .join("; ");

        const countInfo = matches.length > this.MAX_EXAMPLES
          ? ` (+${matches.length - this.MAX_EXAMPLES} more)`
          : "";

        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.forbiddenPatterns.aggregated",
          {
            pattern: this.getPatternLabel(pattern),
            count: matches.length,
            examples: exampleSnippets + countInfo
          },
          matches[0].line,
          matches[0].column,
          "validators.forbiddenPatterns.aggregated_suggestion",
          { pattern: this.getPatternLabel(pattern), count: matches.length }
        ));
      }
    }

    return issues;
  }

  /**
   * Build a mask indicating which lines to skip (code blocks and tables)
   */
  private buildSkipMask(lines: string[]): boolean[] {
    const skip: boolean[] = new Array(lines.length).fill(false);
    let inCodeBlock = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      // Toggle code block state
      if (line.startsWith("```")) {
        inCodeBlock = !inCodeBlock;
        skip[i] = true;
        continue;
      }

      // Skip if inside code block
      if (inCodeBlock) {
        skip[i] = true;
        continue;
      }

      // Skip Markdown table lines (contain | but aren't wiki links)
      // Table separator: |---|---| or |:---|:---:|
      // Table row: | cell | cell |
      if (this.isTableLine(line)) {
        skip[i] = true;
        continue;
      }
    }

    return skip;
  }

  /**
   * Check if a line is part of a Markdown table
   */
  private isTableLine(line: string): boolean {
    // Table separator: |---|---| or |:---|:---:|
    if (/^\|[\s:]*-+[\s:|-]*\|$/.test(line)) {
      return true;
    }

    // Table row: starts and ends with |, has multiple cells
    if (/^\|.*\|$/.test(line) && (line.match(/\|/g) || []).length >= 2) {
      return true;
    }

    return false;
  }

  /**
   * Find all matches of a pattern, respecting skip mask
   */
  private findMatches(pattern: string, lines: string[], skipLines: boolean[]): MatchLocation[] {
    const matches: MatchLocation[] = [];

    // Check if pattern should match whole line only (placeholder detection)
    const isPlaceholder = this.isPlaceholderPattern(pattern);

    for (let lineNum = 0; lineNum < lines.length; lineNum++) {
      if (skipLines[lineNum]) continue;

      const line = lines[lineNum];

      if (isPlaceholder) {
        // For placeholders, only match if line equals pattern (trimmed)
        if (line.trim() === pattern) {
          matches.push({
            line: lineNum + 1,
            column: line.indexOf(pattern),
            snippet: this.truncate(line, 40)
          });
        }
      } else {
        // For regular patterns, find all occurrences
        try {
          const regex = new RegExp(this.escapeRegex(pattern), "gi");
          let match;

          while ((match = regex.exec(line)) !== null) {
            matches.push({
              line: lineNum + 1,
              column: match.index,
              snippet: this.truncate(line, 40)
            });

            if (match[0].length === 0) {
              regex.lastIndex++;
            }
          }
        } catch {
          // Fallback to indexOf
          let index = 0;
          while ((index = line.indexOf(pattern, index)) !== -1) {
            matches.push({
              line: lineNum + 1,
              column: index,
              snippet: this.truncate(line, 40)
            });
            index += pattern.length || 1;
          }
        }
      }
    }

    return matches;
  }

  /**
   * Check if pattern looks like a placeholder (template marker)
   * Placeholders: |--|, |-|, <TEMPLATE:...>, {{...}}, etc.
   */
  private isPlaceholderPattern(pattern: string): boolean {
    // Table-like patterns that could be placeholders
    if (/^\|[-|]+\|$/.test(pattern)) {
      return true;
    }

    // Template markers
    if (/^<TEMPLATE:.+>$/.test(pattern)) {
      return true;
    }

    // Mustache-style placeholders
    if (/^\{\{.+\}\}$/.test(pattern)) {
      return true;
    }

    return false;
  }

  /**
   * Escape special regex characters
   */
  private escapeRegex(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  /**
   * Truncate string with ellipsis
   */
  private truncate(str: string, maxLen: number): string {
    if (str.length <= maxLen) return str;
    return str.substring(0, maxLen - 3) + "...";
  }

  /**
   * Get human-readable label for pattern
   */
  private getPatternLabel(pattern: string): string {
    const labels: Record<string, string> = {
      "```": "Code block",
      "http": "Link/URL",
      "|--|": "Table",
      "- [": "Checklist"
    };
    return labels[pattern] || `"${pattern}"`;
  }
}
