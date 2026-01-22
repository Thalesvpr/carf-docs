import { ItemView, WorkspaceLeaf, Events, App, TFile, Notice } from "obsidian";
import { Issue } from "../core/Issue";
import { Severity } from "../core/Severity";
import { I18nService } from "../i18n/I18nService";
import { FixService } from "../services/FixService";
import { FixAction, isAutoFix, isPickFix, isPromptFix } from "../core/FixAction";
import { showPickModal, showPromptModal } from "./modals";

export const ISSUES_PANEL_VIEW_TYPE = "docs-toolkit-issues";

export interface IssuesStore extends Events {
  getState(): { issues: Issue[] };
  revalidateFile(path: string): Promise<void>;
}

/**
 * Terminal-style Problems panel
 * Shows all validation issues in a console log format
 * Includes Fix buttons for actionable issues
 */
export class IssuesPanelView extends ItemView {
  private store: IssuesStore;
  private i18n: I18nService;
  private fixService: FixService;
  private filter: "all" | "error" | "warning" = "all";

  constructor(leaf: WorkspaceLeaf, store: IssuesStore, i18n: I18nService) {
    super(leaf);
    this.store = store;
    this.i18n = i18n;
    this.fixService = new FixService(this.app);
  }

  getViewType(): string { return ISSUES_PANEL_VIEW_TYPE; }
  getDisplayText(): string { return "Problems"; }
  getIcon(): string { return "terminal"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("docs-problems-panel");
    this.registerEvent(
      // @ts-ignore
      this.store.on("state-changed", () => this.render())
    );
    this.render();
  }

  private render(): void {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    const state = this.store.getState();
    let issues = [...state.issues].sort(Issue.compare);

    // Filter
    if (this.filter === "error") {
      issues = issues.filter(i => i.severity === Severity.ERROR);
    } else if (this.filter === "warning") {
      issues = issues.filter(i => i.severity === Severity.WARNING);
    }

    const errors = state.issues.filter(i => i.severity === Severity.ERROR).length;
    const warnings = state.issues.filter(i => i.severity === Severity.WARNING).length;

    // Header
    const header = el.createDiv({ cls: "problems-header" });

    const tabs = header.createDiv({ cls: "problems-tabs" });

    const allTab = tabs.createEl("button", {
      text: `All (${state.issues.length})`,
      cls: this.filter === "all" ? "active" : ""
    });
    allTab.onclick = () => { this.filter = "all"; this.render(); };

    const errTab = tabs.createEl("button", {
      text: `Errors (${errors})`,
      cls: `tab-error ${this.filter === "error" ? "active" : ""}`
    });
    errTab.onclick = () => { this.filter = "error"; this.render(); };

    const warnTab = tabs.createEl("button", {
      text: `Warnings (${warnings})`,
      cls: `tab-warning ${this.filter === "warning" ? "active" : ""}`
    });
    warnTab.onclick = () => { this.filter = "warning"; this.render(); };

    // Terminal output
    const terminal = el.createDiv({ cls: "problems-terminal" });

    if (issues.length === 0) {
      terminal.createDiv({ text: "No problems detected.", cls: "problems-empty" });
      return;
    }

    // Group by file for cleaner output
    const byFile = new Map<string, Issue[]>();
    for (const issue of issues) {
      const path = issue.file.path;
      if (!byFile.has(path)) byFile.set(path, []);
      byFile.get(path)!.push(issue);
    }

    for (const [path, fileIssues] of byFile) {
      // File header
      const fileHeader = terminal.createDiv({ cls: "problems-file" });
      fileHeader.createSpan({ text: "→ ", cls: "problems-arrow" });
      fileHeader.createSpan({ text: path, cls: "problems-path" });
      fileHeader.createSpan({ text: ` (${fileIssues.length})`, cls: "problems-count" });

      fileHeader.onclick = async () => {
        const file = fileIssues[0].file;
        const leaf = this.app.workspace.getLeaf(false);
        await leaf.openFile(file);
      };

      // Issues for this file
      for (const issue of fileIssues) {
        const line = terminal.createDiv({ cls: "problems-line" });

        // Severity prefix
        const prefix = issue.severity === Severity.ERROR ? "ERROR" :
                       issue.severity === Severity.WARNING ? "WARN" : "INFO";
        line.createSpan({ text: `  [${prefix}]`, cls: `problems-${issue.severity}` });

        // Line number
        if (issue.line) {
          line.createSpan({ text: `:${issue.line}`, cls: "problems-linenum" });
        }

        // Validator
        line.createSpan({ text: ` (${issue.validator})`, cls: "problems-validator" });

        // Message
        const msg = this.i18n.t(issue.messageKey, issue.messageParams as Record<string, unknown>);
        line.createSpan({ text: ` ${msg}`, cls: "problems-msg" });

        // Fix buttons
        if (issue.fixes && issue.fixes.length > 0) {
          const fixContainer = line.createSpan({ cls: "problems-fixes" });

          for (const fix of issue.fixes) {
            const fixBtn = fixContainer.createEl("button", {
              text: fix.label,
              cls: `problems-fix-btn problems-fix-${fix.kind}`
            });
            fixBtn.onclick = async (e) => {
              e.stopPropagation();
              await this.applyFix(issue.file, fix);
            };
          }
        }

        // Click to navigate
        line.onclick = async () => {
          const leaf = this.app.workspace.getLeaf(false);
          await leaf.openFile(issue.file);
          if (issue.line) {
            const editor = (leaf.view as any)?.editor;
            if (editor) {
              editor.setCursor({ line: issue.line - 1, ch: 0 });
              editor.scrollIntoView({ from: { line: issue.line - 1, ch: 0 }, to: { line: issue.line - 1, ch: 0 } }, true);
            }
          }
        };
      }
    }

    // Summary at bottom
    const summary = terminal.createDiv({ cls: "problems-summary" });
    summary.createSpan({ text: `\n--- ${errors} errors, ${warnings} warnings ---`, cls: "problems-summary-text" });
  }

  /**
   * Apply a fix action to a file
   */
  private async applyFix(file: TFile, fix: FixAction): Promise<void> {
    try {
      if (isAutoFix(fix)) {
        // Auto fixes apply directly
        const result = await this.fixService.applyFix({ file, action: fix });
        if (result.success) {
          new Notice(`Fixed: ${result.message}`);
          if (result.shouldRevalidate) {
            await this.store.revalidateFile(file.path);
          }
        } else {
          new Notice(`Fix failed: ${result.message}`);
        }
      } else if (isPickFix(fix)) {
        // Pick fixes show a selection modal (single select)
        const selected = await showPickModal(
          this.app,
          fix.label,
          fix.options || [],
          false // single select
        );
        if (selected !== null) {
          const result = await this.fixService.applyFix({
            file,
            action: fix,
            selectedOption: selected as string
          });
          if (result.success) {
            new Notice(`Fixed: ${result.message}`);
            if (result.shouldRevalidate) {
              await this.store.revalidateFile(file.path);
            }
          } else {
            new Notice(`Fix failed: ${result.message}`);
          }
        }
      } else if (isPromptFix(fix)) {
        // Prompt fixes show an input modal
        const value = await showPromptModal(
          this.app,
          fix.label,
          fix.promptHint || "Enter value",
          "" // no default value
        );
        if (value !== null) {
          const result = await this.fixService.applyFix({
            file,
            action: fix,
            promptValue: value
          });
          if (result.success) {
            new Notice(`Fixed: ${result.message}`);
            if (result.shouldRevalidate) {
              await this.store.revalidateFile(file.path);
            }
          } else {
            new Notice(`Fix failed: ${result.message}`);
          }
        }
      }
    } catch (error) {
      new Notice(`Error applying fix: ${(error as Error).message}`);
    }
  }
}
