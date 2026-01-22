import { App, TFile } from "obsidian";
import { FixAction, FixContext, FixResult } from "../core/FixAction";

/**
 * Service for applying fixes to documents
 *
 * This service handles the actual modification of files when a user
 * applies a fix action from the Issues panel.
 *
 * Supports three action types:
 * - insert-frontmatter: Insert YAML frontmatter scaffold at the beginning
 * - set-field: Set a frontmatter field value
 * - remove-field: Remove a frontmatter field
 */
export class FixService {
  constructor(private app: App) {}

  /**
   * Apply a fix action to a file
   *
   * @param context - The fix context containing file, action, and user input
   * @returns Result of the fix operation
   */
  async applyFix(context: FixContext): Promise<FixResult> {
    const { file, action } = context;

    // Validate file exists
    if (!this.app.vault.getAbstractFileByPath(file.path)) {
      return {
        success: false,
        message: `File not found: ${file.path}`,
        shouldRevalidate: false,
        error: new Error(`File not found: ${file.path}`)
      };
    }

    try {
      switch (action.actionType || "set-field") {
        case "insert-frontmatter":
          return await this.insertFrontmatter(context);
        case "set-field":
          return await this.setFrontmatterField(context);
        case "remove-field":
          return await this.removeFrontmatterField(context);
        default:
          return {
            success: false,
            message: `Unknown action type: ${action.actionType}`,
            shouldRevalidate: false
          };
      }
    } catch (error) {
      return {
        success: false,
        message: `Failed to apply fix: ${(error as Error).message}`,
        shouldRevalidate: false,
        error: error as Error
      };
    }
  }

  /**
   * Apply multiple auto fixes to a file
   * Only applies fixes with kind="auto"
   *
   * @param file - Target file
   * @param fixes - Array of fix actions (non-auto will be skipped)
   * @returns Results for each fix
   */
  async applyAutoFixes(file: TFile, fixes: FixAction[]): Promise<FixResult[]> {
    const results: FixResult[] = [];
    const autoFixes = fixes.filter(f => f.kind === "auto");

    for (const action of autoFixes) {
      const result = await this.applyFix({ file, action });
      results.push(result);

      // Stop on first failure
      if (!result.success) {
        break;
      }
    }

    return results;
  }

  /**
   * Get the resolved value for a fix action
   * For auto: returns autoValue
   * For pick: returns selectedOption
   * For prompt: returns promptValue
   */
  getResolvedValue(context: FixContext): unknown {
    const { action, selectedOption, promptValue } = context;

    switch (action.kind) {
      case "auto":
        return action.autoValue;
      case "pick":
        return selectedOption;
      case "prompt":
        return promptValue;
      default:
        return undefined;
    }
  }

  /**
   * Insert frontmatter scaffold at the beginning of a file
   * PR2: Full implementation
   */
  private async insertFrontmatter(context: FixContext): Promise<FixResult> {
    // Stub - will be implemented in PR2
    const { file, action } = context;
    const scaffold = action.autoValue as string;

    if (!scaffold) {
      return {
        success: false,
        message: "No scaffold content provided",
        shouldRevalidate: false
      };
    }

    const content = await this.app.vault.read(file);

    // Check if frontmatter already exists
    if (content.trimStart().startsWith("---")) {
      return {
        success: false,
        message: "File already has frontmatter",
        shouldRevalidate: false
      };
    }

    const newContent = scaffold + "\n" + content;
    await this.app.vault.modify(file, newContent);

    return {
      success: true,
      message: "Frontmatter inserted",
      shouldRevalidate: true
    };
  }

  /**
   * Set a single frontmatter field
   * PR2: Full implementation
   */
  private async setFrontmatterField(context: FixContext): Promise<FixResult> {
    const { file, action } = context;
    const targetField = action.targetField;

    if (!targetField) {
      return {
        success: false,
        message: "No target field specified",
        shouldRevalidate: false
      };
    }

    const value = this.getResolvedValue(context);

    if (value === undefined) {
      return {
        success: false,
        message: "No value to set",
        shouldRevalidate: false
      };
    }

    // Use Obsidian's processFrontMatter for safe YAML manipulation
    await this.app.fileManager.processFrontMatter(file, (fm) => {
      fm[targetField] = value;
    });

    return {
      success: true,
      message: `Set ${targetField} = ${JSON.stringify(value)}`,
      shouldRevalidate: true
    };
  }

  /**
   * Remove a frontmatter field
   * PR2: Full implementation
   */
  private async removeFrontmatterField(context: FixContext): Promise<FixResult> {
    const { file, action } = context;
    const targetField = action.targetField;

    if (!targetField) {
      return {
        success: false,
        message: "No target field specified",
        shouldRevalidate: false
      };
    }

    await this.app.fileManager.processFrontMatter(file, (fm) => {
      delete fm[targetField];
    });

    return {
      success: true,
      message: `Removed field: ${targetField}`,
      shouldRevalidate: true
    };
  }
}
