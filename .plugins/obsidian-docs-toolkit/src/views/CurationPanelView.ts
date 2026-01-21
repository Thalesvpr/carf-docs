import { ItemView, WorkspaceLeaf, TFile, Modal, App, TextAreaComponent, Events } from "obsidian";
import { Document } from "../core/Document";
import { Issue } from "../core/Issue";
import { I18nService } from "../i18n/I18nService";
import { DocsLinterConfig } from "../config/ConfigSchema";

/**
 * CurationPanelView - Sidebar curation panel
 *
 * Features:
 * - Progress overview (approved/total, pending)
 * - Current file info
 * - Actions (approve, reject, skip, navigate)
 * - Files open automatically in main area on navigation
 *
 * Keyboard shortcuts:
 * - Left/Right arrows: Navigate between files
 */

export const CURATION_PANEL_VIEW_TYPE = "docs-toolkit-curation";

/**
 * Interface for document store
 */
export interface DocumentStore extends Events {
  getState(): {
    documents: Document[];
    issues: Issue[];
  };
  getDocument(path: string): Document | undefined;
  getIssuesForFile(path: string): Issue[];
  getReviewQueue(): TFile[];
  setStatus(file: TFile, status: string, description?: string): Promise<void>;
  isLoading(): boolean;
}

/**
 * Interface for metadata service
 */
export interface MetadataService {
  initFrontmatter(file: TFile): Promise<Record<string, unknown> | void>;
}

export class CurationPanelView extends ItemView {
  private store: DocumentStore;
  private metadataService: MetadataService;
  private i18n: I18nService;
  private config: DocsLinterConfig;

  // Current position in queue
  private currentIndex = 0;

  // Expanded sections
  private issuesExpanded = false;

  // Folder filter (null = all folders)
  private folderFilter: string | null = null;

  // Text search filter
  private searchQuery: string = "";

  // Stats panel expanded
  private statsExpanded = false;

  constructor(
    leaf: WorkspaceLeaf,
    store: DocumentStore,
    metadataService: MetadataService,
    i18n: I18nService,
    config: DocsLinterConfig
  ) {
    super(leaf);
    this.store = store;
    this.metadataService = metadataService;
    this.i18n = i18n;
    this.config = config;
  }

  getViewType(): string { return CURATION_PANEL_VIEW_TYPE; }
  getDisplayText(): string { return this.i18n.t("ui.curation.title"); }
  getIcon(): string { return "check-square"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("docs-curation-panel");

    // Subscribe to store changes
    this.registerEvent(
      // @ts-ignore - Events class is compatible
      this.store.on("state-changed", () => this.render())
    );

    // Subscribe to active file changes to sync panel
    this.registerEvent(
      this.app.workspace.on("active-leaf-change", () => this.syncWithActiveFile())
    );

    // Keyboard shortcuts (global)
    this.registerDomEvent(document, "keydown", this.onKey.bind(this));

    // Sync with currently open file on panel open
    this.syncWithActiveFile();

    this.render();
  }

  /**
   * Update configuration
   */
  updateConfig(config: DocsLinterConfig): void {
    this.config = config;
    this.render();
  }

  /**
   * Check if file should be tracked based on config exclude paths
   */
  private isTrackedFile(path: string): boolean {
    for (const pattern of this.config.paths.exclude) {
      const regex = pattern
        .replace(/\*\*/g, ".*")
        .replace(/\*/g, "[^/]*");

      if (new RegExp(`^${regex}`).test(path)) {
        return false;
      }
    }
    return true;
  }

  /**
   * Get the review queue (all files), filtered by folder and search query
   */
  private getQueue(): TFile[] {
    let queue = this.store.getReviewQueue().filter(f => this.isTrackedFile(f.path));

    if (this.folderFilter) {
      queue = queue.filter(f => f.path.startsWith(this.folderFilter + "/"));
    }

    if (this.searchQuery.trim()) {
      const query = this.searchQuery.toLowerCase().trim();
      queue = queue.filter(f => {
        if (f.basename.toLowerCase().includes(query)) return true;
        if (f.path.toLowerCase().includes(query)) return true;
        const doc = this.store.getDocument(f.path);
        if (doc?.id?.toLowerCase().includes(query)) return true;
        const desc = doc?.getFrontmatterField<string>("description");
        if (desc?.toLowerCase().includes(query)) return true;
        return false;
      });
    }

    return queue;
  }

  /**
   * Get available top-level folders for filtering
   */
  private getAvailableFolders(): string[] {
    const queue = this.store.getReviewQueue().filter(f => this.isTrackedFile(f.path));
    const folders = new Set<string>();

    for (const file of queue) {
      const parts = file.path.split("/");
      if (parts.length > 1) {
        folders.add(parts[0]);
        // Also add second level for common patterns
        if (parts.length > 2) {
          folders.add(parts[0] + "/" + parts[1]);
        }
      }
    }

    return Array.from(folders).sort();
  }

  /**
   * Get statistics per folder
   */
  private getFolderStats(): { folder: string; approved: number; rejected: number; pending: number; total: number }[] {
    const state = this.store.getState();
    const docs = state.documents.filter(d => this.isTrackedFile(d.file.path));
    const folderMap = new Map<string, { approved: number; rejected: number; pending: number; total: number }>();

    const approvedStatus = "approved";
    const rejectedStatus = "rejected";

    for (const doc of docs) {
      const parts = doc.file.path.split("/");
      let folder = parts[0];
      if (parts.length > 2) {
        folder = parts[0] + "/" + parts[1];
      }

      if (!folderMap.has(folder)) {
        folderMap.set(folder, { approved: 0, rejected: 0, pending: 0, total: 0 });
      }

      const stats = folderMap.get(folder)!;
      stats.total++;
      if (doc.status === approvedStatus) stats.approved++;
      else if (doc.status === rejectedStatus) stats.rejected++;
      else stats.pending++;
    }

    return Array.from(folderMap.entries())
      .map(([folder, stats]) => ({ folder, ...stats }))
      .sort((a, b) => a.folder.localeCompare(b.folder));
  }

  /**
   * Get current file being reviewed
   */
  private getCurrentFile(): TFile | null {
    const queue = this.getQueue();
    if (queue.length === 0) return null;

    if (this.currentIndex >= queue.length) this.currentIndex = queue.length - 1;
    if (this.currentIndex < 0) this.currentIndex = 0;

    return queue[this.currentIndex];
  }

  /**
   * Sync panel with currently active file in editor
   */
  private syncWithActiveFile(): void {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) return;
    if (!this.isTrackedFile(activeFile.path)) return;

    let queue = this.getQueue();
    let index = queue.findIndex(f => f.path === activeFile.path);

    // If not found and we have a folder filter, try clearing it
    if (index === -1 && this.folderFilter) {
      this.folderFilter = null;
      this.searchQuery = "";
      queue = this.getQueue();
      index = queue.findIndex(f => f.path === activeFile.path);
    }

    if (index !== -1 && index !== this.currentIndex) {
      this.currentIndex = index;
      this.render();
    }
  }

  /**
   * Main render function
   */
  private render(): void {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    const state = this.store.getState();

    // Loading state
    if (this.store.isLoading()) {
      el.createDiv({ text: "Loading...", cls: "docs-cp-loading" });
      return;
    }

    // Get filtered docs based on folder filter
    let docs = state.documents.filter(d => this.isTrackedFile(d.file.path));
    if (this.folderFilter) {
      docs = docs.filter(d => d.file.path.startsWith(this.folderFilter + "/"));
    }

    const approved = docs.filter(d => d.status === "approved").length;
    const rejected = docs.filter(d => d.status === "rejected").length;
    const pending = docs.filter(d => d.status === "review").length;
    const total = docs.length;

    // === FOLDER FILTER SECTION ===
    this.renderFolderFilter(el);

    // === SEARCH SECTION ===
    this.renderSearch(el);

    // === PROGRESS SECTION ===
    this.renderProgress(el, { approved, rejected, pending, total });

    // === FOLDER STATS SECTION ===
    this.renderFolderStats(el);

    // === CURRENT FILE SECTION ===
    const queue = this.getQueue();
    const currentFile = this.getCurrentFile();

    if (queue.length === 0) {
      this.renderAllDone(el);
      return;
    }

    if (currentFile) {
      this.renderCurrentFile(el, currentFile, queue.length);
    }

    // === ACTIONS SECTION ===
    this.renderActions(el, currentFile, queue.length);
  }

  /**
   * Render folder filter dropdown
   */
  private renderFolderFilter(el: HTMLElement): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-filter" });

    const row = section.createDiv({ cls: "docs-cp-filter-row" });
    row.createSpan({ text: "Folder:", cls: "docs-cp-filter-label" });

    const select = row.createEl("select", { cls: "docs-cp-filter-select" });

    // "All" option
    const allOption = select.createEl("option", { text: "All folders", value: "" });
    if (!this.folderFilter) allOption.selected = true;

    // Folder options
    const folders = this.getAvailableFolders();
    for (const folder of folders) {
      const option = select.createEl("option", { text: folder, value: folder });
      if (this.folderFilter === folder) option.selected = true;
    }

    select.onchange = () => {
      this.folderFilter = select.value || null;
      this.currentIndex = 0;
      this.render();
    };
  }

  /**
   * Render search input
   */
  private renderSearch(el: HTMLElement): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-search" });

    const input = section.createEl("input", {
      type: "text",
      placeholder: "Search files...",
      cls: "docs-cp-search-input"
    });
    input.value = this.searchQuery;

    let timeout: NodeJS.Timeout;
    input.oninput = () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        this.searchQuery = input.value;
        this.currentIndex = 0;
        this.render();
        const newInput = el.querySelector(".docs-cp-search-input") as HTMLInputElement;
        if (newInput) {
          newInput.focus();
          newInput.setSelectionRange(newInput.value.length, newInput.value.length);
        }
      }, 200);
    };

    if (this.searchQuery) {
      const clearBtn = section.createEl("button", { text: "\u00D7", cls: "docs-cp-search-clear" });
      clearBtn.onclick = () => {
        this.searchQuery = "";
        this.currentIndex = 0;
        this.render();
      };
    }
  }

  /**
   * Render folder statistics (collapsible)
   */
  private renderFolderStats(el: HTMLElement): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-folder-stats" });

    const header = section.createDiv({ cls: "docs-cp-stats-header" });
    header.createSpan({ text: this.statsExpanded ? "\u25BC" : "\u25B6", cls: "docs-cp-stats-toggle" });
    header.createSpan({ text: "Stats by folder", cls: "docs-cp-stats-title" });
    header.onclick = () => {
      this.statsExpanded = !this.statsExpanded;
      this.render();
    };

    if (!this.statsExpanded) return;

    const list = section.createDiv({ cls: "docs-cp-stats-list" });
    const folderStats = this.getFolderStats();

    for (const stat of folderStats) {
      const row = list.createDiv({ cls: "docs-cp-stats-row" });

      const nameEl = row.createSpan({ text: stat.folder, cls: "docs-cp-stats-folder" });
      nameEl.onclick = (e) => {
        e.stopPropagation();
        this.folderFilter = stat.folder;
        this.currentIndex = 0;
        this.render();
      };

      const barContainer = row.createDiv({ cls: "docs-cp-stats-bar-container" });
      const bar = barContainer.createDiv({ cls: "docs-cp-stats-bar" });

      const approvedPct = stat.total > 0 ? (stat.approved / stat.total) * 100 : 0;
      const rejectedPct = stat.total > 0 ? (stat.rejected / stat.total) * 100 : 0;

      if (stat.approved > 0) {
        const approvedBar = bar.createDiv({ cls: "docs-cp-stats-bar-approved" });
        approvedBar.style.width = `${approvedPct}%`;
      }
      if (stat.rejected > 0) {
        const rejectedBar = bar.createDiv({ cls: "docs-cp-stats-bar-rejected" });
        rejectedBar.style.width = `${rejectedPct}%`;
      }

      const numbers = row.createSpan({ cls: "docs-cp-stats-numbers" });
      numbers.createSpan({ text: `${stat.approved}`, cls: "docs-cp-stats-num-approved" });
      numbers.createSpan({ text: `/` });
      numbers.createSpan({ text: `${stat.total}` });
    }
  }

  /**
   * Render progress section
   */
  private renderProgress(el: HTMLElement, stats: { approved: number; rejected: number; pending: number; total: number }): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-progress" });

    const mainLine = section.createDiv({ cls: "docs-cp-main-stat" });
    mainLine.createSpan({ text: `${stats.approved}`, cls: "docs-cp-stat-num docs-cp-approved" });
    mainLine.createSpan({ text: `/${stats.total}`, cls: "docs-cp-stat-total" });
    mainLine.createSpan({ text: " approved", cls: "docs-cp-stat-label" });

    const secondaryLine = section.createDiv({ cls: "docs-cp-secondary-stats" });

    if (stats.pending > 0) {
      secondaryLine.createSpan({ text: `${stats.pending} ${this.i18n.t("ui.curation.pending")}`, cls: "docs-cp-pending" });
    }
    if (stats.rejected > 0) {
      if (stats.pending > 0) secondaryLine.createSpan({ text: " \u00B7 " });
      secondaryLine.createSpan({ text: `${stats.rejected} rejected`, cls: "docs-cp-rejected" });
    }

    const progressBar = section.createDiv({ cls: "docs-cp-progress-bar" });
    const percentage = stats.total > 0 ? (stats.approved / stats.total) * 100 : 0;
    const fill = progressBar.createDiv({ cls: "docs-cp-progress-fill" });
    fill.style.width = `${percentage}%`;
  }

  /**
   * Render all done state
   */
  private renderAllDone(el: HTMLElement): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-done" });
    section.createDiv({ text: "\u2713", cls: "docs-cp-done-icon" });
    section.createDiv({ text: "All done!", cls: "docs-cp-done-text" });
    section.createDiv({ text: "No pending files to review", cls: "docs-cp-done-sub" });
  }

  /**
   * Render current file section
   */
  private renderCurrentFile(el: HTMLElement, file: TFile, queueLength: number): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-current" });

    const header = section.createDiv({ cls: "docs-cp-current-header" });
    header.createSpan({ text: `${this.currentIndex + 1}/${queueLength}`, cls: "docs-cp-counter" });

    const doc = this.store.getDocument(file.path);
    const fileName = section.createDiv({ cls: "docs-cp-filename" });
    fileName.createSpan({ text: doc?.id || file.basename, cls: "docs-cp-file-id" });

    const pathParts = file.path.split("/");
    if (pathParts.length > 2) {
      const shortPath = pathParts.slice(0, -1).join("/");
      section.createDiv({ text: shortPath, cls: "docs-cp-filepath" });
    }

    const meta = section.createDiv({ cls: "docs-cp-meta" });

    if (doc?.hasFrontmatter) {
      const status = doc.status;
      const statusConfig = this.config.workflow.statuses[status];

      const statusBadge = meta.createSpan({
        text: statusConfig?.name || status,
        cls: `docs-cp-status-badge docs-cp-status-${status}`
      });

      const updated = doc.getFrontmatterField<string>("updated");
      if (updated) {
        meta.createSpan({ text: ` \u00B7 ${updated}`, cls: "docs-cp-updated" });
      }

      const description = doc.getFrontmatterField<string>("description");
      if (description) {
        section.createDiv({ text: description, cls: "docs-cp-description" });
      }
    } else {
      const warning = section.createDiv({ cls: "docs-cp-warning" });
      warning.createSpan({ text: "\u26A0 No YAML frontmatter" });

      const initBtn = warning.createEl("button", { text: "init", cls: "docs-cp-init-btn" });
      initBtn.onclick = () => this.initYaml(file);
    }

    const issues = this.store.getIssuesForFile(file.path);
    if (issues.length > 0) {
      const issuesSection = section.createDiv({ cls: "docs-cp-issues" });

      const issuesHeader = issuesSection.createDiv({ cls: "docs-cp-issues-header" });
      issuesHeader.createSpan({ text: `\u26A0 ${issues.length} issue${issues.length > 1 ? "s" : ""}` });
      issuesHeader.onclick = () => {
        this.issuesExpanded = !this.issuesExpanded;
        this.render();
      };

      if (this.issuesExpanded) {
        const issuesList = issuesSection.createDiv({ cls: "docs-cp-issues-list" });
        for (const issue of issues.slice(0, 5)) {
          const msg = this.i18n.t(issue.messageKey, issue.messageParams as Record<string, unknown>);
          issuesList.createDiv({ text: `\u00B7 ${msg}`, cls: "docs-cp-issue" });
        }
        if (issues.length > 5) {
          issuesList.createDiv({ text: `+${issues.length - 5} more`, cls: "docs-cp-more" });
        }
      }
    }
  }

  /**
   * Render actions section
   */
  private renderActions(el: HTMLElement, file: TFile | null, queueLength: number): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-actions" });

    const doc = file ? this.store.getDocument(file.path) : null;
    const currentStatus = doc?.status;

    const row = section.createDiv({ cls: "docs-cp-actions-row" });

    // Previous
    const prevBtn = row.createEl("button", { text: "\u2190", cls: "docs-cp-btn docs-cp-nav" });
    prevBtn.disabled = this.currentIndex === 0;
    prevBtn.title = "Previous (\u2190)";
    prevBtn.onclick = () => this.navigate(-1);

    // Reject
    const rejectBtn = row.createEl("button", { text: "\u2717", cls: "docs-cp-btn docs-cp-reject-btn" });
    rejectBtn.disabled = !file || currentStatus === "rejected";
    rejectBtn.title = this.i18n.t("ui.curation.reject");
    rejectBtn.onclick = () => file && this.reject(file);

    // Review
    const reviewBtn = row.createEl("button", { text: "\u25CB", cls: "docs-cp-btn docs-cp-review-btn" });
    reviewBtn.disabled = !file || currentStatus === "review";
    reviewBtn.title = "Back to Review";
    reviewBtn.onclick = () => file && this.setReview(file);

    // Approve
    const approveBtn = row.createEl("button", { text: "\u2713", cls: "docs-cp-btn docs-cp-approve-btn" });
    approveBtn.disabled = !file || currentStatus === "approved";
    approveBtn.title = this.i18n.t("ui.curation.approve");
    approveBtn.onclick = () => file && this.approve(file);

    // Next
    const nextBtn = row.createEl("button", { text: "\u2192", cls: "docs-cp-btn docs-cp-nav" });
    nextBtn.disabled = this.currentIndex >= queueLength - 1;
    nextBtn.title = "Next (\u2192)";
    nextBtn.onclick = () => this.navigate(1);

    // Keyboard hints
    const hints = section.createDiv({ cls: "docs-cp-hints" });
    hints.createSpan({ text: "\u2190 \u2192 navigate" });
  }

  // === ACTIONS ===

  private async navigate(delta: number): Promise<void> {
    const queue = this.getQueue();
    const newIndex = this.currentIndex + delta;

    if (newIndex < 0 || newIndex >= queue.length) return;

    this.currentIndex = newIndex;
    await this.openCurrentFile();
    this.render();
  }

  private async approve(file: TFile): Promise<void> {
    await this.store.setStatus(file, "approved");
  }

  private reject(file: TFile): void {
    new RejectModal(this.app, this.i18n, async (reason) => {
      await this.store.setStatus(file, "rejected", reason);
    }).open();
  }

  private async setReview(file: TFile): Promise<void> {
    await this.store.setStatus(file, "review");
  }

  private async initYaml(file: TFile): Promise<void> {
    await this.metadataService.initFrontmatter(file);
  }

  private async openCurrentFile(): Promise<void> {
    const file = this.getCurrentFile();
    if (!file) return;

    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(file);
  }

  private onKey(e: KeyboardEvent): void {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    switch (e.key) {
      case "ArrowLeft":
        e.preventDefault();
        this.navigate(-1);
        break;
      case "ArrowRight":
        e.preventDefault();
        this.navigate(1);
        break;
    }
  }
}

/**
 * Minimal rejection reason modal
 */
class RejectModal extends Modal {
  private onSubmit: (reason: string) => void;
  private i18n: I18nService;
  private reason = "";
  private submitted = false;

  private static draft = "";

  constructor(app: App, i18n: I18nService, onSubmit: (reason: string) => void) {
    super(app);
    this.i18n = i18n;
    this.onSubmit = onSubmit;
  }

  onOpen(): void {
    const { contentEl, modalEl } = this;

    modalEl.addClass("docs-reject-modal");

    const label = contentEl.createEl("label", { text: "Rejection reason" });
    label.style.fontSize = "12px";
    label.style.color = "var(--text-muted)";
    label.style.marginBottom = "6px";
    label.style.display = "block";

    const textArea = new TextAreaComponent(contentEl);
    textArea.setPlaceholder("What needs to be fixed?");
    textArea.inputEl.style.width = "100%";
    textArea.inputEl.style.height = "80px";
    textArea.inputEl.style.resize = "none";

    if (RejectModal.draft) {
      textArea.setValue(RejectModal.draft);
      this.reason = RejectModal.draft;
    }

    textArea.onChange((value) => {
      this.reason = value;
      RejectModal.draft = value;
    });

    setTimeout(() => {
      textArea.inputEl.focus();
      textArea.inputEl.setSelectionRange(
        textArea.inputEl.value.length,
        textArea.inputEl.value.length
      );
    }, 10);

    const footer = contentEl.createDiv();
    footer.style.display = "flex";
    footer.style.justifyContent = "space-between";
    footer.style.alignItems = "center";
    footer.style.marginTop = "8px";

    const hint = footer.createSpan({ text: "Ctrl+Enter to confirm" });
    hint.style.fontSize = "11px";
    hint.style.color = "var(--text-faint)";

    const submitBtn = footer.createEl("button", { text: this.i18n.t("ui.curation.reject"), cls: "mod-warning" });
    submitBtn.style.padding = "4px 12px";
    submitBtn.onclick = () => this.submit();

    textArea.inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.submit();
      }
      if (e.key === "Escape") {
        this.close();
      }
    });
  }

  private submit(): void {
    if (this.reason.trim()) {
      this.submitted = true;
      RejectModal.draft = "";
      this.onSubmit(this.reason.trim());
      this.close();
    }
  }

  onClose(): void {
    this.contentEl.empty();
  }
}
