import { App, PluginSettingTab, Setting } from "obsidian";
import type DocsToolkitPlugin from "../main";
import { VALID_MODULES } from "./models/types";

/**
 * Plugin settings interface
 */
export interface DocsToolkitSettings {
  // Paths
  centralPath: string;
  projectsPath: string;

  // Validators
  enabledValidators: string[];

  // Automation
  autoUpdateTimestamp: boolean;
  autoValidateOnSave: boolean;

  // Stale threshold in days
  staleThresholdDays: number;

  // UI
  maxDotsCount: number;

  // Index generation
  recursiveIndexDefault: "ask" | "yes" | "no";
}

/**
 * Default settings
 */
export const DEFAULT_SETTINGS: DocsToolkitSettings = {
  centralPath: "CENTRAL",
  projectsPath: "PROJECTS",
  enabledValidators: [
    "broken-links",
    "frontmatter",
    "orphans",
    "structure",
    "title",
    "stale",
    "empty-folders",
    "naming"
  ],
  autoUpdateTimestamp: true,
  autoValidateOnSave: true,
  staleThresholdDays: 180,
  maxDotsCount: 41,
  recursiveIndexDefault: "ask"
};

/**
 * Settings tab for the plugin
 */
export class DocsToolkitSettingTab extends PluginSettingTab {
  plugin: DocsToolkitPlugin;

  constructor(app: App, plugin: DocsToolkitPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl("h2", { text: "Docs Toolkit Settings" });

    // Paths section
    containerEl.createEl("h3", { text: "Paths" });

    new Setting(containerEl)
      .setName("Central path")
      .setDesc("Path to CENTRAL folder")
      .addText(text => text
        .setPlaceholder("CENTRAL")
        .setValue(this.plugin.settings.centralPath)
        .onChange(async (value) => {
          this.plugin.settings.centralPath = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName("Projects path")
      .setDesc("Path to PROJECTS folder")
      .addText(text => text
        .setPlaceholder("PROJECTS")
        .setValue(this.plugin.settings.projectsPath)
        .onChange(async (value) => {
          this.plugin.settings.projectsPath = value;
          await this.plugin.saveSettings();
        }));

    // Automation section
    containerEl.createEl("h3", { text: "Automation" });

    new Setting(containerEl)
      .setName("Auto-update timestamp")
      .setDesc("Automatically update 'updated' field when saving")
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.autoUpdateTimestamp)
        .onChange(async (value) => {
          this.plugin.settings.autoUpdateTimestamp = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName("Auto-validate on save")
      .setDesc("Run validation when saving a file")
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.autoValidateOnSave)
        .onChange(async (value) => {
          this.plugin.settings.autoValidateOnSave = value;
          await this.plugin.saveSettings();
        }));

    // Stale threshold
    new Setting(containerEl)
      .setName("Stale threshold (days)")
      .setDesc("Documents not updated after this many days are marked as stale")
      .addText(text => text
        .setPlaceholder("180")
        .setValue(String(this.plugin.settings.staleThresholdDays))
        .onChange(async (value) => {
          const days = parseInt(value);
          if (!isNaN(days) && days > 0) {
            this.plugin.settings.staleThresholdDays = days;
            await this.plugin.saveSettings();
          }
        }));

    // UI section
    containerEl.createEl("h3", { text: "UI" });

    new Setting(containerEl)
      .setName("Navigation dots count")
      .setDesc("Maximum number of dots shown in the curation panel navigation (11-101)")
      .addSlider(slider => slider
        .setLimits(11, 101, 10)
        .setValue(this.plugin.settings.maxDotsCount)
        .setDynamicTooltip()
        .onChange(async (value) => {
          this.plugin.settings.maxDotsCount = value;
          await this.plugin.saveSettings();
        }));

    // Index generation section
    containerEl.createEl("h3", { text: "Index Generation" });

    new Setting(containerEl)
      .setName("Recursive index regeneration")
      .setDesc("When regenerating README index, include subfolders?")
      .addDropdown(dropdown => dropdown
        .addOption("ask", "Always ask")
        .addOption("yes", "Always recursive")
        .addOption("no", "Only current folder")
        .setValue(this.plugin.settings.recursiveIndexDefault)
        .onChange(async (value: "ask" | "yes" | "no") => {
          this.plugin.settings.recursiveIndexDefault = value;
          await this.plugin.saveSettings();
        }));

    // Validators section
    containerEl.createEl("h3", { text: "Validators" });
    containerEl.createEl("p", {
      text: "Validators are now configured via .docslint.yaml in your vault root. Use the 'Docs Toolkit: Reload Configuration' command after editing.",
      cls: "setting-item-description"
    });
  }
}
