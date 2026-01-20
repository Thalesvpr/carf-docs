import { App, TFile, TFolder } from "obsidian";
import { Document } from "../models/Document";
import { MetadataService } from "./MetadataService";
import { DocType, Status } from "../models/types";

/**
 * Service for generating and updating README index files
 */
export class IndexService {
  private app: App;
  private metadataService: MetadataService;
  private pendingSyncs: Set<string> = new Set();
  private syncTimeout: NodeJS.Timeout | null = null;

  constructor(app: App, metadataService: MetadataService) {
    this.app = app;
    this.metadataService = metadataService;
  }

  /**
   * Schedule a sync for a folder (debounced)
   */
  scheduleSync(folder: TFolder): void {
    this.pendingSyncs.add(folder.path);

    if (this.syncTimeout) {
      clearTimeout(this.syncTimeout);
    }

    this.syncTimeout = setTimeout(() => {
      this.processPendingSyncs();
    }, 2000); // Wait 2 seconds before syncing
  }

  /**
   * Process all pending sync requests
   */
  private async processPendingSyncs(): Promise<void> {
    const folders = Array.from(this.pendingSyncs);
    this.pendingSyncs.clear();

    for (const folderPath of folders) {
      const folder = this.app.vault.getAbstractFileByPath(folderPath);
      if (folder instanceof TFolder) {
        await this.syncFolderIndex(folder);
      }
    }
  }

  /**
   * Sync the README index for a folder
   */
  async syncFolderIndex(folder: TFolder): Promise<void> {
    const readmePath = `${folder.path}/README.md`;
    let readme = this.app.vault.getAbstractFileByPath(readmePath) as TFile | null;

    // Get all markdown files in the folder (except README)
    const files = folder.children
      .filter(f => f instanceof TFile && f.name.endsWith(".md") && f.name !== "README.md")
      .sort((a, b) => a.name.localeCompare(b.name)) as TFile[];

    // Get all subfolders
    const subfolders = folder.children
      .filter(f => f instanceof TFolder)
      .sort((a, b) => a.name.localeCompare(b.name)) as TFolder[];

    // Generate index content
    const indexContent = await this.generateIndexContent(folder, files, subfolders);

    if (readme) {
      // Update existing README
      const currentContent = await this.app.vault.read(readme);
      const newContent = this.updateIndexSection(currentContent, indexContent);
      if (newContent !== currentContent) {
        await this.app.vault.modify(readme, newContent);
      }
    }
  }

  /**
   * Generate index content for files and subfolders
   */
  private async generateIndexContent(
    folder: TFolder,
    files: TFile[],
    subfolders: TFolder[]
  ): Promise<string> {
    const lines: string[] = [];

    // Add subfolders section if any
    if (subfolders.length > 0) {
      lines.push("## Subpastas");
      lines.push("");
      for (const subfolder of subfolders) {
        const folderName = subfolder.name;
        lines.push(`- [[${subfolder.path}/README|${folderName}]]`);
      }
      lines.push("");
    }

    // Add files section if any
    if (files.length > 0) {
      lines.push("## Documentos");
      lines.push("");

      // Group by status if there are CARF documents
      const docsByStatus = new Map<Status, TFile[]>();

      for (const file of files) {
        const doc = await this.metadataService.parseDocument(file);
        const status = doc.status || Status.REVIEW;
        if (!docsByStatus.has(status)) {
          docsByStatus.set(status, []);
        }
        docsByStatus.get(status)!.push(file);
      }

      // List by status
      const statusOrder = [Status.REVIEW, Status.APPROVED, Status.REJECTED];
      const statusLabels: Record<Status, string> = {
        [Status.REVIEW]: "Em Revisão",
        [Status.APPROVED]: "Aprovados",
        [Status.REJECTED]: "Rejeitados"
      };

      for (const status of statusOrder) {
        const statusFiles = docsByStatus.get(status);
        if (statusFiles && statusFiles.length > 0) {
          lines.push(`### ${statusLabels[status]}`);
          lines.push("");
          for (const file of statusFiles) {
            const doc = await this.metadataService.parseDocument(file);
            const title = doc.title || file.basename;
            const icon = this.getStatusIcon(status);
            lines.push(`- ${icon} [[${file.path}|${title}]]`);
          }
          lines.push("");
        }
      }
    }

    return lines.join("\n");
  }

  /**
   * Get status icon
   */
  private getStatusIcon(status: Status): string {
    switch (status) {
      case Status.APPROVED:
        return "✓";
      case Status.REJECTED:
        return "✗";
      case Status.REVIEW:
      default:
        return "○";
    }
  }

  /**
   * Update the index section in README content
   */
  private updateIndexSection(content: string, indexContent: string): string {
    // Look for existing index section markers
    const startMarker = "<!-- CARF-INDEX-START -->";
    const endMarker = "<!-- CARF-INDEX-END -->";

    const startIdx = content.indexOf(startMarker);
    const endIdx = content.indexOf(endMarker);

    if (startIdx !== -1 && endIdx !== -1) {
      // Replace existing index section
      const before = content.substring(0, startIdx);
      const after = content.substring(endIdx + endMarker.length);
      return `${before}${startMarker}\n${indexContent}\n${endMarker}${after}`;
    }

    // No existing markers - append at end
    const separator = content.endsWith("\n") ? "" : "\n";
    return `${content}${separator}\n${startMarker}\n${indexContent}\n${endMarker}\n`;
  }

  /**
   * Check if a file change should trigger index sync
   */
  shouldSyncIndex(file: TFile): boolean {
    // Only sync for markdown files in CARF paths
    if (!file.name.endsWith(".md")) return false;
    if (!Document.isInCARFPath(file.path)) return false;

    // Check if folder has a README
    const folder = file.parent;
    if (!folder) return false;

    const readmePath = `${folder.path}/README.md`;
    return this.app.vault.getAbstractFileByPath(readmePath) !== null;
  }
}
