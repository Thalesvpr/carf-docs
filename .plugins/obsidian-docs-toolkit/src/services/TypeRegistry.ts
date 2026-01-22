import { TFile } from "obsidian";
import { DocsLinterConfig, DocumentTypeConfig, DetectionConfig } from "../config/ConfigSchema";

/**
 * Extended type definition with resolved ID
 */
export interface DocumentTypeDefinition {
  id: string;
  name: string;
  detection: DetectionConfig;
  validation?: DocumentTypeConfig;
  template?: string;
  priority: number;
}

/**
 * TypeRegistry - Central source of truth for document type detection
 *
 * Replaces all hardcoded type detection scattered across the codebase.
 * Types are defined in .docslint.yaml and loaded at startup.
 *
 * Detection order:
 * 1. Types sorted by priority (higher first)
 * 2. For each type, check detection criteria (OR between criteria):
 *    - frontmatter.type match
 *    - filename.exact match
 *    - filename.pattern regex
 *    - path.contains substring
 *    - path.pattern regex
 * 3. First matching type wins
 * 4. Fallback to "doc" if no match
 */
export class TypeRegistry {
  private types: Map<string, DocumentTypeDefinition> = new Map();
  private sortedTypes: DocumentTypeDefinition[] = [];
  private fallbackType: DocumentTypeDefinition;

  constructor() {
    // Default fallback type
    this.fallbackType = {
      id: "doc",
      name: "Document",
      detection: {},
      priority: -999
    };
  }

  /**
   * Load types from config
   */
  loadFromConfig(config: DocsLinterConfig): void {
    this.types.clear();

    if (!config.documentTypes) {
      console.log("[TypeRegistry] No documentTypes in config");
      this.sortedTypes = [this.fallbackType];
      return;
    }

    // Load types from config
    for (const [id, typeConfig] of Object.entries(config.documentTypes)) {
      const typeDef: DocumentTypeDefinition = {
        id,
        name: typeConfig.name || id,
        detection: typeConfig.detection || {},
        validation: typeConfig,
        template: typeConfig.template,
        priority: typeConfig.priority ?? 0
      };
      this.types.set(id, typeDef);
    }

    // Sort by priority (higher first)
    this.sortedTypes = Array.from(this.types.values())
      .sort((a, b) => b.priority - a.priority);

    // Ensure fallback is always last
    if (!this.types.has("doc")) {
      this.sortedTypes.push(this.fallbackType);
    }

    console.log(`[TypeRegistry] Loaded ${this.types.size} types:`,
      this.sortedTypes.map(t => `${t.id}(${t.priority})`).join(", "));
  }

  /**
   * Detect the type of a document
   *
   * @param file - The file to check
   * @param frontmatter - Parsed frontmatter (can use metadataCache)
   * @returns The detected type ID
   */
  detectType(file: TFile, frontmatter: Record<string, unknown> | null): string {
    for (const typeDef of this.sortedTypes) {
      if (this.matchesType(file, frontmatter, typeDef)) {
        return typeDef.id;
      }
    }
    return this.fallbackType.id;
  }

  /**
   * Check if a file matches a type definition
   */
  private matchesType(
    file: TFile,
    frontmatter: Record<string, unknown> | null,
    typeDef: DocumentTypeDefinition
  ): boolean {
    const detection = typeDef.detection;
    if (!detection) return false;

    // Check frontmatter type (highest priority)
    if (detection.frontmatter?.type) {
      const fmType = frontmatter?.type;
      if (typeof fmType === "string" &&
          fmType.toLowerCase() === detection.frontmatter.type.toLowerCase()) {
        return true;
      }
    }

    // Check frontmatter field match (generic)
    if (detection.frontmatter?.field && detection.frontmatter?.value) {
      const fieldValue = frontmatter?.[detection.frontmatter.field];
      if (fieldValue === detection.frontmatter.value) {
        return true;
      }
    }

    // Check filename exact match
    if (detection.filename?.exact) {
      if (file.name === detection.filename.exact) {
        return true;
      }
    }

    // Check filename pattern (regex)
    if (detection.filename?.pattern) {
      try {
        const regex = new RegExp(detection.filename.pattern, "i");
        if (regex.test(file.name)) {
          return true;
        }
      } catch (e) {
        console.warn(`[TypeRegistry] Invalid filename pattern for ${typeDef.id}:`, e);
      }
    }

    // Check path contains (substring)
    if (detection.path?.contains) {
      const normalizedPath = file.path.toLowerCase();
      const searchPath = detection.path.contains.toLowerCase();
      if (normalizedPath.includes(searchPath)) {
        return true;
      }
    }

    // Check path pattern (regex/glob)
    if (detection.path?.pattern) {
      try {
        // Convert simple glob to regex
        const pattern = detection.path.pattern
          .replace(/\*\*/g, ".*")
          .replace(/\*/g, "[^/]*")
          .replace(/\?/g, ".");
        const regex = new RegExp(pattern, "i");
        if (regex.test(file.path)) {
          return true;
        }
      } catch (e) {
        console.warn(`[TypeRegistry] Invalid path pattern for ${typeDef.id}:`, e);
      }
    }

    return false;
  }

  /**
   * Get the validation config for a type
   */
  getValidationConfig(typeId: string): DocumentTypeConfig | null {
    return this.types.get(typeId)?.validation || null;
  }

  /**
   * Get full type definition
   */
  getType(typeId: string): DocumentTypeDefinition | null {
    return this.types.get(typeId) || null;
  }

  /**
   * Get all registered types
   */
  getAllTypes(): DocumentTypeDefinition[] {
    return this.sortedTypes;
  }

  /**
   * Check if a type exists
   */
  hasType(typeId: string): boolean {
    return this.types.has(typeId);
  }

  /**
   * Get human-readable name for a type
   */
  getTypeName(typeId: string): string {
    return this.types.get(typeId)?.name || typeId;
  }
}
