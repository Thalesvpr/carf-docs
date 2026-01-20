import { TFile } from "obsidian";
import { DocType, Status, Module, CARFFrontmatter } from "./types";

/**
 * Represents a parsed CARF document with its metadata and content
 */
export class Document {
  file: TFile;
  frontmatter: CARFFrontmatter | null;
  content: string;
  sections: Map<string, string>;
  links: DocumentLink[];
  title: string | null;

  constructor(
    file: TFile,
    frontmatter: CARFFrontmatter | null,
    content: string,
    sections: Map<string, string>,
    links: DocumentLink[],
    title: string | null
  ) {
    this.file = file;
    this.frontmatter = frontmatter;
    this.content = content;
    this.sections = sections;
    this.links = links;
    this.title = title;
  }

  /**
   * Get the document type from frontmatter or infer from filename
   */
  get type(): DocType {
    if (this.frontmatter?.type) {
      return this.frontmatter.type;
    }
    return Document.inferTypeFromFilename(this.file.name);
  }

  /**
   * Get the document ID
   */
  get id(): string | null {
    return this.frontmatter?.id || this.extractIdFromFilename();
  }

  /**
   * Get the document status
   */
  get status(): Status {
    return this.frontmatter?.status || Status.REVIEW;
  }

  /**
   * Check if document has valid frontmatter
   */
  get hasValidFrontmatter(): boolean {
    return this.frontmatter !== null;
  }

  /**
   * Check if document is a CARF document (RF, RNF, UC, US)
   */
  get isCARFDocument(): boolean {
    const carfTypes = [DocType.RF, DocType.RNF, DocType.UC, DocType.US];
    return carfTypes.includes(this.type);
  }

  /**
   * Extract ID from filename (e.g., "RF-001-titulo.md" -> "RF-001")
   */
  private extractIdFromFilename(): string | null {
    const match = this.file.name.match(/^(RF|RNF|UC|US)-\d{3}/);
    return match ? match[0] : null;
  }

  /**
   * Infer document type from filename
   */
  static inferTypeFromFilename(filename: string): DocType {
    if (filename === "README.md") return DocType.README;
    if (filename.startsWith("RF-")) return DocType.RF;
    if (filename.startsWith("RNF-")) return DocType.RNF;
    if (/^(\d{2}-)?UC-/.test(filename)) return DocType.UC;
    if (filename.startsWith("US-")) return DocType.US;
    if (/^\d{2}-.+\.md$/.test(filename)) return DocType.ARCH;
    return DocType.OTHER;
  }

  /**
   * Check if file is in a CARF path
   */
  static isInCARFPath(path: string): boolean {
    return path.startsWith("CENTRAL/") || path.startsWith("PROJECTS/");
  }
}

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
