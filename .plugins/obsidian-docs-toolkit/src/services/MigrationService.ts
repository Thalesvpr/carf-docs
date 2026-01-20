import { App, TFile, TFolder, Notice } from "obsidian";
import { Document } from "../models/Document";
import { MetadataService } from "./MetadataService";
import { DocType, Status, Module, CARFFrontmatter, VALID_MODULES } from "../models/types";

/**
 * Result of a migration operation
 */
export interface MigrationResult {
  file: TFile;
  success: boolean;
  message: string;
  oldFooter?: string;
  newFrontmatter?: CARFFrontmatter;
}

/**
 * Service for migrating old footer-based metadata to YAML frontmatter
 */
export class MigrationService {
  private app: App;
  private metadataService: MetadataService;

  constructor(app: App, metadataService: MetadataService) {
    this.app = app;
    this.metadataService = metadataService;
  }

  /**
   * Migrate a single file from footer to frontmatter
   */
  async migrateFile(file: TFile): Promise<MigrationResult> {
    const content = await this.app.vault.read(file);

    // Check if already has frontmatter
    if (content.startsWith("---\n")) {
      return {
        file,
        success: false,
        message: "Arquivo já possui frontmatter"
      };
    }

    // Try to extract footer metadata
    const footerData = this.extractFooterMetadata(content);

    if (!footerData) {
      return {
        file,
        success: false,
        message: "Nenhum footer de metadados encontrado"
      };
    }

    // Create frontmatter from footer data
    const frontmatter = this.createFrontmatterFromFooter(file, footerData);

    // Remove footer from content
    const contentWithoutFooter = this.removeFooter(content);

    // Add frontmatter
    const newContent = this.addFrontmatter(contentWithoutFooter, frontmatter);

    // Write the new content
    await this.app.vault.modify(file, newContent);

    return {
      file,
      success: true,
      message: "Migração concluída com sucesso",
      oldFooter: footerData.raw,
      newFrontmatter: frontmatter
    };
  }

  /**
   * Migrate all files in the vault
   */
  async migrateAll(): Promise<MigrationResult[]> {
    const results: MigrationResult[] = [];
    const files = this.getCARFFiles();

    let migrated = 0;
    let skipped = 0;
    let failed = 0;

    for (const file of files) {
      const result = await this.migrateFile(file);
      results.push(result);

      if (result.success) {
        migrated++;
      } else if (result.message.includes("já possui")) {
        skipped++;
      } else {
        failed++;
      }
    }

    new Notice(
      `Migração concluída:\n` +
      `✓ ${migrated} migrados\n` +
      `○ ${skipped} já tinham frontmatter\n` +
      `✗ ${failed} falharam`
    );

    return results;
  }

  /**
   * Extract metadata from old footer format
   */
  private extractFooterMetadata(content: string): FooterData | null {
    // Look for footer patterns like:
    // ---
    // **Status:** Review
    // **Módulos:** GEOAPI, GEOWEB
    // **Epic:** authentication
    // ---

    const footerPatterns = [
      // Pattern 1: Horizontal rules around metadata
      /\n---\n([\s\S]*?\*\*Status:\*\*[\s\S]*?)\n---\s*$/,
      // Pattern 2: Just metadata at end of file
      /\n(\*\*Status:\*\*[^\n]*(?:\n\*\*[^*]+:\*\*[^\n]*)*)\s*$/,
      // Pattern 3: Metadata section with header
      /\n##\s*Meta(?:dados?|data)?\s*\n([\s\S]*?\*\*Status:\*\*[\s\S]*?)$/i
    ];

    let footerMatch: RegExpMatchArray | null = null;
    for (const pattern of footerPatterns) {
      footerMatch = content.match(pattern);
      if (footerMatch) break;
    }

    if (!footerMatch) return null;

    const footerContent = footerMatch[1];
    const data: FooterData = { raw: footerMatch[0] };

    // Extract status
    const statusMatch = footerContent.match(/\*\*Status:\*\*\s*(\w+)/i);
    if (statusMatch) {
      data.status = this.normalizeStatus(statusMatch[1]);
    }

    // Extract modules
    const modulesMatch = footerContent.match(/\*\*M[óo]dulos?:\*\*\s*([^\n]+)/i);
    if (modulesMatch) {
      data.modules = this.parseModules(modulesMatch[1]);
    }

    // Extract epic
    const epicMatch = footerContent.match(/\*\*Epic:\*\*\s*([^\n]+)/i);
    if (epicMatch) {
      data.epic = epicMatch[1].trim();
    }

    // Extract created date
    const createdMatch = footerContent.match(/\*\*Cria[çc][ãa]o:\*\*\s*([^\n]+)/i);
    if (createdMatch) {
      data.created = this.parseDate(createdMatch[1]);
    }

    // Extract updated date
    const updatedMatch = footerContent.match(/\*\*Atualiza[çc][ãa]o:\*\*\s*([^\n]+)/i);
    if (updatedMatch) {
      data.updated = this.parseDate(updatedMatch[1]);
    }

    return data;
  }

  /**
   * Normalize status value
   */
  private normalizeStatus(status: string): Status {
    const normalized = status.toLowerCase().trim();
    switch (normalized) {
      case "approved":
      case "aprovado":
        return Status.APPROVED;
      case "rejected":
      case "rejeitado":
        return Status.REJECTED;
      case "review":
      case "revisão":
      case "revisao":
      case "em revisão":
      case "em revisao":
      default:
        return Status.REVIEW;
    }
  }

  /**
   * Parse modules from string
   */
  private parseModules(modulesStr: string): Module[] {
    return modulesStr
      .split(/[,;]/)
      .map(m => m.trim().toUpperCase())
      .filter(m => VALID_MODULES.includes(m as Module)) as Module[];
  }

  /**
   * Parse date from string
   */
  private parseDate(dateStr: string): string {
    // Try to parse various date formats
    const cleaned = dateStr.trim();

    // ISO format
    if (/^\d{4}-\d{2}-\d{2}$/.test(cleaned)) {
      return cleaned;
    }

    // BR format: DD/MM/YYYY
    const brMatch = cleaned.match(/(\d{2})\/(\d{2})\/(\d{4})/);
    if (brMatch) {
      return `${brMatch[3]}-${brMatch[2]}-${brMatch[1]}`;
    }

    // Try to parse with Date
    try {
      const date = new Date(cleaned);
      if (!isNaN(date.getTime())) {
        return date.toISOString().split("T")[0];
      }
    } catch {
      // Ignore parse errors
    }

    // Default to today
    return new Date().toISOString().split("T")[0];
  }

  /**
   * Create frontmatter from extracted footer data
   */
  private createFrontmatterFromFooter(file: TFile, footerData: FooterData): CARFFrontmatter {
    const type = Document.inferTypeFromFilename(file.name);
    const id = this.extractIdFromFilename(file.name) || "";
    const now = this.metadataService.formatDate(new Date());

    return {
      id: id,
      type: type,
      modules: footerData.modules || [],
      epic: footerData.epic || "",
      status: footerData.status || Status.REVIEW,
      created: footerData.created || now,
      updated: footerData.updated || now
    };
  }

  /**
   * Extract ID from filename
   */
  private extractIdFromFilename(filename: string): string | null {
    const match = filename.match(/^(RF|RNF|UC|US)-\d{3}/);
    return match ? match[0] : null;
  }

  /**
   * Remove footer from content
   */
  private removeFooter(content: string): string {
    const footerPatterns = [
      /\n---\n[\s\S]*?\*\*Status:\*\*[\s\S]*?\n---\s*$/,
      /\n\*\*Status:\*\*[^\n]*(?:\n\*\*[^*]+:\*\*[^\n]*)*\s*$/,
      /\n##\s*Meta(?:dados?|data)?\s*\n[\s\S]*?\*\*Status:\*\*[\s\S]*?$/i
    ];

    let result = content;
    for (const pattern of footerPatterns) {
      result = result.replace(pattern, "");
    }

    return result.trimEnd() + "\n";
  }

  /**
   * Add frontmatter to content
   */
  private addFrontmatter(content: string, frontmatter: CARFFrontmatter): string {
    const yaml = this.frontmatterToYaml(frontmatter);
    return `---\n${yaml}---\n\n${content}`;
  }

  /**
   * Convert frontmatter object to YAML string
   */
  private frontmatterToYaml(fm: CARFFrontmatter): string {
    const lines: string[] = [];

    // Required fields
    lines.push(`status: ${fm.status}`);
    lines.push(`updated: ${fm.updated}`);

    // Optional fields
    if (fm.id) {
      lines.push(`id: ${fm.id}`);
    }
    if (fm.type) {
      lines.push(`type: ${fm.type}`);
    }
    if (fm.modules && fm.modules.length > 0) {
      lines.push(`modules: [${fm.modules.join(", ")}]`);
    }
    if (fm.epic) {
      lines.push(`epic: ${fm.epic}`);
    }
    if (fm.created) {
      lines.push(`created: ${fm.created}`);
    }
    if (fm.description) {
      lines.push(`description: "${fm.description}"`);
    }

    return lines.join("\n") + "\n";
  }

  /**
   * Get all CARF markdown files
   */
  private getCARFFiles(): TFile[] {
    const files: TFile[] = [];

    const processFolder = (folder: TFolder) => {
      for (const child of folder.children) {
        if (child instanceof TFile && child.extension === "md") {
          if (Document.isInCARFPath(child.path)) {
            files.push(child);
          }
        } else if (child instanceof TFolder) {
          processFolder(child);
        }
      }
    };

    const root = this.app.vault.getRoot();
    processFolder(root);

    return files;
  }
}

/**
 * Extracted footer data
 */
interface FooterData {
  raw: string;
  status?: Status;
  modules?: Module[];
  epic?: string;
  created?: string;
  updated?: string;
}
