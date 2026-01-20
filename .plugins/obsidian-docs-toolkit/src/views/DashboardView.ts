import { ItemView, WorkspaceLeaf } from "obsidian";
import { DocumentStore, StoreState } from "../store/DocumentStore";
import { Issue } from "../models/Issue";
import { Status } from "../models/types";

export const DASHBOARD_VIEW_TYPE = "docs-toolkit-dashboard";

export class DashboardView extends ItemView {
  private store: DocumentStore;
  private onStartReview: () => void;
  private expanded = false;

  constructor(leaf: WorkspaceLeaf, store: DocumentStore, onStartReview: () => void) {
    super(leaf);
    this.store = store;
    this.onStartReview = onStartReview;
  }

  getViewType(): string { return DASHBOARD_VIEW_TYPE; }
  getDisplayText(): string { return "Docs"; }
  getIcon(): string { return "file-check"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("docs-toolkit-dashboard");

    // Subscribe to store changes using registerEvent for auto-cleanup
    this.registerEvent(
      // @ts-ignore - Events class is compatible
      this.store.on("state-changed", () => this.render())
    );

    this.render();
  }

  private render(): void {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    const state = this.store.getState();

    // Loading state
    if (this.store.isLoading()) {
      el.createSpan({ text: "loading...", cls: "docs-loading" });
      return;
    }

    // Filter out READMEs
    const docs = state.documents.filter(d => d.file.name !== "README.md");
    const approved = docs.filter(d => d.status === Status.APPROVED).length;
    const pending = docs.filter(d => d.status === Status.REVIEW).length;

    // Filter issues to match docs
    const docPaths = new Set(docs.map(d => d.file.path));
    const issues = state.issues.filter(i => docPaths.has(i.file.path));
    const errors = issues.filter(i => i.severity === "error").length;
    const warnings = issues.filter(i => i.severity === "warning").length;

    // Main stats line
    const statsLine = el.createDiv({ cls: "docs-stats-line" });
    statsLine.createSpan({ text: `${approved}/${docs.length}`, cls: "docs-stat-main" });
    statsLine.createSpan({ text: " approved", cls: "docs-stat-label" });

    // Pending line with review button
    if (pending > 0) {
      const pendingLine = el.createDiv({ cls: "docs-pending-line" });
      pendingLine.createSpan({ text: `${pending} pending`, cls: "docs-pending-count" });
      const reviewBtn = pendingLine.createEl("button", { text: "Review", cls: "docs-review-btn" });
      reviewBtn.onclick = () => this.onStartReview();
    }

    // Issues summary
    if (errors > 0 || warnings > 0) {
      const issuesLine = el.createDiv({ cls: "docs-issues-line" });
      const parts: string[] = [];
      if (errors > 0) parts.push(`${errors} errors`);
      if (warnings > 0) parts.push(`${warnings} warnings`);

      const summary = issuesLine.createSpan({ text: parts.join(" \u00b7 "), cls: "docs-issues-summary" });
      summary.onclick = () => {
        this.expanded = !this.expanded;
        this.render();
      };

      // Expandable issue list
      if (this.expanded && issues.length > 0) {
        const list = el.createDiv({ cls: "docs-issues-list" });
        for (const issue of issues.slice(0, 20)) {
          const row = list.createDiv({ cls: "docs-issue-row" });
          row.textContent = `${issue.icon} ${issue.file.basename}: ${issue.message}`;
          row.onclick = () => this.openIssue(issue);
        }
        if (issues.length > 20) {
          list.createDiv({ text: `+${issues.length - 20} more`, cls: "docs-more" });
        }
      }
    }
  }

  private async openIssue(issue: Issue): Promise<void> {
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(issue.file);
    if (issue.line) {
      // @ts-ignore
      const editor = leaf.view?.editor;
      if (editor) editor.setCursor({ line: issue.line - 1, ch: 0 });
    }
  }
}
