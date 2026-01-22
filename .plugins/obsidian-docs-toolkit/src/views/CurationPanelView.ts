import { ItemView, WorkspaceLeaf, TFile, Modal, App, TextAreaComponent, Events, setIcon, prepareSimpleSearch, SearchResult } from "obsidian";
import { Document } from "../core/Document";
import { Issue } from "../core/Issue";
import { I18nService } from "../i18n/I18nService";
import { DocsLinterConfig } from "../config/ConfigSchema";
import { DocsToolkitSettings } from "../settings";
import { FilterSuggest } from "../ui/FilterSuggest";

export const CURATION_PANEL_VIEW_TYPE = "docs-toolkit-curation";

export interface DocumentStore extends Events {
  getState(): { documents: Document[]; issues: Issue[] };
  getDocument(path: string): Document | undefined;
  getIssuesForFile(path: string): Issue[];
  getReviewQueue(): TFile[];
  setStatus(file: TFile, status: string, description?: string): Promise<void>;
  isLoading(): boolean;
}

export interface MetadataService {
  initFrontmatter(file: TFile): Promise<Record<string, unknown> | void>;
}

export interface PluginRef {
  settings: DocsToolkitSettings;
}

export class CurationPanelView extends ItemView {
  private store: DocumentStore;
  private metadataService: MetadataService;
  private i18n: I18nService;
  private config: DocsLinterConfig;
  private plugin: PluginRef;
  private currentIndex = 0;
  private filterQuery = "";

  constructor(
    leaf: WorkspaceLeaf,
    store: DocumentStore,
    metadataService: MetadataService,
    i18n: I18nService,
    config: DocsLinterConfig,
    plugin: PluginRef
  ) {
    super(leaf);
    this.store = store;
    this.metadataService = metadataService;
    this.i18n = i18n;
    this.config = config;
    this.plugin = plugin;
  }

  getViewType(): string { return CURATION_PANEL_VIEW_TYPE; }
  getDisplayText(): string { return "Curation"; }
  getIcon(): string { return "check-square"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("docs-curation-panel");

    this.registerEvent(
      // @ts-ignore
      this.store.on("state-changed", () => this.render())
    );

    this.registerEvent(
      this.app.workspace.on("active-leaf-change", () => this.syncWithActiveFile())
    );

    // Listen to metadataCache changes for reactive Properties updates
    this.registerEvent(
      this.app.metadataCache.on("changed", (file) => {
        const currentFile = this.getCurrentFile();
        if (currentFile && file.path === currentFile.path) {
          // Re-render when current file's metadata changes (Properties edited)
          this.render();
        }
      })
    );

    this.registerDomEvent(document, "keydown", this.onKey.bind(this));
    this.syncWithActiveFile();
    this.render();
  }

  updateConfig(config: DocsLinterConfig): void {
    this.config = config;
    this.render();
  }

  private isTrackedFile(path: string): boolean {
    for (const pattern of this.config.paths.exclude) {
      // Use placeholder to avoid ** being affected by * replacement
      const regex = pattern
        .replace(/\*\*/g, "<<DOUBLESTAR>>")
        .replace(/\*/g, "[^/]*")
        .replace(/<<DOUBLESTAR>>/g, ".*");
      if (new RegExp(`^${regex}`).test(path)) return false;
    }
    return true;
  }

  private getQueue(): TFile[] {
    let files = this.store.getReviewQueue().filter(f => this.isTrackedFile(f.path));

    // Apply filter if set
    if (this.filterQuery.trim()) {
      files = files.filter(f => this.matchesFilter(f, this.filterQuery));
    }

    return files;
  }

  /**
   * Parse and apply filter query using Obsidian's native search API
   * Supports: path:, file:, tag:, status:, -prefix for exclusion, OR
   * Uses prepareSimpleSearch for efficient text matching
   */
  private matchesFilter(file: TFile, query: string): boolean {
    const doc = this.store.getDocument(file.path);

    // Split by OR (case insensitive)
    const orGroups = query.split(/\s+OR\s+/i);

    // Any OR group matching = true (OR logic between groups)
    for (const group of orGroups) {
      const tokens = this.parseFilterTokens(group.trim());

      // All tokens in a group must match (AND logic within group)
      let groupMatches = true;
      for (const token of tokens) {
        if (!this.matchToken(file, doc, token)) {
          groupMatches = false;
          break;
        }
      }

      if (groupMatches) return true;
    }

    return false;
  }

  private parseFilterTokens(query: string): Array<{type: string; value: string; exclude: boolean}> {
    const tokens: Array<{type: string; value: string; exclude: boolean}> = [];

    // Match quoted strings and unquoted tokens with optional operators
    // Supports: path:, file:, tag:, status:, id:, section:, line:
    const regex = /(-?)(?:(path|file|tag|status|id|section|line):)?(?:"([^"]+)"|(\S+))/gi;
    let match;

    while ((match = regex.exec(query)) !== null) {
      const exclude = match[1] === "-";
      const type = (match[2] || "text").toLowerCase();
      const value = match[3] || match[4]; // quoted or unquoted

      tokens.push({ type, value, exclude });
    }

    return tokens;
  }

  private matchToken(file: TFile, doc: Document | undefined, token: {type: string; value: string; exclude: boolean}): boolean {
    const { type, value, exclude } = token;
    let matches = false;

    // Use Obsidian's native prepareSimpleSearch for efficient matching
    const search = prepareSimpleSearch(value);

    switch (type) {
      case "path":
        matches = search(file.path) !== null;
        break;
      case "file":
        matches = search(file.name) !== null;
        break;
      case "tag":
        if (doc?.frontmatter?.tags) {
          const tags = Array.isArray(doc.frontmatter.tags)
            ? doc.frontmatter.tags
            : [doc.frontmatter.tags];
          // Match any tag
          matches = tags.some(t => search(String(t)) !== null);
        }
        break;
      case "status":
        // Status uses exact match (lowercase comparison)
        matches = (doc?.status || "none").toLowerCase() === value.toLowerCase();
        break;
      case "id":
        matches = doc?.id ? search(doc.id) !== null : false;
        break;
      case "section":
        // Section search - check if any section title matches (sections is Map<string, string>)
        if (doc?.sections) {
          for (const title of doc.sections.keys()) {
            if (search(title) !== null) {
              matches = true;
              break;
            }
          }
        }
        break;
      case "line":
        // Line search - would need content, skip for now (use in full search)
        matches = false;
        break;
      case "text":
      default:
        // Search in path, name, and id using native search
        matches = search(file.path) !== null ||
                  search(file.name) !== null ||
                  (doc?.id ? search(doc.id) !== null : false);
        break;
    }

    return exclude ? !matches : matches;
  }

  private getCurrentFile(): TFile | null {
    const queue = this.getQueue();
    if (queue.length === 0) return null;
    if (this.currentIndex >= queue.length) this.currentIndex = queue.length - 1;
    if (this.currentIndex < 0) this.currentIndex = 0;
    return queue[this.currentIndex];
  }

  private syncWithActiveFile(): void {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile || !this.isTrackedFile(activeFile.path)) return;

    const queue = this.getQueue();
    const index = queue.findIndex(f => f.path === activeFile.path);

    if (index !== -1 && index !== this.currentIndex) {
      this.currentIndex = index;
      this.render();
    }
  }

  private render(): void {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    if (this.store.isLoading()) {
      el.createDiv({ text: "Loading...", cls: "pane-empty" });
      return;
    }

    const docs = this.store.getState().documents.filter(d => this.isTrackedFile(d.file.path));
    const total = docs.length;
    const approved = docs.filter(d => d.status === "approved").length;
    const review = docs.filter(d => d.status === "review").length;
    const rejected = docs.filter(d => d.status === "rejected").length;
    const noStatus = docs.filter(d => !d.status).length;
    const queue = this.getQueue();
    const file = this.getCurrentFile();
    const doc = file ? this.store.getDocument(file.path) : null;

    // Actions (very top)
    const actions = el.createDiv({ cls: "docs-actions" });
    const actionsRow = actions.createDiv({ cls: "docs-actions-row" });

    // First button (go to start)
    const firstBtn = actionsRow.createEl("button", { cls: "docs-btn docs-btn-nav", attr: { title: "Ir para o primeiro" } });
    setIcon(firstBtn, "chevrons-left");
    firstBtn.disabled = this.currentIndex === 0;
    firstBtn.onclick = () => this.goTo(0);

    // Left arrow
    const prevBtn = actionsRow.createEl("button", { cls: "docs-btn docs-btn-nav", attr: { title: "Anterior" } });
    setIcon(prevBtn, "arrow-left");
    prevBtn.disabled = this.currentIndex === 0;
    prevBtn.onclick = () => this.navigate(-1);

    // Center group: reject, review, approve
    const centerGroup = actionsRow.createDiv({ cls: "docs-btn-center" });

    const rejectBtn = centerGroup.createEl("button", { cls: "docs-btn docs-btn-reject", attr: { title: "Rejeitar" } });
    setIcon(rejectBtn, "x");
    rejectBtn.disabled = !file || doc?.status === "rejected";
    rejectBtn.onclick = () => file && this.reject(file);

    const reviewBtn = centerGroup.createEl("button", { cls: "docs-btn docs-btn-review", attr: { title: "Marcar para revisão" } });
    setIcon(reviewBtn, "circle");
    reviewBtn.disabled = !file || doc?.status === "review";
    reviewBtn.onclick = () => file && this.setReview(file);

    const approveBtn = centerGroup.createEl("button", { cls: "docs-btn docs-btn-approve", attr: { title: "Aprovar" } });
    setIcon(approveBtn, "check");
    approveBtn.disabled = !file || doc?.status === "approved";
    approveBtn.onclick = () => file && this.approve(file);

    // Right arrow
    const nextBtn = actionsRow.createEl("button", { cls: "docs-btn docs-btn-nav", attr: { title: "Próximo" } });
    setIcon(nextBtn, "arrow-right");
    nextBtn.disabled = this.currentIndex >= queue.length - 1;
    nextBtn.onclick = () => this.navigate(1);

    // Last button (go to end)
    const lastBtn = actionsRow.createEl("button", { cls: "docs-btn docs-btn-nav", attr: { title: "Ir para o último" } });
    setIcon(lastBtn, "chevrons-right");
    lastBtn.disabled = this.currentIndex >= queue.length - 1;
    lastBtn.onclick = () => this.goTo(queue.length - 1);

    // Filter input with autocomplete (like Graph View)
    const filterContainer = el.createDiv({ cls: "docs-filter-container" });
    const filterInput = filterContainer.createEl("input", {
      cls: "docs-filter-input",
      attr: {
        type: "text",
        placeholder: "path: file: tag: status: -exclude OR",
        value: this.filterQuery,
        spellcheck: "false"
      }
    });

    // Attach FilterSuggest for autocomplete
    new FilterSuggest(
      this.app,
      filterInput,
      () => this.store.getState().documents.filter(d => this.isTrackedFile(d.file.path)),
      (value) => {
        this.filterQuery = value;
        this.currentIndex = 0;
        this.render();
      }
    );

    // Clear button (only show if there's a filter)
    if (this.filterQuery) {
      const clearBtn = filterContainer.createEl("button", { cls: "docs-filter-clear", attr: { title: "Limpar filtro" } });
      setIcon(clearBtn, "x");
      clearBtn.onclick = (e) => {
        e.stopPropagation();
        this.filterQuery = "";
        this.currentIndex = 0;
        this.render();
      };
    }

    // Debounced filter update (for manual typing)
    let debounceTimer: NodeJS.Timeout;
    filterInput.oninput = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        this.filterQuery = filterInput.value;
        this.currentIndex = 0;
        this.render();
      }, 400);
    };

    // Show filtered count if filter is active
    if (this.filterQuery) {
      const totalUnfiltered = this.store.getReviewQueue().filter(f => this.isTrackedFile(f.path)).length;
      filterContainer.createDiv({
        text: `${queue.length} / ${totalUnfiltered}`,
        cls: "docs-filter-count"
      });
    }

    // Header with progress stats
    const header = el.createDiv({ cls: "nav-header" });
    const statsRow = header.createDiv({ cls: "docs-stats-row" });

    // Helper to calculate percentage
    const pct = (n: number) => total > 0 ? Math.round((n / total) * 100) : 0;

    // Approved stat
    const approvedStat = statsRow.createDiv({ cls: "docs-stat", attr: { title: "Aprovados" } });
    approvedStat.createDiv({ cls: "docs-stat-dot docs-dot-approved" });
    approvedStat.createSpan({ text: `${approved}`, cls: "docs-stat-num" });
    approvedStat.createSpan({ text: `${pct(approved)}%`, cls: "docs-stat-pct" });

    // Review stat
    const reviewStat = statsRow.createDiv({ cls: "docs-stat", attr: { title: "Em revisão" } });
    reviewStat.createDiv({ cls: "docs-stat-dot docs-dot-review" });
    reviewStat.createSpan({ text: `${review}`, cls: "docs-stat-num" });
    reviewStat.createSpan({ text: `${pct(review)}%`, cls: "docs-stat-pct" });

    // Rejected stat
    const rejectedStat = statsRow.createDiv({ cls: "docs-stat", attr: { title: "Rejeitados" } });
    rejectedStat.createDiv({ cls: "docs-stat-dot docs-dot-rejected" });
    rejectedStat.createSpan({ text: `${rejected}`, cls: "docs-stat-num" });
    rejectedStat.createSpan({ text: `${pct(rejected)}%`, cls: "docs-stat-pct" });

    // No status stat (gray)
    if (noStatus > 0) {
      const noStatusStat = statsRow.createDiv({ cls: "docs-stat", attr: { title: "Sem status" } });
      noStatusStat.createDiv({ cls: "docs-stat-dot docs-dot-none" });
      noStatusStat.createSpan({ text: `${noStatus}`, cls: "docs-stat-num" });
      noStatusStat.createSpan({ text: `${pct(noStatus)}%`, cls: "docs-stat-pct" });
    }

    // Total
    const totalStat = statsRow.createDiv({ cls: "docs-stat docs-stat-total", attr: { title: "Total de arquivos" } });
    totalStat.createSpan({ text: `${total}`, cls: "docs-stat-num docs-stat-total-num" });

    // Problems button row
    const headerInfo = header.createDiv({ cls: "nav-buttons-container" });

    // Problems button
    const allIssues = this.store.getState().issues;
    if (allIssues.length > 0) {
      const problemsBtn = headerInfo.createEl("button", {
        text: `⚠ ${allIssues.length}`,
        cls: "docs-problems-btn"
      });
      problemsBtn.onclick = () => {
        (this.app as any).commands.executeCommandById("docs-toolkit:open-issues-panel");
      };
    }

    // Dots navigation (configurable, centered on current)
    const dotsContainer = header.createDiv({ cls: "docs-dots" });
    const maxDots = this.plugin.settings.maxDotsCount;
    const halfWindow = Math.floor(maxDots / 2);

    let start = 0;
    let end = queue.length;

    if (queue.length > maxDots) {
      start = Math.max(0, this.currentIndex - halfWindow);
      end = Math.min(queue.length, start + maxDots);
      if (end - start < maxDots) {
        start = Math.max(0, end - maxDots);
      }
    }

    for (let i = start; i < end; i++) {
      const f = queue[i];
      const d = this.store.getDocument(f.path);
      const status = d?.status || "none";
      const isCurrent = i === this.currentIndex;
      const isAdjacent = i === this.currentIndex - 1 || i === this.currentIndex + 1;

      const dot = dotsContainer.createDiv({
        cls: `docs-dot docs-dot-${status}${isCurrent ? " docs-dot-current" : ""}${isAdjacent ? " docs-dot-adjacent" : ""}`
      });

      dot.onclick = () => {
        this.currentIndex = i;
        this.openCurrentFile();
        this.render();
      };
    }

    if (queue.length === 0) {
      const empty = el.createDiv({ cls: "pane-empty" });
      empty.createDiv({ text: "All done!", cls: "docs-done-text" });
      return;
    }

    if (!file) return;

    const issues = this.store.getIssuesForFile(file.path);

    // File info
    const fileSection = el.createDiv({ cls: "docs-file-section" });

    // Counter
    fileSection.createDiv({
      text: `${this.currentIndex + 1} of ${queue.length}`,
      cls: "docs-counter"
    });

    // File name
    const nameRow = fileSection.createDiv({ cls: "docs-file-name" });
    nameRow.createSpan({ text: doc?.id || file.basename });

    // Path
    const pathParts = file.path.split("/");
    if (pathParts.length > 1) {
      fileSection.createDiv({
        text: pathParts.slice(0, -1).join("/"),
        cls: "docs-file-path"
      });
    }

    // Status
    if (doc?.hasFrontmatter) {
      const status = doc.status;
      fileSection.createDiv({
        text: status.toUpperCase(),
        cls: `docs-status docs-status-${status}`
      });
    } else {
      const warning = fileSection.createDiv({ cls: "docs-warning" });
      warning.createSpan({ text: "No frontmatter" });
      const initBtn = warning.createEl("button", { text: "Init", cls: "docs-init-btn" });
      initBtn.onclick = () => this.initYaml(file);
    }

    // Issues
    if (issues.length > 0) {
      const issuesSection = el.createDiv({ cls: "docs-issues-section" });
      issuesSection.createDiv({
        text: `${issues.length} issue${issues.length > 1 ? "s" : ""}`,
        cls: "docs-issues-title"
      });

      const list = issuesSection.createDiv({ cls: "docs-issues-list" });
      for (const issue of issues.slice(0, 8)) {
        const row = list.createDiv({ cls: "docs-issue-row" });

        const icon = issue.severity === "error" ? "×" : "!";
        row.createSpan({ text: icon, cls: `docs-issue-icon docs-${issue.severity}` });

        const msg = this.i18n.t(issue.messageKey, issue.messageParams as Record<string, unknown>);
        row.createSpan({ text: msg, cls: "docs-issue-msg" });

        if (issue.line) {
          row.createSpan({ text: `:${issue.line}`, cls: "docs-issue-line" });
        }

        row.onclick = () => this.navigateToIssue(issue);
      }

      if (issues.length > 8) {
        list.createDiv({ text: `+${issues.length - 8} more`, cls: "docs-more" });
      }
    }

    // Claude prompt box
    const promptText = this.generateClaudePrompt(file, doc, issues);
    const promptSection = el.createDiv({ cls: "docs-prompt-section" });

    const promptHeader = promptSection.createDiv({ cls: "docs-prompt-header" });
    const toggleBtn = promptHeader.createEl("button", { cls: "docs-prompt-toggle" });
    setIcon(toggleBtn, "chevron-right");
    promptHeader.createSpan({ text: "Claude Prompt", cls: "docs-prompt-title" });

    const copyBtn = promptHeader.createEl("button", { cls: "docs-prompt-copy" });
    setIcon(copyBtn, "copy");
    copyBtn.onclick = (e) => {
      e.stopPropagation();
      navigator.clipboard.writeText(promptText);
      setIcon(copyBtn, "check");
      setTimeout(() => setIcon(copyBtn, "copy"), 1500);
    };

    const promptContent = promptSection.createDiv({ cls: "docs-prompt-content hidden" });
    promptContent.createEl("pre", { text: promptText, cls: "docs-prompt-text" });

    promptHeader.onclick = () => {
      const isHidden = promptContent.hasClass("hidden");
      promptContent.toggleClass("hidden", !isHidden);
      setIcon(toggleBtn, isHidden ? "chevron-down" : "chevron-right");
    };
  }

  private async navigate(delta: number): Promise<void> {
    const queue = this.getQueue();
    const newIndex = this.currentIndex + delta;
    if (newIndex < 0 || newIndex >= queue.length) return;
    this.currentIndex = newIndex;
    await this.openCurrentFile();
    this.render();
  }

  private async goTo(index: number): Promise<void> {
    const queue = this.getQueue();
    if (index < 0 || index >= queue.length) return;
    this.currentIndex = index;
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

  private async navigateToIssue(issue: Issue): Promise<void> {
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(issue.file);
    if (issue.line) {
      const editor = (leaf.view as any)?.editor;
      if (editor) {
        editor.setCursor({ line: issue.line - 1, ch: issue.column || 0 });
        editor.scrollIntoView({ from: { line: issue.line - 1, ch: 0 }, to: { line: issue.line - 1, ch: 0 } }, true);
      }
    }
  }

  private onKey(e: KeyboardEvent): void {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); this.navigate(-1); }
    if (e.key === "ArrowRight") { e.preventDefault(); this.navigate(1); }
  }

  private generateClaudePrompt(file: TFile, doc: Document | null | undefined, issues: Issue[]): string {
    const lines: string[] = [];

    // Get frontmatter from Obsidian's metadataCache (official API for Properties)
    const cache = this.app.metadataCache.getFileCache(file);
    const frontmatter = cache?.frontmatter;

    // Debug: log what metadataCache returns
    console.log("[Claude Prompt] file:", file.path);
    console.log("[Claude Prompt] cache:", cache);
    console.log("[Claude Prompt] frontmatter:", frontmatter);
    console.log("[Claude Prompt] description:", frontmatter?.description);

    // File path
    lines.push(`@${file.path.replace(/\//g, "\\")}`);
    lines.push("");

    // Status info (from metadataCache)
    const status = frontmatter?.status || doc?.status || "sem status";
    lines.push(`**Status:** ${String(status).toUpperCase()}`);

    // Description - fallback: metadataCache first, then doc.frontmatter
    const description = frontmatter?.description || doc?.frontmatter?.description;
    if (description && String(description).trim()) {
      // Preserve the full description including line breaks
      lines.push(`**Descrição:** ${String(description)}`);
    } else {
      lines.push(`**Descrição:** (não informada)`);
    }

    if (frontmatter?.rejection_reason) {
      lines.push(`**Motivo da Rejeição:** ${frontmatter.rejection_reason}`);
    }
    lines.push("");

    // Document info
    lines.push("## Informações do Documento");
    lines.push(`- **Arquivo:** ${file.basename}`);
    lines.push(`- **Path:** ${file.path}`);
    if (doc?.frontmatter?.type) lines.push(`- **Tipo:** ${doc.frontmatter.type}`);
    if (doc?.frontmatter?.id) lines.push(`- **ID:** ${doc.frontmatter.id}`);
    if (doc?.frontmatter?.modules) {
      const modules = Array.isArray(doc.frontmatter.modules)
        ? doc.frontmatter.modules.join(", ")
        : doc.frontmatter.modules;
      lines.push(`- **Módulos:** ${modules}`);
    }
    if (doc?.frontmatter?.updated) lines.push(`- **Atualizado:** ${doc.frontmatter.updated}`);
    if (!doc?.hasFrontmatter) lines.push(`- **Aviso:** Documento sem frontmatter YAML`);
    lines.push("");

    // Issues/Errors
    if (issues.length > 0) {
      lines.push("## Problemas Encontrados");
      for (const issue of issues) {
        const severity = issue.severity === "error" ? "ERROR" : "WARNING";
        const msg = this.i18n.t(issue.messageKey, issue.messageParams as Record<string, unknown>);
        const line = issue.line ? `:${issue.line}` : "";
        lines.push(`- [${severity}]${line} ${msg}`);
      }
    } else {
      lines.push("## Problemas Encontrados");
      lines.push("Nenhum problema detectado.");
    }
    lines.push("");

    // Instructions
    lines.push("---");
    lines.push("Por favor, analise este arquivo e ajude a corrigir os problemas listados acima.");

    return lines.join("\n");
  }
}

class RejectModal extends Modal {
  private onSubmit: (reason: string) => void;
  private i18n: I18nService;
  private reason = "";

  constructor(app: App, i18n: I18nService, onSubmit: (reason: string) => void) {
    super(app);
    this.i18n = i18n;
    this.onSubmit = onSubmit;
  }

  onOpen(): void {
    const { contentEl } = this;
    contentEl.createEl("h3", { text: "Reject" });

    const textArea = new TextAreaComponent(contentEl);
    textArea.setPlaceholder("Reason...");
    textArea.inputEl.style.width = "100%";
    textArea.inputEl.style.height = "80px";
    textArea.onChange((v) => this.reason = v);

    setTimeout(() => textArea.inputEl.focus(), 10);

    const footer = contentEl.createDiv({ cls: "modal-button-container" });
    const submitBtn = footer.createEl("button", { text: "Reject", cls: "mod-warning" });
    submitBtn.onclick = () => {
      if (this.reason.trim()) {
        this.onSubmit(this.reason.trim());
        this.close();
      }
    };

    textArea.inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        submitBtn.click();
      }
    });
  }

  onClose(): void { this.contentEl.empty(); }
}
