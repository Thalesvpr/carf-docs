import { App, Events, TFile, TFolder, parseYaml } from "obsidian";
import { Document, DocumentLink, Frontmatter } from "../core/Document";
import { Issue, IssueSummary, calculateIssueSummary } from "../core/Issue";
import { DocsLinterConfig } from "../config/ConfigSchema";
import { ValidatorRegistry } from "../validators/ValidatorRegistry";
import { ValidationService } from "../services/ValidationService";
import { DocumentParser } from "../services/DocumentParser";
import { TemplateService } from "../services/TemplateService";
import { I18nService } from "../i18n/I18nService";

export interface StoreState {
  documents: Document[];
  issues: Issue[];
  summary: IssueSummary;
  reviewQueue: TFile[];
}

/**
 * Central event-driven store for document state.
 * v2.0 - Fully configurable via .docslint.yaml
 * Emits 'state-changed' event on every mutation.
 */
export class DocumentStore extends Events {
  private app: App;
  private config: DocsLinterConfig;
  private registry: ValidatorRegistry;
  private templateService: TemplateService;
  private i18n: I18nService;
  private documentParser: DocumentParser;
  private validationService: ValidationService;

  private documents: Map<string, Document> = new Map();
  private issues: Map<string, Issue[]> = new Map();
  private loading = false;

  constructor(
    app: App,
    config: DocsLinterConfig,
    registry: ValidatorRegistry,
    templateService: TemplateService,
    i18n: I18nService
  ) {
    super();
    this.app = app;
    this.config = config;
    this.registry = registry;
    this.templateService = templateService;
    this.i18n = i18n;
    this.documentParser = new DocumentParser(app);
    this.validationService = new ValidationService(
      app,
      registry,
      templateService,
      i18n
    );
  }

  /**
   * Update configuration (called when .docslint.yaml changes)
   */
  updateConfig(config: DocsLinterConfig): void {
    this.config = config;
  }

  // --- State Access ---

  getState(): StoreState {
    const docs = Array.from(this.documents.values());
    const allIssues = Array.from(this.issues.values()).flat();
    allIssues.sort(Issue.compare);

    return {
      documents: docs,
      issues: allIssues,
      summary: calculateIssueSummary(allIssues),
      reviewQueue: this.getReviewQueue()
    };
  }

  getReviewQueue(): TFile[] {
    return Array.from(this.documents.values())
      .sort((a, b) => a.file.path.localeCompare(b.file.path))
      .map(d => d.file);
  }

  getDocument(path: string): Document | undefined {
    return this.documents.get(path);
  }

  getIssuesForFile(path: string): Issue[] {
    return this.issues.get(path) || [];
  }

  isLoading(): boolean {
    return this.loading;
  }

  // --- State Mutations ---

  /**
   * Load all documents from vault. Emits 'state-changed' when done.
   */
  async loadAll(): Promise<void> {
    this.loading = true;
    this.trigger("state-changed");

    const files = this.getIncludedFiles();
    this.documents.clear();
    this.issues.clear();

    // Initialize template service
    await this.templateService.initialize();

    // Parse all documents
    for (const file of files) {
      const doc = await this.documentParser.parse(file);
      this.documents.set(file.path, doc);
    }

    // Run validation on all documents
    const docs = Array.from(this.documents.values());
    const result = await this.validationService.validateAll(docs, this.config);

    // Store issues
    for (const [path, docResult] of result.documentResults) {
      this.issues.set(path, docResult.issues);
    }

    this.loading = false;
    this.trigger("state-changed");
  }

  /**
   * Update a single document. Emits 'state-changed'.
   */
  async updateDocument(file: TFile): Promise<void> {
    if (!file.name.endsWith(".md")) return;
    if (!this.isIncludedFile(file.path)) return;

    const doc = await this.documentParser.parse(file);
    this.documents.set(file.path, doc);

    // Re-validate this file
    const allDocs = Array.from(this.documents.values());
    const docIssues = await this.validationService.validateDocument(
      doc,
      this.config,
      allDocs
    );
    this.issues.set(file.path, docIssues);

    // Update template cache if this is a template
    if (this.templateService.isTemplate(doc)) {
      await this.templateService.refreshTemplate(file);
    }

    this.trigger("state-changed");
  }

  /**
   * Remove a document from store. Emits 'state-changed'.
   */
  removeDocument(path: string): void {
    this.documents.delete(path);
    this.issues.delete(path);
    this.templateService.removeTemplate(path);
    this.trigger("state-changed");
  }

  /**
   * Set status for a document. Updates frontmatter and emits 'state-changed'.
   */
  async setStatus(file: TFile, status: string, description?: string): Promise<void> {
    const content = await this.app.vault.read(file);
    const newContent = this.updateStatusInContent(content, status, description);
    await this.app.vault.modify(file, newContent);
    await this.updateDocument(file);
  }

  // --- Internal Helpers ---

  /**
   * Get files that match include patterns and don't match exclude patterns
   */
  private getIncludedFiles(): TFile[] {
    return this.app.vault.getMarkdownFiles().filter(file =>
      this.isIncludedFile(file.path)
    );
  }

  /**
   * Check if a file path should be included
   * Simple logic: if it's not excluded, include it
   */
  private isIncludedFile(path: string): boolean {
    // Check exclude patterns - if matched, reject
    for (const pattern of this.config.paths.exclude) {
      if (this.matchGlob(path, pattern)) {
        return false;
      }
    }

    // Accept all .md files that are not excluded
    return true;
  }

  /**
   * Simple glob matching
   */
  private matchGlob(path: string, pattern: string): boolean {
    const regex = pattern
      .replace(/\*\*/g, ".*")
      .replace(/\*/g, "[^/]*")
      .replace(/\?/g, ".");

    return new RegExp(`^${regex}$`).test(path);
  }

  /**
   * Format date as YYYY-MM-DD
   */
  private formatDate(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  /**
   * Update status in frontmatter content
   */
  private updateStatusInContent(
    content: string,
    status: string,
    description?: string
  ): string {
    const today = this.formatDate(new Date());

    // Update status in frontmatter
    let newContent = content.replace(
      /^(---\r?\n[\s\S]*?status:\s*)\w+/m,
      `$1${status}`
    );

    // Update 'updated' field
    newContent = newContent.replace(
      /^(---\r?\n[\s\S]*?updated:\s*)\S+/m,
      `$1${today}`
    );

    // Handle description field
    if (description) {
      if (/^---\r?\n[\s\S]*?description:/m.test(newContent)) {
        newContent = newContent.replace(
          /^(---\r?\n[\s\S]*?description:\s*).*/m,
          `$1"${description.replace(/"/g, '\\"')}"`
        );
      } else {
        newContent = newContent.replace(
          /^(---\r?\n[\s\S]*?)(---)/m,
          `$1description: "${description.replace(/"/g, '\\"')}"\n$2`
        );
      }
    } else {
      // Remove description if exists and no new description
      newContent = newContent.replace(
        /^(---\r?\n[\s\S]*?)description:.*\r?\n/m,
        `$1`
      );
    }

    return newContent;
  }
}
