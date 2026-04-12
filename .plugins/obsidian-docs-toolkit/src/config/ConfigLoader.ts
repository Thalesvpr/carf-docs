import { App, TFile, parseYaml } from "obsidian";
import {
  DocsLinterConfig,
  DEFAULT_CONFIG,
  PathsConfig,
  DocumentTypeConfig,
  ValidatorConfig,
  WorkflowConfig
} from "./ConfigSchema";

const CONFIG_FILENAME = ".docslint.yaml";
const PRESETS_PATH = ".plugins/obsidian-docs-toolkit/config/presets";

/**
 * Loads and parses .docslint.yaml configuration with preset inheritance
 */
export class ConfigLoader {
  private app: App;
  private configCache: DocsLinterConfig | null = null;
  private presetCache: Map<string, Partial<DocsLinterConfig>> = new Map();

  constructor(app: App) {
    this.app = app;
  }

  /**
   * Load the configuration from .docslint.yaml
   * Returns default config if file doesn't exist
   */
  async loadConfig(): Promise<DocsLinterConfig> {
    // Check for config file in vault root
    const configFile = this.app.vault.getAbstractFileByPath(CONFIG_FILENAME);

    if (!configFile || !(configFile instanceof TFile)) {
      console.log("DocsLinter: No .docslint.yaml found, using defaults");
      return this.deepClone(DEFAULT_CONFIG);
    }

    try {
      const content = await this.app.vault.read(configFile);
      const rawConfig = parseYaml(content) as Partial<DocsLinterConfig>;

      // Process extends
      const config = await this.resolveExtends(rawConfig);

      console.log("DocsLinter: Config after resolveExtends, exclude patterns:", config.paths?.exclude);

      // Merge with defaults
      this.configCache = this.mergeWithDefaults(config);

      console.log("DocsLinter: Final config exclude patterns:", this.configCache.paths.exclude);

      return this.configCache;
    } catch (e) {
      console.error("DocsLinter: Failed to parse .docslint.yaml", e);
      return this.deepClone(DEFAULT_CONFIG);
    }
  }

  /**
   * Get cached config or load if not cached
   */
  async getConfig(): Promise<DocsLinterConfig> {
    if (this.configCache) {
      return this.configCache;
    }
    return this.loadConfig();
  }

  /**
   * Clear the config cache (call when config file changes)
   */
  clearCache(): void {
    this.configCache = null;
    this.presetCache.clear();
  }

  /**
   * Resolve extends chain and merge configs
   */
  private async resolveExtends(
    config: Partial<DocsLinterConfig>
  ): Promise<Partial<DocsLinterConfig>> {
    if (!config.extends) {
      return config;
    }

    const extendsList = Array.isArray(config.extends)
      ? config.extends
      : [config.extends];

    let baseConfig: Partial<DocsLinterConfig> = {};

    for (const ext of extendsList) {
      const preset = await this.loadPreset(ext);
      baseConfig = this.mergeConfigs(baseConfig, preset);
    }

    // Remove extends from final config to avoid re-processing
    const { extends: _, ...configWithoutExtends } = config;

    return this.mergeConfigs(baseConfig, configWithoutExtends);
  }

  /**
   * Load a preset by name or path
   */
  private async loadPreset(name: string): Promise<Partial<DocsLinterConfig>> {
    // Check cache
    if (this.presetCache.has(name)) {
      console.log(`DocsLinter: Preset ${name} loaded from cache`);
      return this.presetCache.get(name)!;
    }

    // Determine path
    const path = name.startsWith("./")
      ? name
      : `${PRESETS_PATH}/${name}.yaml`;

    console.log(`DocsLinter: Loading preset ${name} from path: ${path}`);

    const presetFile = this.app.vault.getAbstractFileByPath(path);

    if (!presetFile || !(presetFile instanceof TFile)) {
      console.warn(`DocsLinter: Preset not found: ${name} at path: ${path}`);
      return {};
    }

    try {
      const content = await this.app.vault.read(presetFile);
      const preset = parseYaml(content) as Partial<DocsLinterConfig>;

      console.log(`DocsLinter: Preset ${name} loaded, exclude patterns:`, preset.paths?.exclude);

      // Recursively resolve extends in preset
      const resolved = await this.resolveExtends(preset);

      this.presetCache.set(name, resolved);
      return resolved;
    } catch (e) {
      console.error(`DocsLinter: Failed to load preset ${name}`, e);
      return {};
    }
  }

  /**
   * Merge two configs (source overwrites base)
   */
  private mergeConfigs(
    base: Partial<DocsLinterConfig>,
    source: Partial<DocsLinterConfig>
  ): Partial<DocsLinterConfig> {
    return {
      language: source.language ?? base.language,
      paths: this.mergePaths(base.paths, source.paths),
      documentTypes: this.mergeDocumentTypes(base.documentTypes, source.documentTypes),
      validators: this.mergeValidators(base.validators, source.validators),
      workflow: this.mergeWorkflow(base.workflow, source.workflow)
    };
  }

  /**
   * Merge paths config
   */
  private mergePaths(
    base?: PathsConfig,
    source?: PathsConfig
  ): PathsConfig | undefined {
    if (!base && !source) return undefined;
    if (!base) return source;
    if (!source) return base;

    return {
      include: [...(base.include || []), ...(source.include || [])],
      exclude: [...(base.exclude || []), ...(source.exclude || [])]
    };
  }

  /**
   * Merge document types (deep merge)
   */
  private mergeDocumentTypes(
    base?: Record<string, DocumentTypeConfig>,
    source?: Record<string, DocumentTypeConfig>
  ): Record<string, DocumentTypeConfig> | undefined {
    if (!base && !source) return undefined;
    if (!base) return source;
    if (!source) return base;

    const result = { ...base };

    for (const [key, value] of Object.entries(source)) {
      if (result[key]) {
        // Deep merge
        result[key] = {
          ...result[key],
          ...value,
          detection: { ...result[key].detection, ...value.detection },
          frontmatter: value.frontmatter
            ? { ...result[key].frontmatter, ...value.frontmatter }
            : result[key].frontmatter,
          sections: value.sections
            ? { ...result[key].sections, ...value.sections }
            : result[key].sections,
          title: value.title
            ? { ...result[key].title, ...value.title }
            : result[key].title
        };
      } else {
        result[key] = value;
      }
    }

    return result;
  }

  /**
   * Merge validators config
   */
  private mergeValidators(
    base?: Record<string, ValidatorConfig>,
    source?: Record<string, ValidatorConfig>
  ): Record<string, ValidatorConfig> | undefined {
    if (!base && !source) return undefined;
    if (!base) return source;
    if (!source) return base;

    const result = { ...base };

    for (const [key, value] of Object.entries(source)) {
      if (result[key]) {
        result[key] = { ...result[key], ...value };
      } else {
        result[key] = value;
      }
    }

    return result;
  }

  /**
   * Merge workflow config
   */
  private mergeWorkflow(
    base?: WorkflowConfig,
    source?: WorkflowConfig
  ): WorkflowConfig | undefined {
    if (!base && !source) return undefined;
    if (!base) return source;
    if (!source) return base;

    return {
      statuses: { ...base.statuses, ...source.statuses }
    };
  }

  /**
   * Merge config with defaults
   */
  private mergeWithDefaults(config: Partial<DocsLinterConfig>): DocsLinterConfig {
    return {
      language: config.language ?? DEFAULT_CONFIG.language,
      paths: {
        include: config.paths?.include ?? DEFAULT_CONFIG.paths.include,
        exclude: config.paths?.exclude ?? DEFAULT_CONFIG.paths.exclude
      },
      documentTypes: config.documentTypes ?? DEFAULT_CONFIG.documentTypes,
      validators: {
        ...DEFAULT_CONFIG.validators,
        ...config.validators
      },
      workflow: {
        statuses: {
          ...DEFAULT_CONFIG.workflow.statuses,
          ...config.workflow?.statuses
        }
      }
    };
  }

  /**
   * Deep clone an object
   */
  private deepClone<T>(obj: T): T {
    return JSON.parse(JSON.stringify(obj));
  }
}
