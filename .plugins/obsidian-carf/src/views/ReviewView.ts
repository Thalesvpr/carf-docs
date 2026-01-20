import { ItemView, WorkspaceLeaf, TFile, MarkdownRenderer } from "obsidian";
import { MetadataService } from "../services/MetadataService";
import { ValidationService } from "../services/ValidationService";
import { Document } from "../models/Document";
import { Status } from "../models/types";
import { Issue } from "../models/Issue";

export const REVIEW_VIEW_TYPE = "carf-review";

export class ReviewView extends ItemView {
  private metadataService: MetadataService;
  private validationService: ValidationService;
  private queue: TFile[] = [];
  private index: number = 0;
  private doc: Document | null = null;
  private issues: Issue[] = [];

  constructor(
    leaf: WorkspaceLeaf,
    metadataService: MetadataService,
    validationService: ValidationService
  ) {
    super(leaf);
    this.metadataService = metadataService;
    this.validationService = validationService;
  }

  getViewType(): string { return REVIEW_VIEW_TYPE; }
  getDisplayText(): string { return "Review"; }
  getIcon(): string { return "check-square"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("carf-rv");
    await this.loadQueue();
    await this.render();
    this.registerDomEvent(document, "keydown", this.onKey.bind(this));
  }

  async loadQueue(): Promise<void> {
    const result = this.validationService.getLastResult();
    if (!result) await this.validationService.validateAll();

    const docs = this.validationService.getLastResult()?.documents || [];
    this.queue = docs
      .filter(d => d.file.name !== "README.md" && d.status === Status.REVIEW)
      .map(d => d.file);
    this.index = 0;
  }

  async render(): Promise<void> {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    // Empty state
    if (this.queue.length === 0) {
      const empty = el.createDiv({ cls: "carf-rv-empty" });
      empty.createEl("div", { text: "✓", cls: "carf-rv-done-icon" });
      empty.createEl("div", { text: "Nenhum arquivo para revisar", cls: "carf-rv-done-text" });
      return;
    }

    // Load current
    const file = this.queue[this.index];
    this.doc = await this.metadataService.parseDocument(file);
    this.issues = await this.validationService.validateFile(file);

    // Counter
    const counter = el.createDiv({ cls: "carf-rv-counter" });
    counter.createSpan({ text: `${this.index + 1}`, cls: "carf-rv-current" });
    counter.createSpan({ text: ` / ${this.queue.length}` });

    // Title
    el.createEl("h2", {
      text: this.doc.title || file.basename,
      cls: "carf-rv-title"
    });

    // Path
    el.createDiv({ text: file.path, cls: "carf-rv-path" });

    // Init frontmatter button if missing
    if (!this.doc.frontmatter) {
      const initBtn = el.createEl("button", {
        text: "criar yaml",
        cls: "carf-rv-init"
      });
      initBtn.onclick = () => this.initYaml();
    }

    // Issues
    if (this.issues.length > 0) {
      const issuesEl = el.createDiv({ cls: "carf-rv-issues" });
      for (const issue of this.issues) {
        const row = issuesEl.createDiv({ cls: "carf-rv-issue" });
        row.createSpan({ text: issue.icon + " " + issue.message });
      }
    }

    // Preview
    const preview = el.createDiv({ cls: "carf-rv-preview" });
    const content = this.metadataService.getBodyContent(this.doc.content);
    await MarkdownRenderer.render(this.app, content, preview, file.path, this);

    // Actions
    const actions = el.createDiv({ cls: "carf-rv-actions" });

    const prevBtn = actions.createEl("button", { text: "←", cls: "carf-rv-btn" });
    prevBtn.disabled = this.index === 0;
    prevBtn.onclick = () => this.prev();

    const rejectBtn = actions.createEl("button", { text: "✗ Rejeitar", cls: "carf-rv-btn carf-rv-reject" });
    rejectBtn.onclick = () => this.reject();

    const approveBtn = actions.createEl("button", { text: "✓ Aprovar", cls: "carf-rv-btn carf-rv-approve" });
    approveBtn.onclick = () => this.approve();

    const skipBtn = actions.createEl("button", { text: "→", cls: "carf-rv-btn" });
    skipBtn.onclick = () => this.next();

    // Open link
    const openLink = el.createDiv({ cls: "carf-rv-open" });
    const link = openLink.createEl("a", { text: "abrir no editor" });
    link.onclick = () => this.openInEditor();
  }

  async approve(): Promise<void> {
    if (!this.doc) return;
    await this.metadataService.setStatus(this.doc.file, Status.APPROVED);
    this.queue.splice(this.index, 1);
    if (this.index >= this.queue.length) this.index = Math.max(0, this.queue.length - 1);
    await this.render();
  }

  async reject(): Promise<void> {
    if (!this.doc) return;
    await this.metadataService.setStatus(this.doc.file, Status.REJECTED);
    this.queue.splice(this.index, 1);
    if (this.index >= this.queue.length) this.index = Math.max(0, this.queue.length - 1);
    await this.render();
  }

  async next(): Promise<void> {
    if (this.index < this.queue.length - 1) {
      this.index++;
      await this.render();
    }
  }

  async prev(): Promise<void> {
    if (this.index > 0) {
      this.index--;
      await this.render();
    }
  }

  async openInEditor(): Promise<void> {
    if (!this.doc) return;
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(this.doc.file);
  }

  async initYaml(): Promise<void> {
    if (!this.doc) return;
    await this.metadataService.initFrontmatter(this.doc.file);
    await this.render();
  }

  onKey(e: KeyboardEvent): void {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
    if (e.key === "ArrowLeft") this.prev();
    else if (e.key === "ArrowRight") this.next();
    else if (e.key.toLowerCase() === "a" && !e.ctrlKey) this.approve();
    else if (e.key.toLowerCase() === "r" && !e.ctrlKey) this.reject();
  }
}
