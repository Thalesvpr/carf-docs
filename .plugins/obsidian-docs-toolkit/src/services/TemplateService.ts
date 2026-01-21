import { App, TFile, parseYaml } from "obsidian";
import { Document } from "../core/Document";
import { TemplateValidation, TemplateFrontmatter, isTemplateFrontmatter } from "../config/ConfigSchema";

/**
 * Template definition with file reference and validation rules
 */
export interface Template {
  file: TFile;
  templateFor: string;
  validation: TemplateValidation;
}

/**
 * Service for discovering and applying template validation rules
 */
export class TemplateService {
  private app: App;
  private templateCache: Map<string, Template> = new Map();
  private initialized = false;

  constructor(app: App) {
    this.app = app;
  }

  /**
   * Initialize by discovering all templates in the vault
   */
  async initialize(): Promise<void> {
    this.templateCache.clear();
    await this.discoverTemplates();
    this.initialized = true;
  }

  /**
   * Get template validation rules for a document
   */
  getTemplateValidation(doc: Document): TemplateValidation | null {
    if (!this.initialized) {
      console.warn("TemplateService not initialized");
      return null;
    }

    // Check if document has a detected type
    if (doc.detectedType) {
      const template = this.templateCache.get(doc.detectedType);
      if (template) {
        return template.validation;
      }
    }

    // Check if document has a type in frontmatter
    const fmType = doc.getFrontmatterField<string>("type");
    if (fmType && fmType !== "template") {
      const template = this.templateCache.get(fmType.toLowerCase());
      if (template) {
        return template.validation;
      }
    }

    return null;
  }

  /**
   * Get a template by type name
   */
  getTemplate(typeName: string): Template | undefined {
    return this.templateCache.get(typeName.toLowerCase());
  }

  /**
   * Get all discovered templates
   */
  getAllTemplates(): Template[] {
    return Array.from(this.templateCache.values());
  }

  /**
   * Check if a document is a template
   */
  isTemplate(doc: Document): boolean {
    if (!doc.hasFrontmatter) return false;

    const fm = doc.frontmatter as Record<string, unknown>;
    return isTemplateFrontmatter(fm);
  }

  /**
   * Refresh a single template (after file change)
   */
  async refreshTemplate(file: TFile): Promise<void> {
    const template = await this.parseTemplateFile(file);

    if (template) {
      this.templateCache.set(template.templateFor, template);
    } else {
      // Check if this file was a template and remove it
      for (const [key, t] of this.templateCache.entries()) {
        if (t.file.path === file.path) {
          this.templateCache.delete(key);
          break;
        }
      }
    }
  }

  /**
   * Remove a template by file path
   */
  removeTemplate(filePath: string): void {
    for (const [key, template] of this.templateCache.entries()) {
      if (template.file.path === filePath) {
        this.templateCache.delete(key);
        break;
      }
    }
  }

  /**
   * Clear the template cache
   */
  clearCache(): void {
    this.templateCache.clear();
    this.initialized = false;
  }

  /**
   * Discover all template files in the vault
   */
  private async discoverTemplates(): Promise<void> {
    const files = this.app.vault.getMarkdownFiles();

    for (const file of files) {
      const template = await this.parseTemplateFile(file);
      if (template) {
        this.templateCache.set(template.templateFor, template);
      }
    }
  }

  /**
   * Parse a file to check if it's a template
   */
  private async parseTemplateFile(file: TFile): Promise<Template | null> {
    try {
      const content = await this.app.vault.read(file);
      const frontmatter = this.parseFrontmatter(content);

      if (!frontmatter) return null;

      if (!isTemplateFrontmatter(frontmatter)) {
        return null;
      }

      return {
        file,
        templateFor: frontmatter.template_for.toLowerCase(),
        validation: frontmatter.validation || {}
      };
    } catch (e) {
      console.error(`Failed to parse template file: ${file.path}`, e);
      return null;
    }
  }

  /**
   * Parse YAML frontmatter from content
   */
  private parseFrontmatter(content: string): Record<string, unknown> | null {
    const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!match) return null;

    try {
      return parseYaml(match[1]) as Record<string, unknown>;
    } catch {
      return null;
    }
  }
}
