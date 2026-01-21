import { ItemView, WorkspaceLeaf, TFile, Modal, App, TextAreaComponent } from "obsidian";
import { DocumentStore } from "../store/DocumentStore";
import { MetadataService } from "../services/MetadataService";
import { Document } from "../models/Document";
import { Status } from "../models/types";

/**
 * CurationPanelView - Painel lateral de curadoria contínua
 *
 * NOVO FLUXO DE CURADORIA:
 * ========================
 *
 * Este painel substitui a antiga separação entre Dashboard e ReviewView.
 * Agora toda a curadoria acontece de forma contínua e lateral:
 *
 * 1. O painel fica fixo na sidebar direita
 * 2. Mostra progresso geral (aprovados/total, pendentes)
 * 3. Mostra informações do arquivo atual em análise
 * 4. Ações (aprovar, rejeitar, pular, navegar)
 * 5. Ao navegar, o arquivo abre AUTOMATICAMENTE na área principal
 *
 * Não existe mais "modo de review". O review É simplesmente:
 * - Olhar o arquivo na área principal (editor nativo do Obsidian)
 * - Decidir usando os botões do painel lateral
 *
 * ATALHOS DE TECLADO:
 * - ← / → : Navegar entre arquivos
 * - A : Aprovar
 * - R : Rejeitar
 * - S : Pular (skip)
 */

export const CURATION_PANEL_VIEW_TYPE = "docs-toolkit-curation";

export class CurationPanelView extends ItemView {
  private store: DocumentStore;
  private metadataService: MetadataService;

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
    metadataService: MetadataService
  ) {
    super(leaf);
    this.store = store;
    this.metadataService = metadataService;
  }

  getViewType(): string { return CURATION_PANEL_VIEW_TYPE; }
  getDisplayText(): string { return "Curation"; }
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

    this.render();
  }

  /**
   * Get the review queue (pending files), filtered by folder and search query
   */
  private getQueue(): TFile[] {
    let queue = this.store.getReviewQueue();

    if (this.folderFilter) {
      queue = queue.filter(f => f.path.startsWith(this.folderFilter + "/"));
    }

    if (this.searchQuery.trim()) {
      const query = this.searchQuery.toLowerCase().trim();
      queue = queue.filter(f => {
        // Search in filename
        if (f.basename.toLowerCase().includes(query)) return true;
        // Search in path
        if (f.path.toLowerCase().includes(query)) return true;
        // Search in document ID and description
        const doc = this.store.getDocument(f.path);
        if (doc?.id?.toLowerCase().includes(query)) return true;
        if (doc?.frontmatter?.description?.toLowerCase().includes(query)) return true;
        return false;
      });
    }

    return queue;
  }

  /**
   * Get available top-level folders for filtering
   */
  private getAvailableFolders(): string[] {
    const queue = this.store.getReviewQueue();
    const folders = new Set<string>();

    for (const file of queue) {
      const parts = file.path.split("/");
      if (parts.length > 1) {
        // Add top-level folder
        folders.add(parts[0]);
        // Add second-level for PROJECTS (e.g., PROJECTS/LIB)
        if (parts[0] === "PROJECTS" && parts.length > 2) {
          folders.add(parts[0] + "/" + parts[1]);
          // Add third-level for nested libs (e.g., PROJECTS/LIB/TS)
          if (parts[1] === "LIB" && parts.length > 3) {
            folders.add(parts[0] + "/" + parts[1] + "/" + parts[2]);
          }
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
    const docs = state.documents.filter(d => d.file.name !== "README.md");
    const folderMap = new Map<string, { approved: number; rejected: number; pending: number; total: number }>();

    for (const doc of docs) {
      const parts = doc.file.path.split("/");
      // Get top-level folder or PROJECTS/X for projects
      let folder = parts[0];
      if (folder === "PROJECTS" && parts.length > 2) {
        folder = parts[0] + "/" + parts[1];
      }

      if (!folderMap.has(folder)) {
        folderMap.set(folder, { approved: 0, rejected: 0, pending: 0, total: 0 });
      }

      const stats = folderMap.get(folder)!;
      stats.total++;
      if (doc.status === Status.APPROVED) stats.approved++;
      else if (doc.status === Status.REJECTED) stats.rejected++;
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

    // Clamp index
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

    const queue = this.getQueue();
    const index = queue.findIndex(f => f.path === activeFile.path);

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
    let docs = state.documents.filter(d => d.file.name !== "README.md");
    if (this.folderFilter) {
      docs = docs.filter(d => d.file.path.startsWith(this.folderFilter + "/"));
    }
    const approved = docs.filter(d => d.status === Status.APPROVED).length;
    const rejected = docs.filter(d => d.status === Status.REJECTED).length;
    const pending = docs.filter(d => d.status === Status.REVIEW).length;
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
      this.currentIndex = 0; // Reset to first file in new filter
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

    // Debounced search
    let timeout: NodeJS.Timeout;
    input.oninput = () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        this.searchQuery = input.value;
        this.currentIndex = 0;
        this.render();
        // Re-focus input after render
        const newInput = el.querySelector(".docs-cp-search-input") as HTMLInputElement;
        if (newInput) {
          newInput.focus();
          newInput.setSelectionRange(newInput.value.length, newInput.value.length);
        }
      }, 200);
    };

    // Clear button
    if (this.searchQuery) {
      const clearBtn = section.createEl("button", { text: "×", cls: "docs-cp-search-clear" });
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

    // Header (clickable to expand/collapse)
    const header = section.createDiv({ cls: "docs-cp-stats-header" });
    header.createSpan({ text: this.statsExpanded ? "▼" : "▶", cls: "docs-cp-stats-toggle" });
    header.createSpan({ text: "Stats by folder", cls: "docs-cp-stats-title" });
    header.onclick = () => {
      this.statsExpanded = !this.statsExpanded;
      this.render();
    };

    if (!this.statsExpanded) return;

    // Stats list
    const list = section.createDiv({ cls: "docs-cp-stats-list" });
    const folderStats = this.getFolderStats();

    for (const stat of folderStats) {
      const row = list.createDiv({ cls: "docs-cp-stats-row" });

      // Folder name (clickable to filter)
      const nameEl = row.createSpan({ text: stat.folder, cls: "docs-cp-stats-folder" });
      nameEl.onclick = (e) => {
        e.stopPropagation();
        this.folderFilter = stat.folder;
        this.currentIndex = 0;
        this.render();
      };

      // Mini progress bar
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

      // Numbers
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

    // Main stat
    const mainLine = section.createDiv({ cls: "docs-cp-main-stat" });
    mainLine.createSpan({ text: `${stats.approved}`, cls: "docs-cp-stat-num docs-cp-approved" });
    mainLine.createSpan({ text: `/${stats.total}`, cls: "docs-cp-stat-total" });
    mainLine.createSpan({ text: " approved", cls: "docs-cp-stat-label" });

    // Secondary stats
    const secondaryLine = section.createDiv({ cls: "docs-cp-secondary-stats" });

    if (stats.pending > 0) {
      secondaryLine.createSpan({ text: `${stats.pending} pending`, cls: "docs-cp-pending" });
    }
    if (stats.rejected > 0) {
      if (stats.pending > 0) secondaryLine.createSpan({ text: " · " });
      secondaryLine.createSpan({ text: `${stats.rejected} rejected`, cls: "docs-cp-rejected" });
    }

    // Progress bar
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
    section.createDiv({ text: "✓", cls: "docs-cp-done-icon" });
    section.createDiv({ text: "All done!", cls: "docs-cp-done-text" });
    section.createDiv({ text: "No pending files to review", cls: "docs-cp-done-sub" });
  }

  /**
   * Render current file section
   */
  private renderCurrentFile(el: HTMLElement, file: TFile, queueLength: number): void {
    const section = el.createDiv({ cls: "docs-cp-section docs-cp-current" });

    // Header with counter
    const header = section.createDiv({ cls: "docs-cp-current-header" });
    header.createSpan({ text: `${this.currentIndex + 1}/${queueLength}`, cls: "docs-cp-counter" });

    // File name
    const doc = this.store.getDocument(file.path);
    const fileName = section.createDiv({ cls: "docs-cp-filename" });
    fileName.createSpan({ text: doc?.id || file.basename, cls: "docs-cp-file-id" });

    // Path (truncated)
    const pathParts = file.path.split("/");
    if (pathParts.length > 2) {
      const shortPath = pathParts.slice(0, -1).join("/");
      section.createDiv({ text: shortPath, cls: "docs-cp-filepath" });
    }

    // Metadata
    const meta = section.createDiv({ cls: "docs-cp-meta" });

    if (doc?.frontmatter) {
      const fm = doc.frontmatter;

      // Status badge
      const statusBadge = meta.createSpan({
        text: fm.status || "review",
        cls: `docs-cp-status-badge docs-cp-status-${fm.status || "review"}`
      });

      // Updated date
      if (fm.updated) {
        meta.createSpan({ text: ` · ${fm.updated}`, cls: "docs-cp-updated" });
      }

      // Description (if present)
      if (fm.description) {
        section.createDiv({ text: fm.description, cls: "docs-cp-description" });
      }
    } else {
      // No frontmatter warning
      const warning = section.createDiv({ cls: "docs-cp-warning" });
      warning.createSpan({ text: "⚠ No YAML frontmatter" });

      const initBtn = warning.createEl("button", { text: "init", cls: "docs-cp-init-btn" });
      initBtn.onclick = () => this.initYaml(file);
    }

    // Issues
    const issues = this.store.getIssuesForFile(file.path);
    if (issues.length > 0) {
      const issuesSection = section.createDiv({ cls: "docs-cp-issues" });

      const issuesHeader = issuesSection.createDiv({ cls: "docs-cp-issues-header" });
      issuesHeader.createSpan({ text: `⚠ ${issues.length} issue${issues.length > 1 ? "s" : ""}` });
      issuesHeader.onclick = () => {
        this.issuesExpanded = !this.issuesExpanded;
        this.render();
      };

      if (this.issuesExpanded) {
        const issuesList = issuesSection.createDiv({ cls: "docs-cp-issues-list" });
        for (const issue of issues.slice(0, 5)) {
          issuesList.createDiv({ text: `· ${issue.message}`, cls: "docs-cp-issue" });
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

    // Get current document status
    const doc = file ? this.store.getDocument(file.path) : null;
    const currentStatus = doc?.status;

    // Navigation + Actions row
    const row = section.createDiv({ cls: "docs-cp-actions-row" });

    // Previous
    const prevBtn = row.createEl("button", { text: "←", cls: "docs-cp-btn docs-cp-nav" });
    prevBtn.disabled = this.currentIndex === 0;
    prevBtn.title = "Previous (←)";
    prevBtn.onclick = () => this.navigate(-1);

    // Reject
    const rejectBtn = row.createEl("button", { text: "✗", cls: "docs-cp-btn docs-cp-reject-btn" });
    rejectBtn.disabled = !file || currentStatus === Status.REJECTED;
    rejectBtn.title = "Reject (R)";
    rejectBtn.onclick = () => file && this.reject(file);

    // Review (back to review)
    const reviewBtn = row.createEl("button", { text: "○", cls: "docs-cp-btn docs-cp-review-btn" });
    reviewBtn.disabled = !file || currentStatus === Status.REVIEW;
    reviewBtn.title = "Back to Review (V)";
    reviewBtn.onclick = () => file && this.setReview(file);

    // Approve
    const approveBtn = row.createEl("button", { text: "✓", cls: "docs-cp-btn docs-cp-approve-btn" });
    approveBtn.disabled = !file || currentStatus === Status.APPROVED;
    approveBtn.title = "Approve (A)";
    approveBtn.onclick = () => file && this.approve(file);

    // Next
    const nextBtn = row.createEl("button", { text: "→", cls: "docs-cp-btn docs-cp-nav" });
    nextBtn.disabled = this.currentIndex >= queueLength - 1;
    nextBtn.title = "Next (→)";
    nextBtn.onclick = () => this.navigate(1);

    // Keyboard hints
    const hints = section.createDiv({ cls: "docs-cp-hints" });
    hints.createSpan({ text: "← → nav · A approve · V review · R reject" });
  }

  // === ACTIONS ===

  /**
   * Navigate to previous/next file
   */
  private async navigate(delta: number): Promise<void> {
    const queue = this.getQueue();
    const newIndex = this.currentIndex + delta;

    if (newIndex < 0 || newIndex >= queue.length) return;

    this.currentIndex = newIndex;
    await this.openCurrentFile();
    this.render();
  }

  /**
   * Approve current file (clears rejection reason)
   */
  private async approve(file: TFile): Promise<void> {
    await this.store.setStatus(file, Status.APPROVED);
  }

  /**
   * Reject current file (prompts for reason)
   */
  private reject(file: TFile): void {
    new RejectModal(this.app, async (reason) => {
      await this.store.setStatus(file, Status.REJECTED, reason);
    }).open();
  }

  /**
   * Set file back to review status (clears rejection reason)
   */
  private async setReview(file: TFile): Promise<void> {
    await this.store.setStatus(file, Status.REVIEW);
  }

  /**
   * Initialize YAML frontmatter
   */
  private async initYaml(file: TFile): Promise<void> {
    await this.metadataService.initFrontmatter(file);
  }

  /**
   * Open current file in main editor area
   */
  private async openCurrentFile(): Promise<void> {
    const file = this.getCurrentFile();
    if (!file) return;

    // Open in main area (not in this leaf)
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(file);
  }

  /**
   * Keyboard handler
   */
  private onKey(e: KeyboardEvent): void {
    // Ignore if typing in input
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

    // Ignore if modifier keys (except for our shortcuts)
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    const file = this.getCurrentFile();

    switch (e.key) {
      case "ArrowLeft":
        e.preventDefault();
        this.navigate(-1);
        break;
      case "ArrowRight":
        e.preventDefault();
        this.navigate(1);
        break;
      case "a":
      case "A":
        if (file) {
          e.preventDefault();
          this.approve(file);
        }
        break;
      case "r":
      case "R":
        if (file) {
          e.preventDefault();
          this.reject(file);
        }
        break;
      case "v":
      case "V":
        if (file) {
          e.preventDefault();
          this.setReview(file);
        }
        break;
    }
  }
}

/**
 * Modal minimalista para motivo da rejeição
 */
class RejectModal extends Modal {
  private onSubmit: (reason: string) => void;
  private reason = "";

  constructor(app: App, onSubmit: (reason: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen(): void {
    const { contentEl, modalEl } = this;

    // Compact modal
    modalEl.addClass("docs-reject-modal");

    // Label pequeno
    const label = contentEl.createEl("label", { text: "Motivo da rejeição" });
    label.style.fontSize = "12px";
    label.style.color = "var(--text-muted)";
    label.style.marginBottom = "6px";
    label.style.display = "block";

    // Textarea
    const textArea = new TextAreaComponent(contentEl);
    textArea.setPlaceholder("O que precisa ser corrigido?");
    textArea.inputEl.style.width = "100%";
    textArea.inputEl.style.height = "80px";
    textArea.inputEl.style.resize = "none";
    textArea.onChange((value) => {
      this.reason = value;
    });

    // Focus
    setTimeout(() => textArea.inputEl.focus(), 10);

    // Hint + button inline
    const footer = contentEl.createDiv();
    footer.style.display = "flex";
    footer.style.justifyContent = "space-between";
    footer.style.alignItems = "center";
    footer.style.marginTop = "8px";

    const hint = footer.createSpan({ text: "Ctrl+Enter para confirmar" });
    hint.style.fontSize = "11px";
    hint.style.color = "var(--text-faint)";

    const submitBtn = footer.createEl("button", { text: "Rejeitar", cls: "mod-warning" });
    submitBtn.style.padding = "4px 12px";
    submitBtn.onclick = () => this.submit();

    // Keyboard
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
      this.onSubmit(this.reason.trim());
      this.close();
    }
  }

  onClose(): void {
    this.contentEl.empty();
  }
}
