import {
  App,
  Plugin,
  TFile,
  TFolder,
  WorkspaceLeaf,
  addIcon
} from "obsidian";

import { DocsToolkitSettings, DEFAULT_SETTINGS, DocsToolkitSettingTab } from "./src/settings";
import { DocumentStore } from "./src/store/DocumentStore";
import { MetadataService } from "./src/services/MetadataService";
import { IndexService } from "./src/services/IndexService";
import { MigrationService } from "./src/services/MigrationService";
import { DashboardView, DASHBOARD_VIEW_TYPE } from "./src/views/DashboardView";
import { ReviewView, REVIEW_VIEW_TYPE } from "./src/views/ReviewView";
import { InitMetadataCommand } from "./src/commands/InitMetadataCommand";
import { MigrateFooterCommand } from "./src/commands/MigrateFooterCommand";
import { SyncIndexCommand } from "./src/commands/SyncIndexCommand";
import { Document } from "./src/models/Document";
import { Status } from "./src/models/types";

// Custom icon for Docs Toolkit
const DOCS_ICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 15l2 2 4-4"></path></svg>`;

export default class DocsToolkitPlugin extends Plugin {
  settings: DocsToolkitSettings;

  // Core store
  store: DocumentStore;

  // Services (simplified)
  metadataService: MetadataService;
  indexService: IndexService;
  migrationService: MigrationService;

  // Commands
  private initMetadataCommand: InitMetadataCommand;
  private migrateFooterCommand: MigrateFooterCommand;
  private syncIndexCommand: SyncIndexCommand;

  // Status bar item
  private statusBarItem: HTMLElement;

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

    // Initialize services (for commands only)
    this.metadataService = new MetadataService(this.app);
    this.indexService = new IndexService(this.app, this.metadataService);
    this.migrationService = new MigrationService(this.app, this.metadataService);

    // Initialize commands
    this.initMetadataCommand = new InitMetadataCommand(this.app, this.metadataService);
    this.migrateFooterCommand = new MigrateFooterCommand(this.app, this.migrationService);
    this.syncIndexCommand = new SyncIndexCommand(this.app, this.indexService);

    // Register views
    this.registerView(
      DASHBOARD_VIEW_TYPE,
      (leaf) => new DashboardView(leaf, this.store, () => this.activateReview())
    );

    this.registerView(
      REVIEW_VIEW_TYPE,
      (leaf) => new ReviewView(leaf, this.store, this.metadataService)
    );

    // Register commands
    this.registerCommands();

    // Wire vault events to store
    this.registerVaultEvents();

    // Listen to store changes for status bar
    this.store.on("state-changed", () => this.updateStatusBar());

    // Add status bar item
    this.statusBarItem = this.addStatusBarItem();
    this.statusBarItem.setText("Docs: Loading...");
    this.statusBarItem.addClass("docs-toolkit-status-bar");
    this.statusBarItem.onclick = () => this.activateDashboard();

    // Add settings tab
    this.addSettingTab(new DocsToolkitSettingTab(this.app, this));

    // Add ribbon icon
    this.addRibbonIcon("docs-icon", "Open Docs Toolkit Dashboard", () => {
      this.activateDashboard();
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

    // Approve
    this.addCommand({
      id: "approve",
      name: "Approve",
      hotkeys: [{ modifiers: ["Ctrl", "Shift"], key: "a" }],
      callback: () => this.approveCurrentFile()
    });

    // Reject
    this.addCommand({
      id: "reject",
      name: "Reject",
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

    // Open Dashboard
    this.addCommand({
      id: "open-dashboard",
      name: "Open Dashboard",
      callback: () => this.activateDashboard()
    });

    // Open Review Mode
    this.addCommand({
      id: "open-review",
      name: "Open Review Mode",
      callback: () => this.activateReview()
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

        // Add new path if in CARF path
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
   * Update status bar with current stats
   */
  private updateStatusBar(): void {
    const state = this.store.getState();
    const docs = state.documents.filter(d => d.file.name !== "README.md");
    const approved = docs.filter(d => d.status === Status.APPROVED).length;
    const rejected = docs.filter(d => d.status === Status.REJECTED).length;
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
   * Activate the dashboard view
   */
  async activateDashboard(): Promise<void> {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(DASHBOARD_VIEW_TYPE);

    if (leaves.length > 0) {
      leaf = leaves[0];
    } else {
      leaf = workspace.getRightLeaf(false);
      if (leaf) {
        await leaf.setViewState({
          type: DASHBOARD_VIEW_TYPE,
          active: true
        });
      }
    }

    if (leaf) {
      workspace.revealLeaf(leaf);
    }
  }

  /**
   * Activate the review view
   */
  async activateReview(): Promise<void> {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(REVIEW_VIEW_TYPE);

    if (leaves.length > 0) {
      leaf = leaves[0];
    } else {
      leaf = workspace.getLeaf(true);
      if (leaf) {
        await leaf.setViewState({
          type: REVIEW_VIEW_TYPE,
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
