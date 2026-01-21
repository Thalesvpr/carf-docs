import { App, TFile, parseYaml } from "obsidian";
import { Document, DocumentLink, Frontmatter } from "../core/Document";

/**
 * Service for parsing markdown documents into Document objects
 */
export class DocumentParser {
  private app: App;

  constructor(app: App) {
    this.app = app;
  }

  /**
   * Parse a file into a Document object
   */
  async parse(file: TFile): Promise<Document> {
    const content = await this.app.vault.read(file);
    const frontmatter = this.parseFrontmatter(content);
    const bodyContent = this.getBodyContent(content);
    const sections = this.parseSections(bodyContent);
    const links = this.parseLinks(bodyContent);
    const title = this.parseTitle(bodyContent);

    return new Document(
      file,
      frontmatter,
      content,
      bodyContent,
      sections,
      links,
      title
    );
  }

  /**
   * Parse YAML frontmatter from content
   */
  private parseFrontmatter(content: string): Frontmatter | null {
    const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!match) return null;

    try {
      const yaml = parseYaml(match[1]);
      if (!yaml || typeof yaml !== "object") return null;
      return yaml as Frontmatter;
    } catch {
      return null;
    }
  }

  /**
   * Get body content (without frontmatter)
   */
  private getBodyContent(content: string): string {
    return content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n*/, "");
  }

  /**
   * Parse sections from body content (## and ### headers)
   */
  private parseSections(content: string): Map<string, string> {
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

    if (currentSection) {
      sections.set(currentSection, currentContent.join("\n").trim());
    }

    return sections;
  }

  /**
   * Parse links from body content
   */
  private parseLinks(content: string): DocumentLink[] {
    const links: DocumentLink[] = [];
    const lines = content.split("\n");

    for (let lineNum = 0; lineNum < lines.length; lineNum++) {
      const line = lines[lineNum];

      // Wiki links [[target]] or [[target|alias]]
      const wikiLinkRegex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
      let match;
      while ((match = wikiLinkRegex.exec(line)) !== null) {
        links.push({
          target: match[1],
          line: lineNum + 1,
          column: match.index,
          type: "wiki",
          resolved: false
        });
      }

      // Markdown links [text](target)
      const mdLinkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
      while ((match = mdLinkRegex.exec(line)) !== null) {
        const target = match[2];
        // Skip external links
        if (!target.startsWith("http://") && !target.startsWith("https://")) {
          links.push({
            target,
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
   * Parse the main title (# header)
   */
  private parseTitle(content: string): string | null {
    const match = content.match(/^#\s+(.+)$/m);
    return match ? match[1].trim() : null;
  }
}
