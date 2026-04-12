import { TFile } from "obsidian";

/**
 * Represents a link found in a document
 */
export interface DocumentLink {
  target: string;       // The link target (path or wikilink)
  line: number;         // Line number where link appears
  column: number;       // Column number where link starts
  type: "wiki" | "markdown";  // Link type
  resolved: boolean;    // Whether the link resolves to an existing file
}

/**
 * Generic frontmatter structure (any YAML is valid)
 */
export type Frontmatter = Record<string, unknown>;

/**
 * Agnostic document model - works with any documentation structure
 */
export class Document {
  file: TFile;
  frontmatter: Frontmatter | null;
  content: string;
  bodyContent: string;
  sections: Map<string, string>;
  links: DocumentLink[];
  title: string | null;

  /** Detected document type (from config) */
  detectedType: string | null = null;

  constructor(
    file: TFile,
    frontmatter: Frontmatter | null,
    content: string,
    bodyContent: string,
    sections: Map<string, string>,
    links: DocumentLink[],
    title: string | null
  ) {
    this.file = file;
    this.frontmatter = frontmatter;
    this.content = content;
    this.bodyContent = bodyContent;
    this.sections = sections;
    this.links = links;
    this.title = title;
  }

  /**
   * Get the document status from frontmatter
   */
  get status(): string {
    if (this.frontmatter && typeof this.frontmatter.status === "string") {
      return this.frontmatter.status.toLowerCase();
    }
    return "review";
  }

  /**
   * Get the document ID from frontmatter
   */
  get id(): string | null {
    if (this.frontmatter && typeof this.frontmatter.id === "string") {
      return this.frontmatter.id;
    }
    return null;
  }

  /**
   * Check if document has frontmatter
   */
  get hasFrontmatter(): boolean {
    return this.frontmatter !== null;
  }

  /**
   * Get frontmatter field value with type checking
   */
  getFrontmatterField<T>(field: string): T | undefined {
    if (!this.frontmatter) return undefined;
    return this.frontmatter[field] as T | undefined;
  }

  /**
   * Check if frontmatter field exists
   */
  hasFrontmatterField(field: string): boolean {
    return this.frontmatter !== null && field in this.frontmatter;
  }

  /**
   * Get section names (normalized for comparison)
   */
  getSectionNames(): string[] {
    return Array.from(this.sections.keys());
  }

  /**
   * Check if section exists (with normalization)
   */
  hasSection(sectionName: string): boolean {
    const normalized = Document.normalizeString(sectionName);
    return this.getSectionNames().some(
      s => Document.normalizeString(s) === normalized
    );
  }

  /**
   * Get section content by name (with normalization)
   */
  getSection(sectionName: string): string | undefined {
    const normalized = Document.normalizeString(sectionName);
    for (const [name, content] of this.sections) {
      if (Document.normalizeString(name) === normalized) {
        return content;
      }
    }
    return undefined;
  }

  /**
   * Normalize string for comparison (removes accents, lowercases, removes non-alphanumeric)
   */
  static normalizeString(str: string): string {
    return str
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "") // Remove diacritics
      .replace(/[^a-z0-9]/g, "");      // Remove non-alphanumeric
  }

  /**
   * Count words in body content (excludes frontmatter and code blocks)
   */
  countWords(): number {
    // Remove code blocks
    const withoutCode = this.bodyContent
      .replace(/```[\s\S]*?```/g, "")
      .replace(/`[^`]+`/g, "");

    // Remove links but keep text
    const withoutLinks = withoutCode
      .replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, "$2$1")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1");

    // Count words
    const words = withoutLinks.trim().split(/\s+/).filter(w => w.length > 0);
    return words.length;
  }

  /**
   * Count words in a specific section
   */
  countWordsInSection(sectionName: string): number {
    const content = this.getSection(sectionName);
    if (!content) return 0;

    const withoutCode = content
      .replace(/```[\s\S]*?```/g, "")
      .replace(/`[^`]+`/g, "");

    const words = withoutCode.trim().split(/\s+/).filter(w => w.length > 0);
    return words.length;
  }

  /**
   * Get the last modified date
   */
  get lastModified(): Date {
    return new Date(this.file.stat.mtime);
  }

  /**
   * Get days since last modification
   */
  get daysSinceModified(): number {
    const now = Date.now();
    const diff = now - this.file.stat.mtime;
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }

  /**
   * Get the updated date from frontmatter
   */
  get updatedDate(): Date | null {
    if (this.frontmatter && typeof this.frontmatter.updated === "string") {
      const date = new Date(this.frontmatter.updated);
      return isNaN(date.getTime()) ? null : date;
    }
    return null;
  }

  /**
   * Get days since last updated (from frontmatter)
   */
  get daysSinceUpdated(): number | null {
    const updated = this.updatedDate;
    if (!updated) return null;
    const now = Date.now();
    const diff = now - updated.getTime();
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }
}
