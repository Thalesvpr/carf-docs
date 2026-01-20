import {
  App,
  Plugin,
  TFile,
  TFolder,
  WorkspaceLeaf,
  Menu,
  Notice,
  addIcon
} from "obsidian";

import { DocsToolkitSettings, DEFAULT_SETTINGS, DocsToolkitSettingTab } from "./src/settings";
import { DocumentStore } from "./src/store/DocumentStore";
import { MetadataService } from "./src/services/MetadataService";
import { IndexService } from "./src/services/IndexService";
import { MigrationService } from "./src/services/MigrationService";
import { CurationPanelView, CURATION_PANEL_VIEW_TYPE } from "./src/views/CurationPanelView";
import { IssuesPanelView, ISSUES_PANEL_VIEW_TYPE } from "./src/views/IssuesPanelView";
import { InitMetadataCommand } from "./src/commands/InitMetadataCommand";
import { MigrateFooterCommand } from "./src/commands/MigrateFooterCommand";
import { SyncIndexCommand } from "./src/commands/SyncIndexCommand";
import { Document } from "./src/models/Document";
import { Status } from "./src/models/types";

// Custom icon for Docs Toolkit
const DOCS_ICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 15l2 2 4-4"></path></svg>`;

/**
 * Docs Toolkit Plugin
 *
 * FLUXO DE CURADORIA:
 * ===================
 *
 * O plugin usa um único painel lateral (CurationPanelView) que concentra
 * todo o controle da curadoria. Não há "modo de review" separado.
 *
 * 1. O painel lateral mostra:
 *    - Progresso geral (aprovados/total, pendentes)
 *    - Informações do arquivo atual
 *    - Ações (aprovar, rejeitar, pular, navegar)
 *    - Status da sessão
 *
 * 2. Ao navegar entre arquivos, eles abrem automaticamente na área
 *    principal do Obsidian (editor nativo)
 *
 * 3. O usuário lê o arquivo e decide usando os botões do painel
 *    ou atalhos de teclado (A=aprovar, R=rejeitar, S=skip, ←/→=navegar)
 *
 * O review É simplesmente: olhar o arquivo → decidir
 */
export default class DocsToolkitPlugin extends Plugin {
  settings: DocsToolkitSettings;

  // Core store
  store: DocumentStore;

  // Services
  metadataService: MetadataService;
  indexService: IndexService;
  migrationService: MigrationService;

  // Commands
  private initMetadataCommand: InitMetadataCommand;
  private migrateFooterCommand: MigrateFooterCommand;
  private syncIndexCommand: SyncIndexCommand;

  // Status bar item
  private statusBarItem: HTMLElement;

  // Reference to curation panel
  private curationPanel: CurationPanelView | null = null;

  async onload(): Promise<void> {
    console.log("Loading Docs Toolkit Plugin");

    // Load settings
    await this.loadSettings();

    // Register custom icon
    addIcon("docs-icon", DOCS_ICON);

    // Initialize store (central state)
    this.store = new DocumentStore(this.app);

    // Apply validator settings
    for (const validator of this.store.getValidators()) {
      const enabled = this.settings.enabledValidators.includes(validator.id);
      this.store.setValidatorEnabled(validator.id, enabled);
    }

    // Initialize services
    this.metadataService = new MetadataService(this.app);
    this.indexService = new IndexService(this.app, this.metadataService);
    this.migrationService = new MigrationService(this.app, this.metadataService);

    // Initialize commands
    this.initMetadataCommand = new InitMetadataCommand(this.app, this.metadataService);
    this.migrateFooterCommand = new MigrateFooterCommand(this.app, this.migrationService);
    this.syncIndexCommand = new SyncIndexCommand(this.app, this.indexService);

    // Register the curation panel view (sidebar)
    this.registerView(
      CURATION_PANEL_VIEW_TYPE,
      (leaf) => {
        this.curationPanel = new CurationPanelView(leaf, this.store, this.metadataService);
        return this.curationPanel;
      }
    );

    // Register the issues panel view (like VS Code's Problems panel)
    this.registerView(
      ISSUES_PANEL_VIEW_TYPE,
      (leaf) => new IssuesPanelView(leaf, this.store)
    );

    // Register commands
    this.registerCommands();

    // Wire vault events to store
    this.registerVaultEvents();

    // Register context menu for folders
    this.registerFolderContextMenu();

    // Listen to store changes for status bar
    this.store.on("state-changed", () => this.updateStatusBar());

    // Add status bar item
    this.statusBarItem = this.addStatusBarItem();
    this.statusBarItem.setText("Docs: Loading...");
    this.statusBarItem.addClass("docs-toolkit-status-bar");
    this.statusBarItem.onclick = () => this.activateCurationPanel();

    // Add settings tab
    this.addSettingTab(new DocsToolkitSettingTab(this.app, this));

    // Add ribbon icon
    this.addRibbonIcon("docs-icon", "Open Curation Panel", () => {
      this.activateCurationPanel();
    });

    // Load initial state when vault is ready
    this.app.workspace.onLayoutReady(() => {
      this.store.loadAll();
    });
  }

  async onunload(): Promise<void> {
    console.log("Unloading Docs Toolkit Plugin");
  }

  /**
   * Register all plugin commands
   */
  private registerCommands(): void {
    // Init Metadata
    this.addCommand({
      id: "init-metadata",
      name: "Init Metadata",
      callback: () => this.initMetadataCommand.execute()
    });

    // Migrate Footer
    this.addCommand({
      id: "migrate-footer",
      name: "Migrate Footer",
      callback: () => this.migrateFooterCommand.execute()
    });

    // Migrate All Footers
    this.addCommand({
      id: "migrate-all-footers",
      name: "Migrate All Footers",
      callback: () => this.migrateFooterCommand.executeAll()
    });

    // Approve current file
    this.addCommand({
      id: "approve",
      name: "Approve Current File",
      hotkeys: [{ modifiers: ["Ctrl", "Shift"], key: "a" }],
      callback: () => this.approveCurrentFile()
    });

    // Reject current file
    this.addCommand({
      id: "reject",
      name: "Reject Current File",
      hotkeys: [{ modifiers: ["Ctrl", "Shift"], key: "r" }],
      callback: () => this.rejectCurrentFile()
    });

    // Sync Index
    this.addCommand({
      id: "sync-index",
      name: "Sync Index",
      callback: () => this.syncIndexCommand.execute()
    });

    // Sync All Indexes
    this.addCommand({
      id: "sync-all-indexes",
      name: "Sync All Indexes",
      callback: () => this.syncIndexCommand.executeAll()
    });

    // Open Curation Panel
    this.addCommand({
      id: "open-curation-panel",
      name: "Open Curation Panel",
      callback: () => this.activateCurationPanel()
    });

    // Open Issues Panel
    this.addCommand({
      id: "open-issues-panel",
      name: "Open Issues Panel",
      callback: () => this.activateIssuesPanel()
    });

  }

  /**
   * Wire vault events to store
   */
  private registerVaultEvents(): void {
    // On file modify
    this.registerEvent(
      this.app.vault.on("modify", async (file) => {
        if (!(file instanceof TFile)) return;
        if (!file.name.endsWith(".md")) return;
        if (!Document.isInCARFPath(file.path)) return;

        // Auto-update timestamp
        if (this.settings.autoUpdateTimestamp) {
          setTimeout(async () => {
            try {
              const hasFrontmatter = await this.metadataService.hasFrontmatter(file);
              if (hasFrontmatter) {
                await this.metadataService.updateTimestamp(file);
              }
            } catch (e) {
              console.error("Failed to update timestamp:", e);
            }
          }, 100);
        }

        // Update store (debounced to avoid rapid updates)
        setTimeout(() => this.store.updateDocument(file), 200);

        // Auto-sync index
        if (this.settings.autoSyncIndex && file.parent) {
          if (this.indexService.shouldSyncIndex(file)) {
            this.indexService.scheduleSync(file.parent);
          }
        }
      })
    );

    // On file create
    this.registerEvent(
      this.app.vault.on("create", async (file) => {
        if (!(file instanceof TFile)) return;
        if (!file.name.endsWith(".md")) return;
        if (!Document.isInCARFPath(file.path)) return;

        // Add to store
        await this.store.updateDocument(file);
      })
    );

    // On file rename
    this.registerEvent(
      this.app.vault.on("rename", async (file, oldPath) => {
        if (!(file instanceof TFile)) return;
        if (!file.name.endsWith(".md")) return;

        // Remove old path from store
        this.store.removeDocument(oldPath);

        // Add new path if in docs path
        if (Document.isInCARFPath(file.path)) {
          await this.store.updateDocument(file);
        }

        // Update indexes
        if (this.settings.autoSyncIndex) {
          const oldFolderPath = oldPath.substring(0, oldPath.lastIndexOf("/"));
          const oldFolder = this.app.vault.getAbstractFileByPath(oldFolderPath);
          if (oldFolder instanceof TFolder && Document.isInCARFPath(oldFolderPath)) {
            this.indexService.scheduleSync(oldFolder);
          }

          if (file.parent && Document.isInCARFPath(file.parent.path)) {
            this.indexService.scheduleSync(file.parent);
          }
        }
      })
    );

    // On file delete
    this.registerEvent(
      this.app.vault.on("delete", async (file) => {
        if (!(file instanceof TFile)) return;

        // Remove from store
        this.store.removeDocument(file.path);

        // Update indexes
        if (this.settings.autoSyncIndex) {
          const folderPath = file.path.substring(0, file.path.lastIndexOf("/"));
          const folder = this.app.vault.getAbstractFileByPath(folderPath);
          if (folder instanceof TFolder && Document.isInCARFPath(folderPath)) {
            this.indexService.scheduleSync(folder);
          }
        }
      })
    );
  }

  /**
   * Register context menu for folders
   */
  private registerFolderContextMenu(): void {
    this.registerEvent(
      this.app.workspace.on("file-menu", (menu: Menu, file) => {
        // Only for folders
        if (!(file instanceof TFolder)) return;

        // Only for CARF paths
        if (!Document.isInCARFPath(file.path)) return;

        menu.addSeparator();

        // Set all as Review
        menu.addItem((item) => {
          item
            .setTitle("Set all as Review")
            .setIcon("refresh-cw")
            .onClick(async () => {
              await this.setFolderStatus(file, Status.REVIEW);
            });
        });

        // Set all as Approved
        menu.addItem((item) => {
          item
            .setTitle("Set all as Approved")
            .setIcon("check")
            .onClick(async () => {
              await this.setFolderStatus(file, Status.APPROVED);
            });
        });
      })
    );
  }

  /**
   * Set status for all files in a folder
   */
  private async setFolderStatus(folder: TFolder, status: Status): Promise<void> {
    const files = this.getFilesInFolder(folder);
    let count = 0;

    for (const file of files) {
      if (file.name === "README.md") continue;
      await this.store.setStatus(file, status);
      count++;
    }

    new Notice(`${count} files set to ${status}`);
  }

  /**
   * Get all markdown files in a folder (recursive)
   */
  private getFilesInFolder(folder: TFolder): TFile[] {
    const files: TFile[] = [];

    for (const child of folder.children) {
      if (child instanceof TFile && child.extension === "md") {
        files.push(child);
      } else if (child instanceof TFolder) {
        files.push(...this.getFilesInFolder(child));
      }
    }

    return files;
  }

  /**
   * Update status bar with current stats
   */
  private updateStatusBar(): void {
    const state = this.store.getState();
    const docs = state.documents.filter(d => d.file.name !== "README.md");
    const approved = docs.filter(d => d.status === Status.APPROVED).length;
    const review = docs.filter(d => d.status === Status.REVIEW).length;
    const issues = state.summary.errors + state.summary.warnings;

    this.statusBarItem.setText(
      `Docs: ${approved}/${docs.length} | ${review} pending | ${issues} issues`
    );
  }

  /**
   * Approve current file
   */
  private async approveCurrentFile(): Promise<void> {
    const file = this.app.workspace.getActiveFile();
    if (!file || !Document.isInCARFPath(file.path)) return;
    await this.store.setStatus(file, Status.APPROVED);
  }

  /**
   * Reject current file
   */
  private async rejectCurrentFile(): Promise<void> {
    const file = this.app.workspace.getActiveFile();
    if (!file || !Document.isInCARFPath(file.path)) return;
    await this.store.setStatus(file, Status.REJECTED);
  }

  /**
   * Activate the curation panel in the right sidebar
   */
  async activateCurationPanel(): Promise<void> {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(CURATION_PANEL_VIEW_TYPE);

    if (leaves.length > 0) {
      leaf = leaves[0];
    } else {
      // Open in right sidebar
      leaf = workspace.getRightLeaf(false);
      if (leaf) {
        await leaf.setViewState({
          type: CURATION_PANEL_VIEW_TYPE,
          active: true
        });
      }
    }

    if (leaf) {
      workspace.revealLeaf(leaf);
    }
  }

  /**
   * Activate the issues panel (like VS Code's Problems panel)
   */
  async activateIssuesPanel(): Promise<void> {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(ISSUES_PANEL_VIEW_TYPE);

    if (leaves.length > 0) {
      leaf = leaves[0];
    } else {
      // Open in bottom panel (like VS Code)
      leaf = workspace.getLeaf("split", "horizontal");
      if (leaf) {
        await leaf.setViewState({
          type: ISSUES_PANEL_VIEW_TYPE,
          active: true
        });
      }
    }

    if (leaf) {
      workspace.revealLeaf(leaf);
    }
  }

  /**
   * Load plugin settings
   */
  async loadSettings(): Promise<void> {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  /**
   * Save plugin settings
   */
  async saveSettings(): Promise<void> {
    await this.saveData(this.settings);
  }
}
