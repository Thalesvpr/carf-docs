import { ItemView, WorkspaceLeaf } from "obsidian";
import { ValidationService } from "../services/ValidationService";
import { Issue } from "../models/Issue";
import { REVIEW_VIEW_TYPE } from "./ReviewView";

export const DASHBOARD_VIEW_TYPE = "carf-dashboard";

export class DashboardView extends ItemView {
  private validationService: ValidationService;
  private onStartReview: () => void;

  constructor(leaf: WorkspaceLeaf, validationService: ValidationService, onStartReview: () => void) {
    super(leaf);
    this.validationService = validationService;
    this.onStartReview = onStartReview;
  }

  getViewType(): string { return DASHBOARD_VIEW_TYPE; }
  getDisplayText(): string { return "CARF"; }
  getIcon(): string { return "file-check"; }

  async onOpen(): Promise<void> {
    this.containerEl.children[1].addClass("carf-dashboard");
    await this.render();
  }

  async render(): Promise<void> {
    const el = this.containerEl.children[1] as HTMLElement;
    el.empty();

    const result = this.validationService.getLastResult();
    if (!result) {
      el.createSpan({ text: "carregando...", cls: "carf-loading" });
      await this.validationService.validateAll();
      await this.render();
      return;
    }

    // Header
    const header = el.createDiv({ cls: "carf-header" });
    header.createEl("h2", { text: "CARF" });
    const refresh = header.createEl("a", { text: "atualizar" });
    refresh.onclick = async () => {
      await this.validationService.validateAll();
      await this.render();
    };

    // Stats inline - all docs except READMEs
    const docs = result.documents.filter(d => d.file.name !== "README.md");
    const byStatus = this.validationService.getDocumentsByStatus(docs);
    const stats = el.createDiv({ cls: "carf-stats" });

    this.inlineStat(stats, docs.length, "total");
    this.inlineStat(stats, byStatus.approved.length, "approved", "#4ade80");
    this.inlineStat(stats, byStatus.rejected.length, "rejected", "#f87171");
    this.inlineStat(stats, byStatus.review.length, "review");

    // Start button
    if (byStatus.review.length > 0) {
      const btn = el.createEl("button", {
        text: `revisar ${byStatus.review.length} →`,
        cls: "carf-start-btn"
      });
      btn.onclick = () => this.onStartReview();
    }

    // Issues - filter to match docs
    const docPaths = new Set(docs.map(d => d.file.path));
    const issues = result.issues.filter(i => docPaths.has(i.file.path));

    if (issues.length > 0) {
      el.createDiv({ text: `${issues.length} issues`, cls: "carf-issues-title" });
      const list = el.createDiv({ cls: "carf-issues-list" });

      for (const issue of issues.slice(0, 30)) {
        const row = list.createDiv({ cls: "carf-issue-row" });
        row.textContent = `${issue.icon} ${issue.file.basename}: ${issue.message}`;
        row.onclick = () => this.openIssue(issue);
      }

      if (issues.length > 30) {
        el.createDiv({ text: `+${issues.length - 30} mais`, cls: "carf-more" });
      }
    }
  }

  private inlineStat(container: HTMLElement, value: number, label: string, color?: string): void {
    const s = container.createSpan({ cls: "carf-stat" });
    const num = s.createSpan({ text: value.toString(), cls: "carf-stat-num" });
    if (color) num.style.color = color;
    s.createSpan({ text: label, cls: "carf-stat-label" });
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
