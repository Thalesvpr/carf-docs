import { App, TFile, Events } from "obsidian";
import { ConfigLoader } from "./ConfigLoader";
import { DocsLinterConfig } from "./ConfigSchema";

const CONFIG_FILENAME = ".docslint.yaml";

/**
 * Watches for config file changes and triggers reload
 * Emits "config-changed" event when config is updated
 */
export class ConfigWatcher extends Events {
  private app: App;
  private loader: ConfigLoader;
  private currentConfig: DocsLinterConfig | null = null;

  constructor(app: App, loader: ConfigLoader) {
    super();
    this.app = app;
    this.loader = loader;
  }

  /**
   * Start watching for config file changes
   */
  async start(): Promise<void> {
    // Load initial config
    this.currentConfig = await this.loader.loadConfig();

    // Watch for file modifications
    this.app.vault.on("modify", async (file) => {
      if (file instanceof TFile && file.path === CONFIG_FILENAME) {
        await this.reloadConfig();
      }
    });

    // Watch for file creation
    this.app.vault.on("create", async (file) => {
      if (file instanceof TFile && file.path === CONFIG_FILENAME) {
        await this.reloadConfig();
      }
    });

    // Watch for file deletion
    this.app.vault.on("delete", async (file) => {
      if (file instanceof TFile && file.path === CONFIG_FILENAME) {
        await this.reloadConfig();
      }
    });

    // Watch for file rename
    this.app.vault.on("rename", async (file, oldPath) => {
      if (file instanceof TFile) {
        if (file.path === CONFIG_FILENAME || oldPath === CONFIG_FILENAME) {
          await this.reloadConfig();
        }
      }
    });
  }

  /**
   * Reload config and emit event if changed
   */
  private async reloadConfig(): Promise<void> {
    this.loader.clearCache();
    const newConfig = await this.loader.loadConfig();

    // Simple comparison (could be more sophisticated)
    const changed = JSON.stringify(this.currentConfig) !== JSON.stringify(newConfig);

    if (changed) {
      this.currentConfig = newConfig;
      this.trigger("config-changed", newConfig);
    }
  }

  /**
   * Get the current config
   */
  getConfig(): DocsLinterConfig | null {
    return this.currentConfig;
  }
}
