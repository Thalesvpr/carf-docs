import { App, TFile, parseYaml, stringifyYaml } from "obsidian";
import { CARFFrontmatter, DocType, Status, Module, VALID_MODULES } from "../models/types";
import { Document, DocumentLink } from "../models/Document";

/**
 * Service for managing YAML frontmatter in CARF documents
 */
export class MetadataService {
  private app: App;

  constructor(app: App) {
    this.app = app;
  }

  /**
   * Parse a file into a Document object
   */
  async parseDocument(file: TFile): Promise<Document> {
    const content = await this.app.vault.read(file);
    const frontmatter = this.parseFrontmatter(content);
    const bodyContent = this.getBodyContent(content);
    const sections = this.parseSections(bodyContent);
    const links = this.parseLinks(bodyContent);
    const title = this.parseTitle(bodyContent);

    return new Document(file, frontmatter, content, sections, links, title);
  }

  /**
   * Parse YAML frontmatter from content
   */
  parseFrontmatter(content: string): CARFFrontmatter | null {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;

    try {
      const yaml = parseYaml(match[1]);
      if (!yaml) return null;

      // Validate and normalize the frontmatter
      return this.normalizeFrontmatter(yaml);
    } catch (e) {
      console.error("Failed to parse frontmatter:", e);
      return null;
    }
  }

  /**
   * Normalize raw YAML to CARFFrontmatter
   */
  private normalizeFrontmatter(yaml: any): CARFFrontmatter | null {
    // Validate required fields
    if (!yaml.id || !yaml.type || !yaml.status) {
      return null;
    }

    // Normalize type
    const type = yaml.type.toUpperCase() as DocType;
    if (!Object.values(DocType).includes(type)) {
      return null;
    }

    // Normalize status
    const status = yaml.status.toLowerCase() as Status;
    if (!Object.values(Status).includes(status)) {
      return null;
    }

    // Normalize modules
    let modules: Module[] = [];
    if (Array.isArray(yaml.modules)) {
      modules = yaml.modules
        .map((m: string) => m.toUpperCase())
        .filter((m: string) => VALID_MODULES.includes(m as Module)) as Module[];
    }

    return {
      id: yaml.id,
      type: type,
      modules: modules,
      epic: yaml.epic || undefined,
      status: status,
      created: yaml.created || this.formatDate(new Date()),
      updated: yaml.updated || this.formatDate(new Date())
    };
  }

  /**
   * Get body content without frontmatter
   */
  getBodyContent(content: string): string {
    return content.replace(/^---\n[\s\S]*?\n---\n*/, "");
  }

  /**
   * Parse sections from body content
   */
  parseSections(content: string): Map<string, string> {
    const sections = new Map<string, string>();
    const lines = content.split("\n");
    let currentSection = "";
    let currentContent: string[] = [];

    for (const line of lines) {
      const headerMatch = line.match(/^#{2,3}\s+(.+)$/);
      if (headerMatch) {
        if (currentSection) {
          sections.set(currentSection, currentContent.join("\n").trim());
        }
        currentSection = headerMatch[1].trim();
        currentContent = [];
      } else if (currentSection) {
        currentContent.push(line);
      }
    }

    // Save last section
    if (currentSection) {
      sections.set(currentSection, currentContent.join("\n").trim());
    }

    return sections;
  }

  /**
   * Parse links from content
   */
  parseLinks(content: string): DocumentLink[] {
    const links: DocumentLink[] = [];
    const lines = content.split("\n");

    for (let lineNum = 0; lineNum < lines.length; lineNum++) {
      const line = lines[lineNum];

      // Wiki links: [[target]] or [[target|alias]]
      const wikiLinkRegex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
      let match;
      while ((match = wikiLinkRegex.exec(line)) !== null) {
        links.push({
          target: match[1],
          line: lineNum + 1,
          column: match.index,
          type: "wiki",
          resolved: false // Will be resolved later
        });
      }

      // Markdown links: [text](target)
      const mdLinkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
      while ((match = mdLinkRegex.exec(line)) !== null) {
        const target = match[2];
        // Skip external links
        if (!target.startsWith("http://") && !target.startsWith("https://")) {
          links.push({
            target: target,
            line: lineNum + 1,
            column: match.index,
            type: "markdown",
            resolved: false
          });
        }
      }
    }

    return links;
  }

  /**
   * Parse title (H1) from content
   */
  parseTitle(content: string): string | null {
    const match = content.match(/^#\s+(.+)$/m);
    return match ? match[1].trim() : null;
  }

  /**
   * Create default frontmatter for a new document
   */
  createDefaultFrontmatter(file: TFile): CARFFrontmatter {
    const type = Document.inferTypeFromFilename(file.name);
    const id = this.extractIdFromFilename(file.name) || "";
    const now = this.formatDate(new Date());

    return {
      id: id,
      type: type,
      modules: [],
      epic: "",
      status: Status.REVIEW,
      created: now,
      updated: now
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
   * Format date as YYYY-MM-DD
   */
  formatDate(date: Date): string {
    return date.toISOString().split("T")[0];
  }

  /**
   * Add or update frontmatter in a file
   */
  async setFrontmatter(file: TFile, frontmatter: CARFFrontmatter): Promise<void> {
    const content = await this.app.vault.read(file);
    const bodyContent = this.getBodyContent(content);

    const yamlStr = stringifyYaml(frontmatter);
    const newContent = `---\n${yamlStr}---\n\n${bodyContent}`;

    await this.app.vault.modify(file, newContent);
  }

  /**
   * Update a single field in frontmatter
   */
  async updateFrontmatterField<K extends keyof CARFFrontmatter>(
    file: TFile,
    field: K,
    value: CARFFrontmatter[K]
  ): Promise<void> {
    const content = await this.app.vault.read(file);
    const frontmatter = this.parseFrontmatter(content);

    if (!frontmatter) {
      throw new Error("File has no valid frontmatter");
    }

    frontmatter[field] = value;
    await this.setFrontmatter(file, frontmatter);
  }

  /**
   * Update the 'updated' timestamp
   */
  async updateTimestamp(file: TFile): Promise<void> {
    const content = await this.app.vault.read(file);
    const frontmatter = this.parseFrontmatter(content);

    if (frontmatter) {
      frontmatter.updated = this.formatDate(new Date());
      await this.setFrontmatter(file, frontmatter);
    }
  }

  /**
   * Set document status
   */
  async setStatus(file: TFile, status: Status): Promise<void> {
    await this.updateFrontmatterField(file, "status", status);
    await this.updateFrontmatterField(file, "updated", this.formatDate(new Date()));
  }

  /**
   * Check if file has frontmatter
   */
  async hasFrontmatter(file: TFile): Promise<boolean> {
    const content = await this.app.vault.read(file);
    return this.parseFrontmatter(content) !== null;
  }

  /**
   * Initialize frontmatter for a file that doesn't have it
   */
  async initFrontmatter(file: TFile): Promise<CARFFrontmatter> {
    const frontmatter = this.createDefaultFrontmatter(file);
    await this.setFrontmatter(file, frontmatter);
    return frontmatter;
  }
}
