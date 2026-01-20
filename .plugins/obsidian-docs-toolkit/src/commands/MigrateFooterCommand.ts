import { App, TFile, Notice } from "obsidian";
import { MigrationService } from "../services/MigrationService";

/**
 * Command to migrate footer metadata to frontmatter
 */
export class MigrateFooterCommand {
  private app: App;
  private migrationService: MigrationService;

  constructor(app: App, migrationService: MigrationService) {
    this.app = app;
    this.migrationService = migrationService;
  }

  /**
   * Execute the command for current file
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

    const result = await this.migrationService.migrateFile(activeFile);

    if (result.success) {
      new Notice(
        `Migração concluída!\n` +
        `ID: ${result.newFrontmatter?.id}\n` +
        `Status: ${result.newFrontmatter?.status}`
      );
    } else {
      new Notice(`Migração falhou: ${result.message}`);
    }
  }

  /**
   * Execute the command for all files
   */
  async executeAll(): Promise<void> {
    new Notice("Iniciando migração de todos os arquivos...");
    await this.migrationService.migrateAll();
  }
}
