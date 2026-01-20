import { App, TFile, Notice } from "obsidian";
import { MetadataService } from "../services/MetadataService";
import { Document } from "../models/Document";

/**
 * Command to initialize frontmatter in a file
 */
export class InitMetadataCommand {
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

    // Check if already has frontmatter
    const hasFrontmatter = await this.metadataService.hasFrontmatter(activeFile);
    if (hasFrontmatter) {
      new Notice("Arquivo já possui frontmatter");
      return;
    }

    // Check if file is in docs path
    if (!Document.isInCARFPath(activeFile.path)) {
      new Notice("Arquivo não está em um caminho de documentação (CENTRAL/ ou PROJECTS/)");
      return;
    }

    // Initialize frontmatter
    const frontmatter = await this.metadataService.initFrontmatter(activeFile);

    new Notice(
      `Frontmatter criado:\n` +
      `ID: ${frontmatter.id}\n` +
      `Tipo: ${frontmatter.type}\n` +
      `Status: ${frontmatter.status}`
    );
  }
}
