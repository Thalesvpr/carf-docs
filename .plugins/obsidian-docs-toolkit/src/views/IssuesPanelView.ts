import { ItemView, WorkspaceLeaf, TFile, Events } from "obsidian";
import { Issue } from "../core/Issue";
import { Severity } from "../core/Severity";
import { I18nService } from "../i18n/I18nService";

/**
 * IssuesPanelView - IDE-style problems panel
 *
 * Inspired by VS Code's "Problems" panel:
 * - Lists all issues (errors, warnings, info)
 * - Groups by file
 * - Click to navigate to file/line
 * - Filters by severity
 * - Counter in header
 */

export const ISSUES_PANEL_VIEW_TYPE = "docs-toolkit-issues";

type FilterMode = "all" | "errors" | "warnings";
type GroupMode = "file" | "flat";

/**
 * Interface for the store that provides issues
 */
export interface IssuesStore extends Events {
  getState(): { issues: Issue[] };
}

export class IssuesPanelView extends ItemView {
  private store: IssuesStore;
  private i18n: I18nService;
  private filterMode: FilterMode = "all";
  private groupMode: GroupMode = "file";
  private collapsedFiles: Set<string> = new Set();

  constructor(leaf: WorkspaceLeaf, store: IssuesStore, i18n: I18nService) {
    super(leaf);
    this.store = store;
    this.i18n = i18n;
  }

  getViewType(): string { return ISSUES_PANEL_VIEW_TYPE; }
  getDisplayText(): string { return this.i18n.t("ui.issues.title"); }
  getIcon(): string { return "alert-triangle"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("docs-issues-panel");

    // Subscribe to store changes
    this.registerEvent(
      // @ts-ignore
      this.store.on("state-changed", () => this.render())
    );

    this.render();
  }

  /**
   * Get filtered issues based on current filter mode
   */
  private getFilteredIssues(): Issue[] {
    const state = this.store.getState();
    let issues = [...state.issues];

    // Filter by severity
    if (this.filterMode === "errors") {
      issues = issues.filter(i => i.severity === Severity.ERROR);
    } else if (this.filterMode === "warnings") {
      issues = issues.filter(i => i.severity === Severity.WARNING);
    }

    // Sort: errors first, then warnings, then info
    issues.sort(Issue.compare);

    return issues;
  }

  /**
   * Group issues by file
   */
  private groupByFile(issues: Issue[]): Map<string, Issue[]> {
    const grouped = new Map<string, Issue[]>();

    for (const issue of issues) {
      const path = issue.file.path;
      if (!grouped.has(path)) {
        grouped.set(path, []);
      }
      grouped.get(path)!.push(issue);
    }

    return grouped;
  }

  /**
   * Get translated message for an issue
   */
  private getIssueMessage(issue: Issue): string {
    return this.i18n.t(issue.messageKey, issue.messageParams as Record<string, unknown>);
  }

  /**
   * Main render function
   */
  private render(): void {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    const state = this.store.getState();
    const allIssues = state.issues;
    const filteredIssues = this.getFilteredIssues();

    // Count by severity
    const errorCount = allIssues.filter(i => i.severity === Severity.ERROR).length;
    const warningCount = allIssues.filter(i => i.severity === Severity.WARNING).length;
    const infoCount = allIssues.filter(i => i.severity === Severity.INFO).length;

    // === HEADER / TOOLBAR ===
    this.renderToolbar(el, { errorCount, warningCount, infoCount, total: filteredIssues.length });

    // === ISSUES LIST ===
    if (filteredIssues.length === 0) {
      this.renderEmpty(el);
      return;
    }

    if (this.groupMode === "file") {
      this.renderGroupedByFile(el, filteredIssues);
    } else {
      this.renderFlat(el, filteredIssues);
    }
  }

  /**
   * Render toolbar with filters and counts
   */
  private renderToolbar(el: HTMLElement, counts: { errorCount: number; warningCount: number; infoCount: number; total: number }): void {
    const toolbar = el.createDiv({ cls: "docs-ip-toolbar" });

    // Filter buttons (left side)
    const filters = toolbar.createDiv({ cls: "docs-ip-filters" });

    // All
    const allBtn = filters.createEl("button", {
      cls: `docs-ip-filter-btn ${this.filterMode === "all" ? "active" : ""}`
    });
    allBtn.innerHTML = `<span class="docs-ip-filter-icon">\u2299</span> All`;
    allBtn.onclick = () => { this.filterMode = "all"; this.render(); };

    // Errors
    const errBtn = filters.createEl("button", {
      cls: `docs-ip-filter-btn docs-ip-filter-error ${this.filterMode === "errors" ? "active" : ""}`
    });
    errBtn.innerHTML = `<span class="docs-ip-icon-error">\u2717</span> ${counts.errorCount}`;
    errBtn.onclick = () => { this.filterMode = "errors"; this.render(); };

    // Warnings
    const warnBtn = filters.createEl("button", {
      cls: `docs-ip-filter-btn docs-ip-filter-warning ${this.filterMode === "warnings" ? "active" : ""}`
    });
    warnBtn.innerHTML = `<span class="docs-ip-icon-warning">\u26A0</span> ${counts.warningCount}`;
    warnBtn.onclick = () => { this.filterMode = "warnings"; this.render(); };

    // Right side: group toggle
    const actions = toolbar.createDiv({ cls: "docs-ip-actions" });

    const groupBtn = actions.createEl("button", {
      cls: "docs-ip-group-btn",
      attr: { title: this.groupMode === "file" ? "Group by file" : "Flat list" }
    });
    groupBtn.innerHTML = this.groupMode === "file" ? "\uD83D\uDCC1" : "\u2261";
    groupBtn.onclick = () => {
      this.groupMode = this.groupMode === "file" ? "flat" : "file";
      this.render();
    };

    // Collapse/expand all
    if (this.groupMode === "file") {
      const collapseBtn = actions.createEl("button", {
        cls: "docs-ip-collapse-btn",
        attr: { title: "Collapse all" }
      });
      collapseBtn.innerHTML = "\u229F";
      collapseBtn.onclick = () => {
        const grouped = this.groupByFile(this.getFilteredIssues());
        for (const path of grouped.keys()) {
          this.collapsedFiles.add(path);
        }
        this.render();
      };

      const expandBtn = actions.createEl("button", {
        cls: "docs-ip-expand-btn",
        attr: { title: "Expand all" }
      });
      expandBtn.innerHTML = "\u229E";
      expandBtn.onclick = () => {
        this.collapsedFiles.clear();
        this.render();
      };
    }
  }

  /**
   * Render empty state
   */
  private renderEmpty(el: HTMLElement): void {
    const empty = el.createDiv({ cls: "docs-ip-empty" });
    empty.createDiv({ text: "\u2713", cls: "docs-ip-empty-icon" });
    empty.createDiv({ text: this.i18n.t("ui.issues.noIssues"), cls: "docs-ip-empty-text" });
  }

  /**
   * Render issues grouped by file
   */
  private renderGroupedByFile(el: HTMLElement, issues: Issue[]): void {
    const list = el.createDiv({ cls: "docs-ip-list" });
    const grouped = this.groupByFile(issues);

    for (const [path, fileIssues] of grouped) {
      const file = fileIssues[0].file;
      const isCollapsed = this.collapsedFiles.has(path);

      // File header
      const fileHeader = list.createDiv({ cls: "docs-ip-file-header" });

      // Collapse toggle
      const toggle = fileHeader.createSpan({ cls: "docs-ip-toggle" });
      toggle.innerHTML = isCollapsed ? "\u25B6" : "\u25BC";

      // File icon
      fileHeader.createSpan({ text: "\uD83D\uDCC4", cls: "docs-ip-file-icon" });

      // File name
      const fileName = fileHeader.createSpan({ cls: "docs-ip-file-name" });
      fileName.textContent = file.basename;

      // File path (truncated)
      const filePath = fileHeader.createSpan({ cls: "docs-ip-file-path" });
      const pathParts = path.split("/");
      if (pathParts.length > 2) {
        filePath.textContent = pathParts.slice(0, -1).join("/");
      }

      // Issue count badge
      const errCount = fileIssues.filter(i => i.severity === Severity.ERROR).length;
      const warnCount = fileIssues.filter(i => i.severity === Severity.WARNING).length;

      const badges = fileHeader.createSpan({ cls: "docs-ip-file-badges" });
      if (errCount > 0) {
        badges.createSpan({ text: `${errCount}`, cls: "docs-ip-badge docs-ip-badge-error" });
      }
      if (warnCount > 0) {
        badges.createSpan({ text: `${warnCount}`, cls: "docs-ip-badge docs-ip-badge-warning" });
      }

      // Click to toggle collapse
      fileHeader.onclick = () => {
        if (isCollapsed) {
          this.collapsedFiles.delete(path);
        } else {
          this.collapsedFiles.add(path);
        }
        this.render();
      };

      // Issues under this file
      if (!isCollapsed) {
        const issuesContainer = list.createDiv({ cls: "docs-ip-file-issues" });
        for (const issue of fileIssues) {
          this.renderIssueRow(issuesContainer, issue, false);
        }
      }
    }
  }

  /**
   * Render flat list of issues
   */
  private renderFlat(el: HTMLElement, issues: Issue[]): void {
    const list = el.createDiv({ cls: "docs-ip-list docs-ip-flat" });

    for (const issue of issues) {
      this.renderIssueRow(list, issue, true);
    }
  }

  /**
   * Render a single issue row
   */
  private renderIssueRow(container: HTMLElement, issue: Issue, showFile: boolean): void {
    const row = container.createDiv({ cls: `docs-ip-row docs-ip-${issue.severity}` });

    // Severity icon
    const icon = row.createSpan({ cls: "docs-ip-row-icon" });
    icon.innerHTML = issue.icon;

    // Message (translated)
    const message = row.createSpan({ cls: "docs-ip-row-message" });
    message.textContent = this.getIssueMessage(issue);

    // Source info
    const source = row.createSpan({ cls: "docs-ip-row-source" });

    if (showFile) {
      source.createSpan({ text: issue.file.basename, cls: "docs-ip-row-file" });
    }

    if (issue.line) {
      source.createSpan({ text: `:${issue.line}`, cls: "docs-ip-row-line" });
    }

    // Validator tag
    const tag = row.createSpan({ cls: "docs-ip-row-tag" });
    tag.textContent = issue.validator;

    // Click to navigate
    row.onclick = () => this.navigateToIssue(issue);
  }

  /**
   * Navigate to the file/line of an issue
   */
  private async navigateToIssue(issue: Issue): Promise<void> {
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(issue.file);

    // Move cursor to line if available
    if (issue.line) {
      // @ts-ignore
      const editor = leaf.view?.editor;
      if (editor) {
        editor.setCursor({ line: issue.line - 1, ch: 0 });
        editor.scrollIntoView({ from: { line: issue.line - 1, ch: 0 }, to: { line: issue.line - 1, ch: 0 } }, true);
      }
    }
  }
}
