import { ItemView, WorkspaceLeaf, TFile } from "obsidian";
import { DocumentStore } from "../store/DocumentStore";
import { MetadataService } from "../services/MetadataService";
import { Document } from "../models/Document";
import { Status } from "../models/types";
import { Issue } from "../models/Issue";

export const REVIEW_VIEW_TYPE = "docs-toolkit-review";

export class ReviewView extends ItemView {
  private store: DocumentStore;
  private metadataService: MetadataService;
  private index = 0;

  constructor(
    leaf: WorkspaceLeaf,
    store: DocumentStore,
    metadataService: MetadataService
  ) {
    super(leaf);
    this.store = store;
    this.metadataService = metadataService;
  }

  getViewType(): string { return REVIEW_VIEW_TYPE; }
  getDisplayText(): string { return "Review"; }
  getIcon(): string { return "check-square"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("docs-rv");

    // Subscribe to store changes
    this.registerEvent(
      // @ts-ignore - Events class is compatible
      this.store.on("state-changed", () => this.render())
    );

    // Keyboard shortcuts
    this.registerDomEvent(document, "keydown", this.onKey.bind(this));

    this.render();
  }

  private getQueue(): TFile[] {
    return this.store.getReviewQueue();
  }

  private render(): void {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    const queue = this.getQueue();

    // Empty state
    if (queue.length === 0) {
      const empty = el.createDiv({ cls: "docs-rv-empty" });
      empty.createEl("div", { text: "\u2713", cls: "docs-rv-done-icon" });
      empty.createEl("div", { text: "All done", cls: "docs-rv-done-text" });
      return;
    }

    // Clamp index
    if (this.index >= queue.length) this.index = queue.length - 1;
    if (this.index < 0) this.index = 0;

    const file = queue[this.index];
    const doc = this.store.getDocument(file.path);
    const issues = this.store.getIssuesForFile(file.path);

    // Header line: counter + ID
    const header = el.createDiv({ cls: "docs-rv-header" });
    header.createSpan({ text: `${this.index + 1}/${queue.length}`, cls: "docs-rv-counter" });
    header.createSpan({ text: "  " });
    header.createSpan({ text: doc?.id || file.basename, cls: "docs-rv-id" });

    // Issues (compact)
    if (issues.length > 0) {
      const issuesEl = el.createDiv({ cls: "docs-rv-issues" });
      issuesEl.createDiv({ text: `${issues.length} issue${issues.length > 1 ? 's' : ''}:`, cls: "docs-rv-issues-title" });
      for (const issue of issues.slice(0, 5)) {
        issuesEl.createDiv({ text: `\u00b7 ${issue.message}`, cls: "docs-rv-issue" });
      }
      if (issues.length > 5) {
        issuesEl.createDiv({ text: `+${issues.length - 5} more`, cls: "docs-rv-more" });
      }
    }

    // Init frontmatter button if missing
    if (doc && !doc.frontmatter) {
      const initBtn = el.createEl("button", {
        text: "init yaml",
        cls: "docs-rv-init"
      });
      initBtn.onclick = () => this.initYaml(file);
    }

    // Actions bar
    const actions = el.createDiv({ cls: "docs-rv-actions" });

    const prevBtn = actions.createEl("button", { text: "\u2190", cls: "docs-rv-btn" });
    prevBtn.disabled = this.index === 0;
    prevBtn.onclick = () => this.prev();

    const rejectBtn = actions.createEl("button", { text: "\u2717", cls: "docs-rv-btn docs-rv-reject" });
    rejectBtn.onclick = () => this.reject(file);

    const approveBtn = actions.createEl("button", { text: "\u2713", cls: "docs-rv-btn docs-rv-approve" });
    approveBtn.onclick = () => this.approve(file);

    const nextBtn = actions.createEl("button", { text: "\u2192", cls: "docs-rv-btn" });
    nextBtn.disabled = this.index >= queue.length - 1;
    nextBtn.onclick = () => this.next();

    const openBtn = actions.createEl("button", { text: "open", cls: "docs-rv-btn docs-rv-open" });
    openBtn.onclick = () => this.openInEditor(file);
  }

  private async approve(file: TFile): Promise<void> {
    await this.store.setStatus(file, Status.APPROVED);
    // Index will be auto-adjusted in render() after state-changed event
  }

  private async reject(file: TFile): Promise<void> {
    await this.store.setStatus(file, Status.REJECTED);
  }

  private next(): void {
    const queue = this.getQueue();
    if (this.index < queue.length - 1) {
      this.index++;
      this.render();
    }
  }

  private prev(): void {
    if (this.index > 0) {
      this.index--;
      this.render();
    }
  }

  private async openInEditor(file: TFile): Promise<void> {
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(file);
  }

  private async initYaml(file: TFile): Promise<void> {
    await this.metadataService.initFrontmatter(file);
    // Store will update via vault modify event
  }

  private onKey(e: KeyboardEvent): void {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

    const queue = this.getQueue();
    if (queue.length === 0) return;

    const file = queue[this.index];
    if (!file) return;

    if (e.key === "ArrowLeft") this.prev();
    else if (e.key === "ArrowRight") this.next();
    else if (e.key.toLowerCase() === "a" && !e.ctrlKey) this.approve(file);
    else if (e.key.toLowerCase() === "r" && !e.ctrlKey) this.reject(file);
  }
}
