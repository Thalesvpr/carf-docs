import { ItemView, WorkspaceLeaf, TFile, Modal, App, TextAreaComponent, Events, setIcon } from "obsidian";
import { Document } from "../core/Document";
import { Issue } from "../core/Issue";
import { I18nService } from "../i18n/I18nService";
import { DocsLinterConfig } from "../config/ConfigSchema";

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

export class CurationPanelView extends ItemView {
  private store: DocumentStore;
  private metadataService: MetadataService;
  private i18n: I18nService;
  private config: DocsLinterConfig;
  private currentIndex = 0;

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
      const regex = pattern.replace(/\*\*/g, ".*").replace(/\*/g, "[^/]*");
      if (new RegExp(`^${regex}`).test(path)) return false;
    }
    return true;
  }

  private getQueue(): TFile[] {
    return this.store.getReviewQueue().filter(f => this.isTrackedFile(f.path));
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
    const approved = docs.filter(d => d.status === "approved").length;
    const total = docs.length;
    const queue = this.getQueue();
    const file = this.getCurrentFile();
    const doc = file ? this.store.getDocument(file.path) : null;

    // Actions (very top)
    const actions = el.createDiv({ cls: "docs-actions" });
    const actionsRow = actions.createDiv({ cls: "docs-actions-row" });

    // Left arrow
    const prevBtn = actionsRow.createEl("button", { cls: "docs-btn docs-btn-nav" });
    setIcon(prevBtn, "arrow-left");
    prevBtn.disabled = this.currentIndex === 0;
    prevBtn.onclick = () => this.navigate(-1);

    // Center group: reject, review, approve
    const centerGroup = actionsRow.createDiv({ cls: "docs-btn-center" });

    const rejectBtn = centerGroup.createEl("button", { cls: "docs-btn docs-btn-reject" });
    setIcon(rejectBtn, "x");
    rejectBtn.disabled = !file || doc?.status === "rejected";
    rejectBtn.onclick = () => file && this.reject(file);

    const reviewBtn = centerGroup.createEl("button", { cls: "docs-btn docs-btn-review" });
    setIcon(reviewBtn, "circle");
    reviewBtn.disabled = !file || doc?.status === "review";
    reviewBtn.onclick = () => file && this.setReview(file);

    const approveBtn = centerGroup.createEl("button", { cls: "docs-btn docs-btn-approve" });
    setIcon(approveBtn, "check");
    approveBtn.disabled = !file || doc?.status === "approved";
    approveBtn.onclick = () => file && this.approve(file);

    // Right arrow
    const nextBtn = actionsRow.createEl("button", { cls: "docs-btn docs-btn-nav" });
    setIcon(nextBtn, "arrow-right");
    nextBtn.disabled = this.currentIndex >= queue.length - 1;
    nextBtn.onclick = () => this.navigate(1);

    // Header with progress
    const header = el.createDiv({ cls: "nav-header" });
    const headerInfo = header.createDiv({ cls: "nav-buttons-container" });
    headerInfo.createSpan({
      text: `${approved}/${total}`,
      cls: "docs-progress-text"
    });

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

    // Dots navigation (max 51, centered on current)
    const dotsContainer = header.createDiv({ cls: "docs-dots" });
    const maxDots = 51;
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
      const status = d?.status || "review";
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

    // File path
    lines.push(`@${file.path.replace(/\//g, "\\")}`);
    lines.push("");

    // Status info
    if (doc) {
      lines.push(`**Status:** ${doc.status.toUpperCase()}`);
      if (doc.status === "rejected" && doc.frontmatter?.rejection_reason) {
        lines.push(`**Motivo da Rejeição:** ${doc.frontmatter.rejection_reason}`);
      }
      lines.push("");
    }

    // Document info
    if (doc) {
      lines.push("## Informações do Documento");
      if (doc.frontmatter?.type) lines.push(`- **Tipo:** ${doc.frontmatter.type}`);
      if (doc.frontmatter?.id) lines.push(`- **ID:** ${doc.frontmatter.id}`);
      if (doc.frontmatter?.modules) {
        const modules = Array.isArray(doc.frontmatter.modules)
          ? doc.frontmatter.modules.join(", ")
          : doc.frontmatter.modules;
        lines.push(`- **Módulos:** ${modules}`);
      }
      if (doc.frontmatter?.updated) lines.push(`- **Atualizado:** ${doc.frontmatter.updated}`);
      lines.push("");
    }

    // Issues/Errors
    if (issues.length > 0) {
      lines.push("## Problemas Encontrados");
      for (const issue of issues) {
        const severity = issue.severity === "error" ? "ERROR" : "WARNING";
        const msg = this.i18n.t(issue.messageKey, issue.messageParams as Record<string, unknown>);
        const line = issue.line ? `:${issue.line}` : "";
        lines.push(`- [${severity}]${line} ${msg}`);
      }
      lines.push("");
    }

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
