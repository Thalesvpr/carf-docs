/**
 * Mock implementations for Obsidian API
 * Used in unit tests to avoid dependency on actual Obsidian
 */

export class TFile {
  path: string = "";
  name: string = "";
  basename: string = "";
  extension: string = "md";
  parent: TFolder | null = null;
  stat = { mtime: Date.now(), ctime: Date.now(), size: 0 };

  constructor(path?: string) {
    if (path) {
      this.path = path;
      this.name = path.split("/").pop() || "";
      this.basename = this.name.replace(/\.[^.]+$/, "");
      this.extension = this.name.split(".").pop() || "";
    }
  }
}

export class TFolder {
  path: string;
  name: string;
  children: (TFile | TFolder)[];
  parent: TFolder | null;

  constructor(path: string) {
    this.path = path;
    this.name = path.split("/").pop() || "";
    this.children = [];
    this.parent = null;
  }
}

export class App {
  vault = {
    getMarkdownFiles: () => [],
    getAbstractFileByPath: () => null,
    read: async () => "",
    modify: async () => {},
    getRoot: () => new TFolder("")
  };

  metadataCache = {
    getFirstLinkpathDest: () => null,
    getFileCache: () => null
  };

  workspace = {
    getActiveFile: () => null,
    getLeaf: () => null,
    getLeavesOfType: () => [],
    getRightLeaf: () => null,
    revealLeaf: () => {},
    on: () => ({ unload: () => {} }),
    onLayoutReady: (cb: () => void) => cb()
  };
}

export class Events {
  private handlers: Map<string, Set<(...args: unknown[]) => void>> = new Map();

  on(event: string, handler: (...args: unknown[]) => void): { unload: () => void } {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
    return {
      unload: () => this.handlers.get(event)?.delete(handler)
    };
  }

  trigger(event: string, ...args: unknown[]): void {
    this.handlers.get(event)?.forEach(handler => handler(...args));
  }
}

export class Notice {
  constructor(public message: string, public timeout?: number) {}
}

export class Modal {
  app: App;
  containerEl: HTMLElement;
  contentEl: HTMLElement;

  constructor(app: App) {
    this.app = app;
    this.containerEl = document.createElement("div");
    this.contentEl = document.createElement("div");
  }

  open(): void {}
  close(): void {}
  onOpen(): void {}
  onClose(): void {}
}

export class Menu {
  addItem(cb: (item: MenuItem) => void): this {
    cb(new MenuItem());
    return this;
  }
  addSeparator(): this {
    return this;
  }
  showAtMouseEvent(event: MouseEvent): void {}
}

export class MenuItem {
  setTitle(title: string): this { return this; }
  setIcon(icon: string): this { return this; }
  onClick(cb: () => void): this { return this; }
}

export class ItemView {
  app: App;
  leaf: WorkspaceLeaf;
  containerEl: HTMLElement;

  constructor(leaf: WorkspaceLeaf) {
    this.leaf = leaf;
    this.app = leaf.app;
    this.containerEl = document.createElement("div");
    this.containerEl.appendChild(document.createElement("div"));
  }

  getViewType(): string { return ""; }
  getDisplayText(): string { return ""; }
  getIcon(): string { return ""; }
  async onOpen(): Promise<void> {}
  async onClose(): Promise<void> {}
  registerEvent(eventRef: { unload: () => void }): void {}
}

export class WorkspaceLeaf {
  app: App;
  view: ItemView | null = null;

  constructor(app: App) {
    this.app = app;
  }

  async setViewState(state: { type: string; active: boolean }): Promise<void> {}
  async openFile(file: TFile): Promise<void> {}
}

export class Plugin {
  app: App;
  manifest: { id: string; name: string; version: string };

  constructor(app: App, manifest: { id: string; name: string; version: string }) {
    this.app = app;
    this.manifest = manifest;
  }

  async onload(): Promise<void> {}
  async onunload(): Promise<void> {}
  addCommand(command: { id: string; name: string; callback: () => void }): void {}
  addRibbonIcon(icon: string, title: string, callback: () => void): void {}
  addSettingTab(tab: PluginSettingTab): void {}
  registerView(type: string, factory: (leaf: WorkspaceLeaf) => ItemView): void {}
  registerEvent(eventRef: { unload: () => void }): void {}
  async loadData(): Promise<unknown> { return {}; }
  async saveData(data: unknown): Promise<void> {}
}

export class PluginSettingTab {
  app: App;
  plugin: Plugin;
  containerEl: HTMLElement;

  constructor(app: App, plugin: Plugin) {
    this.app = app;
    this.plugin = plugin;
    this.containerEl = document.createElement("div");
  }

  display(): void {}
  hide(): void {}
}

export class Setting {
  settingEl: HTMLElement;
  infoEl: HTMLElement;
  nameEl: HTMLElement;
  descEl: HTMLElement;
  controlEl: HTMLElement;

  constructor(containerEl: HTMLElement) {
    this.settingEl = document.createElement("div");
    this.infoEl = document.createElement("div");
    this.nameEl = document.createElement("div");
    this.descEl = document.createElement("div");
    this.controlEl = document.createElement("div");
    containerEl.appendChild(this.settingEl);
  }

  setName(name: string): this { return this; }
  setDesc(desc: string): this { return this; }
  addToggle(cb: (toggle: ToggleComponent) => void): this { return this; }
  addText(cb: (text: TextComponent) => void): this { return this; }
  addDropdown(cb: (dropdown: DropdownComponent) => void): this { return this; }
}

export class ToggleComponent {
  setValue(value: boolean): this { return this; }
  onChange(cb: (value: boolean) => void): this { return this; }
}

export class TextComponent {
  inputEl: HTMLInputElement;

  constructor() {
    this.inputEl = document.createElement("input");
  }

  setValue(value: string): this { return this; }
  setPlaceholder(placeholder: string): this { return this; }
  onChange(cb: (value: string) => void): this { return this; }
}

export class DropdownComponent {
  selectEl: HTMLSelectElement;

  constructor() {
    this.selectEl = document.createElement("select");
  }

  addOption(value: string, display: string): this { return this; }
  setValue(value: string): this { return this; }
  onChange(cb: (value: string) => void): this { return this; }
}

export function addIcon(id: string, svg: string): void {}

export function parseYaml(yaml: string): unknown {
  // Simple YAML parser mock - handles basic key: value pairs
  const result: Record<string, unknown> = {};
  const lines = yaml.split("\n");

  for (const line of lines) {
    const match = line.match(/^(\w+):\s*(.*)$/);
    if (match) {
      const [, key, value] = match;
      if (value.startsWith("[")) {
        // Array
        result[key] = value.slice(1, -1).split(",").map(s => s.trim()).filter(Boolean);
      } else if (value === "true" || value === "false") {
        result[key] = value === "true";
      } else if (!isNaN(Number(value))) {
        result[key] = Number(value);
      } else {
        result[key] = value.replace(/^["']|["']$/g, "");
      }
    }
  }

  return result;
}

export function stringifyYaml(obj: unknown): string {
  if (typeof obj !== "object" || obj === null) {
    return String(obj);
  }

  const lines: string[] = [];
  for (const [key, value] of Object.entries(obj)) {
    if (Array.isArray(value)) {
      lines.push(`${key}: [${value.join(", ")}]`);
    } else {
      lines.push(`${key}: ${value}`);
    }
  }
  return lines.join("\n");
}
