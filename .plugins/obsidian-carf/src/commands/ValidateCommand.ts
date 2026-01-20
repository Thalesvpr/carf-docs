import { App, TFile, Notice } from "obsidian";
import { ValidationService } from "../services/ValidationService";
import { Severity } from "../models/types";

/**
 * Command to validate files
 */
export class ValidateCommand {
  private app: App;
  private validationService: ValidationService;

  constructor(app: App, validationService: ValidationService) {
    this.app = app;
    this.validationService = validationService;
  }

  /**
   * Validate the current file
   */
  async executeFile(): Promise<void> {
    const activeFile = this.app.workspace.getActiveFile();

    if (!activeFile) {
      new Notice("Nenhum arquivo aberto");
      return;
    }

    if (!activeFile.name.endsWith(".md")) {
      new Notice("Apenas arquivos Markdown suportados");
      return;
    }

    const issues = await this.validationService.validateFile(activeFile);

    if (issues.length === 0) {
      new Notice("✓ Nenhum problema encontrado!");
      return;
    }

    const errors = issues.filter(i => i.severity === Severity.ERROR).length;
    const warnings = issues.filter(i => i.severity === Severity.WARNING).length;
    const info = issues.filter(i => i.severity === Severity.INFO).length;

    new Notice(
      `Problemas encontrados:\n` +
      `✗ ${errors} erros\n` +
      `⚠ ${warnings} avisos\n` +
      `ℹ ${info} info\n\n` +
      `Abra o Dashboard para detalhes.`
    );
  }

  /**
   * Validate all files in the vault
   */
  async executeAll(): Promise<void> {
    new Notice("Validando todos os arquivos...");

    const result = await this.validationService.validateAll();

    new Notice(
      `Validação concluída:\n` +
      `${result.documents.length} arquivos analisados\n` +
      `✗ ${result.summary.errors} erros\n` +
      `⚠ ${result.summary.warnings} avisos\n` +
      `ℹ ${result.summary.info} info`
    );
  }
}
