import { App, Events, TFile, TFolder } from "obsidian";
import { Document } from "../models/Document";
import { Issue, IssueSummary, calculateIssueSummary } from "../models/Issue";
import { Status } from "../models/types";
import { Validator } from "../validators/Validator";

// Import all validators
import { BrokenLinksValidator } from "../validators/BrokenLinksValidator";
import { FrontmatterValidator } from "../validators/FrontmatterValidator";
import { OrphansValidator } from "../validators/OrphansValidator";
import { StructureValidator } from "../validators/StructureValidator";
import { TitleValidator } from "../validators/TitleValidator";
import { StaleValidator } from "../validators/StaleValidator";
import { EmptyFoldersValidator } from "../validators/EmptyFoldersValidator";
import { NamingValidator } from "../validators/NamingValidator";

export interface StoreState {
  documents: Document[];
  issues: Issue[];
  summary: IssueSummary;
  reviewQueue: TFile[];
}

/**
 * Central event-driven store for document state.
 * Emits 'state-changed' event on every mutation.
 */
export class DocumentStore extends Events {
  private app: App;
  private documents: Map<string, Document> = new Map();
  private issues: Map<string, Issue[]> = new Map();
  private validators: Validator[] = [];
  private enabledValidators: Set<string> = new Set();
  private loading = false;

  constructor(app: App) {
    super();
    this.app = app;
    this.registerValidators();
  }

  private registerValidators(): void {
    this.validators = [
      new BrokenLinksValidator(),
      new FrontmatterValidator(),
      new OrphansValidator(),
      new StructureValidator(),
      new TitleValidator(),
      new StaleValidator(),
      new EmptyFoldersValidator(),
      new NamingValidator()
    ];
    // Enable all by default
    this.validators.forEach(v => this.enabledValidators.add(v.id));
  }

  // --- Validator Management ---

  getValidators(): Validator[] {
    return this.validators;
  }

  setValidatorEnabled(id: string, enabled: boolean): void {
    if (enabled) {
      this.enabledValidators.add(id);
    } else {
      this.enabledValidators.delete(id);
    }
  }

  private getEnabledValidators(): Validator[] {
    return this.validators.filter(v => this.enabledValidators.has(v.id));
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
      .filter(d => d.file.name !== "README.md" && d.status === Status.REVIEW)
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

    const files = this.getCARFFiles();
    this.documents.clear();
    this.issues.clear();

    // Parse all documents
    for (const file of files) {
      const doc = await this.parseDocument(file);
      this.documents.set(file.path, doc);
    }

    // Run local validators
    const docs = Array.from(this.documents.values());
    for (const doc of docs) {
      const fileIssues: Issue[] = [];
      for (const validator of this.getEnabledValidators()) {
        if (!validator.isGlobal && validator.validateFile) {
          const vi = await validator.validateFile(doc, this.app);
          fileIssues.push(...vi);
        }
      }
      this.issues.set(doc.file.path, fileIssues);
    }

    // Run global validators
    for (const validator of this.getEnabledValidators()) {
      if (validator.isGlobal && validator.validateAll) {
        const globalIssues = await validator.validateAll(docs, this.app);
        // Distribute global issues to their files
        for (const issue of globalIssues) {
          const existing = this.issues.get(issue.file.path) || [];
          existing.push(issue);
          this.issues.set(issue.file.path, existing);
        }
      }
    }

    this.loading = false;
    this.trigger("state-changed");
  }

  /**
   * Update a single document. Emits 'state-changed'.
   */
  async updateDocument(file: TFile): Promise<void> {
    if (!file.name.endsWith(".md")) return;
    if (!Document.isInCARFPath(file.path)) return;

    const doc = await this.parseDocument(file);
    this.documents.set(file.path, doc);

    // Re-validate this file
    const fileIssues: Issue[] = [];
    for (const validator of this.getEnabledValidators()) {
      if (!validator.isGlobal && validator.validateFile) {
        const vi = await validator.validateFile(doc, this.app);
        fileIssues.push(...vi);
      }
    }
    this.issues.set(file.path, fileIssues);

    this.trigger("state-changed");
  }

  /**
   * Remove a document from store. Emits 'state-changed'.
   */
  removeDocument(path: string): void {
    this.documents.delete(path);
    this.issues.delete(path);
    this.trigger("state-changed");
  }

  /**
   * Set status for a document. Updates frontmatter and emits 'state-changed'.
   */
  async setStatus(file: TFile, status: Status): Promise<void> {
    const content = await this.app.vault.read(file);
    const newContent = this.updateStatusInContent(content, status);
    await this.app.vault.modify(file, newContent);
    // updateDocument will be called by vault 'modify' event
  }

  // --- Internal Helpers ---

  private getCARFFiles(): TFile[] {
    const ignorePaths = [".obsidian", ".git", "node_modules", ".plugins", ".scripts"];
    return this.app.vault.getMarkdownFiles().filter(file => {
      return !ignorePaths.some(p => file.path.startsWith(p + "/") || file.path.startsWith(p));
    });
  }

  private async parseDocument(file: TFile): Promise<Document> {
    const content = await this.app.vault.read(file);
    const frontmatter = this.parseFrontmatter(content);
    const bodyContent = this.getBodyContent(content);
    const sections = this.parseSections(bodyContent);
    const links = this.parseLinks(bodyContent);
    const title = this.parseTitle(bodyContent);

    return new Document(file, frontmatter, content, sections, links, title);
  }

  private parseFrontmatter(content: string): import("../models/types").CARFFrontmatter | null {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;

    try {
      const { parseYaml } = require("obsidian");
      const yaml = parseYaml(match[1]);
      if (!yaml || !yaml.id || !yaml.type || !yaml.status) return null;

      const { DocType, Status: S, VALID_MODULES } = require("../models/types");
      const type = yaml.type.toUpperCase();
      if (!Object.values(DocType).includes(type)) return null;

      const status = yaml.status.toLowerCase();
      if (!Object.values(S).includes(status)) return null;

      let modules: import("../models/types").Module[] = [];
      if (Array.isArray(yaml.modules)) {
        modules = yaml.modules
          .map((m: string) => m.toUpperCase())
          .filter((m: string) => VALID_MODULES.includes(m)) as import("../models/types").Module[];
      }

      return {
        id: yaml.id,
        type,
        modules,
        epic: yaml.epic || undefined,
        status,
        created: yaml.created || this.formatDate(new Date()),
        updated: yaml.updated || this.formatDate(new Date())
      };
    } catch {
      return null;
    }
  }

  private getBodyContent(content: string): string {
    return content.replace(/^---\n[\s\S]*?\n---\n*/, "");
  }

  private parseSections(content: string): Map<string, string> {
    const sections = new Map<string, string>();
    const lines = content.split("\n");
    let currentSection = "";
    let currentContent: string[] = [];

    for (const line of lines) {
      const headerMatch = line.match(/^#{2,3}\s+(.+)$/);
      if (headerMatch) {
        if (currentSection) {
          sections.set(currentSection, currentContent.join("\n").trim());
        }
        currentSection = headerMatch[1].trim();
        currentContent = [];
      } else if (currentSection) {
        currentContent.push(line);
      }
    }

    if (currentSection) {
      sections.set(currentSection, currentContent.join("\n").trim());
    }

    return sections;
  }

  private parseLinks(content: string): import("../models/Document").DocumentLink[] {
    const links: import("../models/Document").DocumentLink[] = [];
    const lines = content.split("\n");

    for (let lineNum = 0; lineNum < lines.length; lineNum++) {
      const line = lines[lineNum];

      // Wiki links
      const wikiLinkRegex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
      let match;
      while ((match = wikiLinkRegex.exec(line)) !== null) {
        links.push({
          target: match[1],
          line: lineNum + 1,
          column: match.index,
          type: "wiki",
          resolved: false
        });
      }

      // Markdown links
      const mdLinkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
      while ((match = mdLinkRegex.exec(line)) !== null) {
        const target = match[2];
        if (!target.startsWith("http://") && !target.startsWith("https://")) {
          links.push({
            target,
            line: lineNum + 1,
            column: match.index,
            type: "markdown",
            resolved: false
          });
        }
      }
    }

    return links;
  }

  private parseTitle(content: string): string | null {
    const match = content.match(/^#\s+(.+)$/m);
    return match ? match[1].trim() : null;
  }

  private formatDate(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  private updateStatusInContent(content: string, status: Status): string {
    const today = this.formatDate(new Date());

    // Update status in frontmatter
    let newContent = content.replace(
      /^(---\n[\s\S]*?status:\s*)\w+/m,
      `$1${status}`
    );

    // Update 'updated' field
    newContent = newContent.replace(
      /^(---\n[\s\S]*?updated:\s*)\S+/m,
      `$1${today}`
    );

    return newContent;
  }
}
