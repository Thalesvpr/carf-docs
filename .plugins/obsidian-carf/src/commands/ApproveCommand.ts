import { App, Notice } from "obsidian";
import { MetadataService } from "../services/MetadataService";
import { Status } from "../models/types";
import { Document } from "../models/Document";

/**
 * Command to mark a document as approved
 */
export class ApproveCommand {
  private app: App;
  private metadataService: MetadataService;

  constructor(app: App, metadataService: MetadataService) {
    this.app = app;
    this.metadataService = metadataService;
  }

  /**
   * Execute the command
   */
  async execute(): Promise<void> {
    const activeFile = this.app.workspace.getActiveFile();

    if (!activeFile) {
      new Notice("Nenhum arquivo aberto");
      return;
    }

    if (!activeFile.name.endsWith(".md")) {
      new Notice("Apenas arquivos Markdown suportados");
      return;
    }

    // Check if file has frontmatter
    const hasFrontmatter = await this.metadataService.hasFrontmatter(activeFile);
    if (!hasFrontmatter) {
      new Notice("Arquivo não possui frontmatter. Execute 'CARF: Init Metadata' primeiro.");
      return;
    }

    // Check if file is in CARF path
    if (!Document.isInCARFPath(activeFile.path)) {
      new Notice("Arquivo não está em um caminho CARF");
      return;
    }

    // Set status to approved
    await this.metadataService.setStatus(activeFile, Status.APPROVED);

    new Notice("✓ Documento aprovado!");
  }
}
