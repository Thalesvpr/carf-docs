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

// Core
import { Document } from "./src/core/Document";

// Config
import { ConfigLoader } from "./src/config/ConfigLoader";
import { ConfigWatcher } from "./src/config/ConfigWatcher";
import { DocsLinterConfig, DEFAULT_CONFIG } from "./src/config/ConfigSchema";

// Validators
import { ValidatorRegistry } from "./src/validators/ValidatorRegistry";
import { createBuiltinValidatorRegistry } from "./src/validators/builtin";

// Services
import { TemplateService } from "./src/services/TemplateService";
import { MetadataService } from "./src/services/MetadataService";
import { IndexService } from "./src/services/IndexService";
import { MigrationService } from "./src/services/MigrationService";

// i18n
import { I18nService } from "./src/i18n/I18nService";

// Store
import { DocumentStore } from "./src/store/DocumentStore";

// Views
import { CurationPanelView, CURATION_PANEL_VIEW_TYPE } from "./src/views/CurationPanelView";
import { IssuesPanelView, ISSUES_PANEL_VIEW_TYPE } from "./src/views/IssuesPanelView";

// Commands
import { InitMetadataCommand } from "./src/commands/InitMetadataCommand";
import { MigrateFooterCommand } from "./src/commands/MigrateFooterCommand";
import { SyncIndexCommand } from "./src/commands/SyncIndexCommand";

// Settings
import { DocsToolkitSettings, DEFAULT_SETTINGS, DocsToolkitSettingTab } from "./src/settings";

// Custom icon for Docs Toolkit
const DOCS_ICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 15l2 2 4-4"></path></svg>`;

/**
 * Docs Toolkit Plugin v2.0
 *
 * A fully configurable documentation linting and curation plugin.
 * Configuration via .docslint.yaml in vault root.
 */
export default class DocsToolkitPlugin extends Plugin {
  settings: DocsToolkitSettings;

  // Configuration
  private configLoader: ConfigLoader;
  private configWatcher: ConfigWatcher;
  private config: DocsLinterConfig;

  // Core components
  private registry: ValidatorRegistry;
  private templateService: TemplateService;
  private i18n: I18nService;
  store: DocumentStore;

  // Services
  metadataService: MetadataService;
  indexService: IndexService;
  migrationService: MigrationService;

  // Commands
  private initMetadataCommand: InitMetadataCommand;
  private migrateFooterCommand: MigrateFooterCommand;
  private syncIndexCommand: SyncIndexCommand;


  // Reference to curation panel
  private curationPanel: CurationPanelView | null = null;

  async onload(): Promise<void> {
    console.log("Loading Docs Toolkit Plugin v2.0");

    // Load plugin settings
    await this.loadSettings();

    // Register custom icon
    addIcon("docs-icon", DOCS_ICON);

    // Initialize configuration system
    this.configLoader = new ConfigLoader(this.app);
    this.config = await this.configLoader.loadConfig();

    // Initialize i18n
    this.i18n = new I18nService(this.app);
    await this.i18n.initialize(this.config.language);

    // Initialize validator registry with built-in validators
    this.registry = createBuiltinValidatorRegistry();

    // Initialize template service
    this.templateService = new TemplateService(this.app);

    // Initialize store
    this.store = new DocumentStore(
      this.app,
      this.config,
      this.registry,
      this.templateService,
      this.i18n
    );

    // Initialize config watcher for hot-reload
    this.configWatcher = new ConfigWatcher(this.app, this.configLoader);
    this.configWatcher.on("config-changed", (newConfig: DocsLinterConfig) => {
      this.onConfigChanged(newConfig);
    });
    await this.configWatcher.start();

    // Initialize services
    this.metadataService = new MetadataService(this.app);
    this.indexService = new IndexService(this.app, this.metadataService);
    this.migrationService = new MigrationService(this.app, this.metadataService);

    // Initialize commands
    this.initMetadataCommand = new InitMetadataCommand(this.app, this.metadataService);
    this.migrateFooterCommand = new MigrateFooterCommand(this.app, this.migrationService);
    this.syncIndexCommand = new SyncIndexCommand(this.app, this.indexService);

    // Register views
    this.registerView(
      CURATION_PANEL_VIEW_TYPE,
      (leaf) => {
        this.curationPanel = new CurationPanelView(
          leaf,
          this.store,
          this.metadataService,
          this.i18n,
          this.config
        );
        return this.curationPanel;
      }
    );

    this.registerView(
      ISSUES_PANEL_VIEW_TYPE,
      (leaf) => new IssuesPanelView(leaf, this.store, this.i18n)
    );

    // Register commands
    this.registerCommands();

    // Wire vault events to store
    this.registerVaultEvents();

    // Register context menu for folders
    this.registerFolderContextMenu();

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
    console.log("Unloading Docs Toolkit Plugin v2.0");
  }

  /**
   * Handle configuration changes (hot-reload)
   */
  private onConfigChanged(newConfig: DocsLinterConfig): void {
    console.log("Config changed, reloading...");
    this.config = newConfig;

    // Update language
    this.i18n.setLocale(newConfig.language);

    // Update store config
    this.store.updateConfig(newConfig);

    // Update curation panel config
    if (this.curationPanel) {
      this.curationPanel.updateConfig(newConfig);
    }

    // Re-validate all documents
    this.store.loadAll();

    new Notice("Docs Toolkit: Configuration reloaded");
  }

  /**
   * Check if file should be tracked
   */
  private isTrackedFile(path: string): boolean {
    for (const pattern of this.config.paths.exclude) {
      const regex = pattern
        .replace(/\*\*/g, ".*")
        .replace(/\*/g, "[^/]*");

      if (new RegExp(`^${regex}`).test(path)) {
        return false;
      }
    }
    return true;
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

    // Reload Configuration
    this.addCommand({
      id: "reload-config",
      name: "Reload Configuration",
      callback: async () => {
        this.configLoader.clearCache();
        const newConfig = await this.configLoader.loadConfig();
        this.onConfigChanged(newConfig);
      }
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
        if (!this.isTrackedFile(file.path)) return;

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

        // Update store (debounced)
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
        if (!this.isTrackedFile(file.path)) return;

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

        // Add new path if tracked
        if (this.isTrackedFile(file.path)) {
          await this.store.updateDocument(file);
        }

        // Update indexes
        if (this.settings.autoSyncIndex) {
          const oldFolderPath = oldPath.substring(0, oldPath.lastIndexOf("/"));
          const oldFolder = this.app.vault.getAbstractFileByPath(oldFolderPath);
          if (oldFolder instanceof TFolder && this.isTrackedFile(oldFolderPath)) {
            this.indexService.scheduleSync(oldFolder);
          }

          if (file.parent && this.isTrackedFile(file.parent.path)) {
            this.indexService.scheduleSync(file.parent);
          }
        }
      })
    );

    // On file delete
    this.registerEvent(
      this.app.vault.on("delete", async (file) => {
        if (!(file instanceof TFile)) return;

        this.store.removeDocument(file.path);

        // Update indexes
        if (this.settings.autoSyncIndex) {
          const folderPath = file.path.substring(0, file.path.lastIndexOf("/"));
          const folder = this.app.vault.getAbstractFileByPath(folderPath);
          if (folder instanceof TFolder && this.isTrackedFile(folderPath)) {
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
        if (!(file instanceof TFolder)) return;
        if (!this.isTrackedFile(file.path)) return;

        menu.addSeparator();

        // Set all as Review
        menu.addItem((item) => {
          item
            .setTitle("Set all as Review")
            .setIcon("refresh-cw")
            .onClick(async () => {
              await this.setFolderStatus(file, "review");
            });
        });

        // Set all as Approved
        menu.addItem((item) => {
          item
            .setTitle("Set all as Approved")
            .setIcon("check")
            .onClick(async () => {
              await this.setFolderStatus(file, "approved");
            });
        });

        // Regenerate README index
        menu.addItem((item) => {
          item
            .setTitle("Regenerate README index")
            .setIcon("list")
            .onClick(async () => {
              await this.regenerateReadmeIndex(file);
              new Notice(`README index regenerated for ${file.name}`);
            });
        });
      })
    );
  }

  /**
   * Set status for all files in a folder
   */
  private async setFolderStatus(folder: TFolder, status: string): Promise<void> {
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
   * Regenerate the README index for a folder
   */
  private async regenerateReadmeIndex(folder: TFolder): Promise<void> {
    await this.indexService.syncFolderIndex(folder);

    const readmePath = `${folder.path}/README.md`;
    const readme = this.app.vault.getAbstractFileByPath(readmePath) as TFile;
    if (readme) {
      await this.store.updateDocument(readme);
    }
  }

  /**
   * Approve current file
   */
  private async approveCurrentFile(): Promise<void> {
    const file = this.app.workspace.getActiveFile();
    if (!file || !this.isTrackedFile(file.path)) return;
    await this.store.setStatus(file, "approved");
  }

  /**
   * Reject current file
   */
  private async rejectCurrentFile(): Promise<void> {
    const file = this.app.workspace.getActiveFile();
    if (!file || !this.isTrackedFile(file.path)) return;
    await this.store.setStatus(file, "rejected");
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
   * Activate the issues panel
   */
  async activateIssuesPanel(): Promise<void> {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(ISSUES_PANEL_VIEW_TYPE);

    if (leaves.length > 0) {
      leaf = leaves[0];
    } else {
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
