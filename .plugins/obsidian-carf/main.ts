import {
  App,
  Plugin,
  TFile,
  TFolder,
  WorkspaceLeaf,
  addIcon
} from "obsidian";

import { CARFPluginSettings, DEFAULT_SETTINGS, CARFSettingTab } from "./src/settings";
import { MetadataService } from "./src/services/MetadataService";
import { ValidationService } from "./src/services/ValidationService";
import { IndexService } from "./src/services/IndexService";
import { MigrationService } from "./src/services/MigrationService";
import { DashboardView, DASHBOARD_VIEW_TYPE } from "./src/views/DashboardView";
import { ReviewView, REVIEW_VIEW_TYPE } from "./src/views/ReviewView";
import { InitMetadataCommand } from "./src/commands/InitMetadataCommand";
import { MigrateFooterCommand } from "./src/commands/MigrateFooterCommand";
import { ValidateCommand } from "./src/commands/ValidateCommand";
import { ApproveCommand } from "./src/commands/ApproveCommand";
import { RejectCommand } from "./src/commands/RejectCommand";
import { SyncIndexCommand } from "./src/commands/SyncIndexCommand";
import { Document } from "./src/models/Document";
import { Status, Severity } from "./src/models/types";

// Custom icon for CARF
const CARF_ICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 15l2 2 4-4"></path></svg>`;

export default class CARFPlugin extends Plugin {
  settings: CARFPluginSettings;

  // Services
  metadataService: MetadataService;
  validationService: ValidationService;
  indexService: IndexService;
  migrationService: MigrationService;

  // Commands
  private initMetadataCommand: InitMetadataCommand;
  private migrateFooterCommand: MigrateFooterCommand;
  private validateCommand: ValidateCommand;
  private approveCommand: ApproveCommand;
  private rejectCommand: RejectCommand;
  private syncIndexCommand: SyncIndexCommand;

  // Status bar item
  private statusBarItem: HTMLElement;

  async onload(): Promise<void> {
    console.log("Loading CARF Plugin");

    // Load settings
    await this.loadSettings();

    // Register custom icon
    addIcon("carf-icon", CARF_ICON);

    // Initialize services
    this.metadataService = new MetadataService(this.app);
    this.validationService = new ValidationService(this.app, this.metadataService);
    this.indexService = new IndexService(this.app, this.metadataService);
    this.migrationService = new MigrationService(this.app, this.metadataService);

    // Apply validator settings
    for (const validator of this.validationService.getValidators()) {
      const enabled = this.settings.enabledValidators.includes(validator.id);
      this.validationService.setValidatorEnabled(validator.id, enabled);
    }

    // Initialize commands
    this.initMetadataCommand = new InitMetadataCommand(this.app, this.metadataService);
    this.migrateFooterCommand = new MigrateFooterCommand(this.app, this.migrationService);
    this.validateCommand = new ValidateCommand(this.app, this.validationService);
    this.approveCommand = new ApproveCommand(this.app, this.metadataService);
    this.rejectCommand = new RejectCommand(this.app, this.metadataService);
    this.syncIndexCommand = new SyncIndexCommand(this.app, this.indexService);

    // Register views
    this.registerView(
      DASHBOARD_VIEW_TYPE,
      (leaf) => new DashboardView(leaf, this.validationService, () => this.activateReview())
    );

    this.registerView(
      REVIEW_VIEW_TYPE,
      (leaf) => new ReviewView(leaf, this.metadataService, this.validationService)
    );

    // Register commands
    this.registerCommands();

    // Register event handlers
    this.registerEventHandlers();

    // Add status bar item
    this.statusBarItem = this.addStatusBarItem();
    this.statusBarItem.setText("CARF: Loading...");
    this.statusBarItem.addClass("carf-status-bar");

    // Add settings tab
    this.addSettingTab(new CARFSettingTab(this.app, this));

    // Add ribbon icon
    this.addRibbonIcon("carf-icon", "Open CARF Dashboard", () => {
      this.activateDashboard();
    });

    // Run initial validation in background after vault is ready
    this.app.workspace.onLayoutReady(() => {
      this.runInitialValidation();
    });
  }

  async onunload(): Promise<void> {
    console.log("Unloading CARF Plugin");
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

    // Validate File
    this.addCommand({
      id: "validate-file",
      name: "Validate File",
      hotkeys: [{ modifiers: ["Ctrl", "Shift"], key: "v" }],
      callback: () => this.validateCommand.executeFile()
    });

    // Validate All
    this.addCommand({
      id: "validate-all",
      name: "Validate All",
      callback: () => this.validateCommand.executeAll()
    });

    // Approve
    this.addCommand({
      id: "approve",
      name: "Approve",
      hotkeys: [{ modifiers: ["Ctrl", "Shift"], key: "a" }],
      callback: () => this.approveCommand.execute()
    });

    // Reject
    this.addCommand({
      id: "reject",
      name: "Reject",
      hotkeys: [{ modifiers: ["Ctrl", "Shift"], key: "r" }],
      callback: () => this.rejectCommand.execute()
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
   * Register event handlers for file changes
   */
  private registerEventHandlers(): void {
    // On file modify
    this.registerEvent(
      this.app.vault.on("modify", async (file) => {
        if (!(file instanceof TFile)) return;
        if (!file.name.endsWith(".md")) return;
        if (!Document.isInCARFPath(file.path)) return;

        // Auto-update timestamp
        if (this.settings.autoUpdateTimestamp) {
          // Use a small delay to avoid conflicts with the user's save
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

        // Auto-validate
        if (this.settings.autoValidateOnSave) {
          const issues = await this.validationService.validateFile(file);
          this.updateStatusBar();
        }

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

        // Check if file matches CARF naming pattern and suggest init
        const type = Document.inferTypeFromFilename(file.name);
        if (type !== "OTHER" && type !== "README") {
          // Could show a suggestion to init metadata
          // For now, just log
          console.log(`CARF: New ${type} file created: ${file.name}`);
        }
      })
    );

    // On file rename
    this.registerEvent(
      this.app.vault.on("rename", async (file, oldPath) => {
        if (!(file instanceof TFile)) return;
        if (!file.name.endsWith(".md")) return;

        // Update any indexes that might be affected
        if (this.settings.autoSyncIndex) {
          // Old folder
          const oldFolderPath = oldPath.substring(0, oldPath.lastIndexOf("/"));
          const oldFolder = this.app.vault.getAbstractFileByPath(oldFolderPath);
          if (oldFolder instanceof TFolder && Document.isInCARFPath(oldFolderPath)) {
            this.indexService.scheduleSync(oldFolder);
          }

          // New folder
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
   * Run initial validation when plugin loads
   */
  private async runInitialValidation(): Promise<void> {
    try {
      await this.validationService.validateAll();
      this.updateStatusBar();
    } catch (e) {
      console.error("Initial validation failed:", e);
      this.statusBarItem.setText("CARF: Error");
    }
  }

  /**
   * Update status bar with current stats
   */
  private updateStatusBar(): void {
    const result = this.validationService.getLastResult();
    if (!result) {
      this.statusBarItem.setText("CARF: No data");
      return;
    }

    const byStatus = this.validationService.getDocumentsByStatus(result.documents);
    const errors = result.summary.errors;
    const warnings = result.summary.warnings;

    this.statusBarItem.setText(
      `CARF: ✓ ${byStatus.approved.length} | ✗ ${byStatus.rejected.length} | ○ ${byStatus.review.length} | ! ${errors + warnings} issues`
    );

    // Add click handler to open dashboard
    this.statusBarItem.onclick = () => this.activateDashboard();
  }

  /**
   * Activate the dashboard view
   */
  async activateDashboard(): Promise<void> {
    const { workspace } = this.app;

    let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(DASHBOARD_VIEW_TYPE);

    if (leaves.length > 0) {
      // Dashboard already open, focus it
      leaf = leaves[0];
    } else {
      // Open new dashboard
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
      // Review already open, focus it
      leaf = leaves[0];
    } else {
      // Open new review in main area
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
