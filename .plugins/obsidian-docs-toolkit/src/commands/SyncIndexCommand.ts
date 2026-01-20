import { App, TFolder, Notice } from "obsidian";
import { IndexService } from "../services/IndexService";
import { Document } from "../models/Document";

/**
 * Command to sync README index
 */
export class SyncIndexCommand {
  private app: App;
  private indexService: IndexService;

  constructor(app: App, indexService: IndexService) {
    this.app = app;
    this.indexService = indexService;
  }

  /**
   * Execute the command for current folder
   */
  async execute(): Promise<void> {
    const activeFile = this.app.workspace.getActiveFile();

    if (!activeFile) {
      new Notice("Nenhum arquivo aberto");
      return;
    }

    const folder = activeFile.parent;
    if (!folder) {
      new Notice("Não foi possível determinar a pasta");
      return;
    }

    // Check if folder is in docs path
    if (!Document.isInCARFPath(folder.path)) {
      new Notice("Pasta não está em um caminho de documentação");
      return;
    }

    await this.indexService.syncFolderIndex(folder);
    new Notice("✓ Índice do README atualizado!");
  }

  /**
   * Sync all README indexes in the vault
   */
  async executeAll(): Promise<void> {
    new Notice("Atualizando todos os índices...");

    const folders = this.getAllCARFFolders();
    let updated = 0;

    for (const folder of folders) {
      // Check if folder has a README
      const readmePath = `${folder.path}/README.md`;
      if (this.app.vault.getAbstractFileByPath(readmePath)) {
        await this.indexService.syncFolderIndex(folder);
        updated++;
      }
    }

    new Notice(`✓ ${updated} índices atualizados!`);
  }

  /**
   * Get all folders in CARF paths
   */
  private getAllCARFFolders(): TFolder[] {
    const folders: TFolder[] = [];

    const processFolder = (folder: TFolder) => {
      if (Document.isInCARFPath(folder.path)) {
        folders.push(folder);
      }
      for (const child of folder.children) {
        if (child instanceof TFolder) {
          processFolder(child);
        }
      }
    };

    const root = this.app.vault.getRoot();
    processFolder(root);

    return folders;
  }
}
