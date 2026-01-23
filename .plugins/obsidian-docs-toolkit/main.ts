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
import { TypeRegistry } from "./src/services/TypeRegistry";

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
  typeRegistry: TypeRegistry;

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

    // Initialize TypeRegistry for data-driven type detection
    this.typeRegistry = new TypeRegistry();
    this.typeRegistry.loadFromConfig(this.config);

    // Initialize template service
    this.templateService = new TemplateService(this.app);

    // Initialize store
    this.store = new DocumentStore(
      this.app,
      this.config,
      this.registry,
      this.templateService,
      this.i18n,
      this.typeRegistry
    );

    // Initialize config watcher for hot-reload
    this.configWatcher = new ConfigWatcher(this.app, this.configLoader);
    this.configWatcher.on("config-changed", (newConfig: DocsLinterConfig) => {
      this.onConfigChanged(newConfig);
    });
    await this.configWatcher.start();

    // Initialize services
    this.metadataService = new MetadataService(this.app, this.typeRegistry);
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
          this.config,
          this
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

    // Reload TypeRegistry with new config
    this.typeRegistry.loadFromConfig(newConfig);

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
      // Use placeholder to avoid ** being affected by * replacement
      const regex = pattern
        .replace(/\*\*/g, "<<DOUBLESTAR>>")
        .replace(/\*/g, "[^/]*")
        .replace(/<<DOUBLESTAR>>/g, ".*")
        .replace(/\?/g, ".");

      if (new RegExp(`^${regex}$`).test(path)) {
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

    // Debug: Show current exclude patterns
    this.addCommand({
      id: "debug-excludes",
      name: "Debug: Show Exclude Patterns",
      callback: () => {
        const excludes = this.config.paths.exclude;
        console.log("[Docs Toolkit] Current exclude patterns:", excludes);
        new Notice(`Exclude patterns (${excludes.length}):\n${excludes.join("\n")}`);
      }
    });

    // Validate Current File (debug command)
    this.addCommand({
      id: "validate-current-file",
      name: "Validate Current File",
      callback: async () => {
        const file = this.app.workspace.getActiveFile();
        if (!file) {
          new Notice("No active file");
          return;
        }

        if (!file.name.endsWith(".md")) {
          new Notice("Not a markdown file");
          return;
        }

        // Force revalidation
        await this.store.updateDocument(file);
        const issues = this.store.getIssuesForFile(file.path);
        const doc = this.store.getDocument(file.path);

        // Show results
        const docType = doc?.detectedType || "generic";
        const tracked = this.isTrackedFile(file.path);

        if (!tracked) {
          new Notice(`File is EXCLUDED from validation (check paths.exclude)`);
          return;
        }

        if (issues.length === 0) {
          new Notice(`✓ ${file.name}\nType: ${docType}\nNo issues found`);
        } else {
          const errors = issues.filter(i => i.severity === "error").length;
          const warnings = issues.filter(i => i.severity === "warning").length;
          new Notice(`✗ ${file.name}\nType: ${docType}\n${errors} errors, ${warnings} warnings`);

          // Log details to console
          console.log(`[Docs Toolkit] Validation results for ${file.path}:`);
          console.log(`  Document type: ${docType}`);
          issues.forEach(i => {
            console.log(`  [${i.severity.toUpperCase()}] ${i.messageKey}`, i.messageParams);
          });
        }
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
      })
    );

    // On metadata change (Properties panel edits)
    this.registerEvent(
      this.app.metadataCache.on("changed", (file) => {
        if (!(file instanceof TFile)) return;
        if (!file.name.endsWith(".md")) return;
        if (!this.isTrackedFile(file.path)) return;

        // Update store immediately for metadata changes
        this.store.updateDocument(file);
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
      })
    );

    // On file delete
    this.registerEvent(
      this.app.vault.on("delete", async (file) => {
        if (!(file instanceof TFile)) return;

        this.store.removeDocument(file.path);
      })
    );
  }

  /**
   * Register context menu for folders
   */
  private registerFolderContextMenu(): void {
    this.registerEvent(
      this.app.workspace.on("file-menu", (menu: Menu, file) => {
        // Handle README.md files
        if (file instanceof TFile && file.name === "README.md") {
          if (!this.isTrackedFile(file.path)) return;
          const folder = file.parent;
          if (!folder) return;

          menu.addSeparator();

          // Regenerate index for this README
          menu.addItem((item) => {
            item
              .setTitle("Regenerate index")
              .setIcon("file-text")
              .onClick(async () => {
                console.log("[DocsToolkit] Regenerate index clicked");
                console.log("[DocsToolkit] file.path:", file.path);
                console.log("[DocsToolkit] folder:", folder?.path);
                try {
                  await this.indexService.syncFolderIndex(folder);
                  await this.store.updateDocument(file);
                  new Notice(`Índice regenerado: ${file.name}`);
                } catch (e) {
                  console.error("[DocsToolkit] Error:", e);
                  new Notice(`Erro ao regenerar índice: ${e}`);
                }
              });
          });
          return;
        }

        // Handle folders
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

        // Update all YAML (add missing fields)
        menu.addItem((item) => {
          item
            .setTitle("Update all YAML")
            .setIcon("file-code")
            .onClick(async () => {
              await this.updateFolderYaml(file);
            });
        });

        // Regenerate README index (current folder only)
        menu.addItem((item) => {
          item
            .setTitle("Regenerate index")
            .setIcon("file-text")
            .onClick(async () => {
              await this.regenerateReadmeIndex(file, false);
              new Notice(`Índice regenerado: ${file.name}`);
            });
        });

        // Regenerate README index (recursive)
        const hasSubfolders = file.children.some(c => c instanceof TFolder);
        if (hasSubfolders) {
          menu.addItem((item) => {
            item
              .setTitle("Regenerate index (all)")
              .setIcon("list-tree")
              .onClick(async () => {
                const count = await this.regenerateReadmeIndex(file, true);
                new Notice(`Índice regenerado em ${count} pastas`);
              });
          });
        }
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
   * Update YAML for all files in a folder (add missing fields)
   */
  private async updateFolderYaml(folder: TFolder): Promise<void> {
    const files = this.getFilesInFolder(folder);
    let updated = 0;
    const fieldCounts: Record<string, number> = {};

    for (const file of files) {
      try {
        const result = await this.metadataService.updateFrontmatter(file);
        if (result.updated) {
          updated++;
          for (const field of result.fields) {
            fieldCounts[field] = (fieldCounts[field] || 0) + 1;
          }
        }
      } catch (e) {
        console.error(`Failed to update YAML for ${file.path}:`, e);
      }
    }

    // Build summary
    const details = Object.entries(fieldCounts)
      .map(([field, count]) => `${field}: ${count}`)
      .join(", ");

    new Notice(`Updated ${updated}/${files.length} files${details ? ` (${details})` : ""}`);

    // Refresh store
    await this.store.loadAll();
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
   * @param folder The folder to regenerate index for
   * @param recursive Whether to include subfolders
   * @returns Number of folders processed
   */
  async regenerateReadmeIndex(folder: TFolder, recursive: boolean = false): Promise<number> {
    let count = 0;

    // Process current folder
    await this.indexService.syncFolderIndex(folder);
    const readmePath = `${folder.path}/README.md`;
    const readme = this.app.vault.getAbstractFileByPath(readmePath) as TFile;
    if (readme) {
      await this.store.updateDocument(readme);
      count++;
    }

    // Process subfolders if recursive
    if (recursive) {
      for (const child of folder.children) {
        if (child instanceof TFolder) {
          count += await this.regenerateReadmeIndex(child, true);
        }
      }
    }

    return count;
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
