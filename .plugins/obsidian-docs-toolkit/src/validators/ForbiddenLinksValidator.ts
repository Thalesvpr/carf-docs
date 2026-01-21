import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";

/**
 * Validator that checks for forbidden internal links.
 *
 * Rules:
 * 1. Non-README files: NO internal links allowed (wikilinks or markdown links)
 * 2. README files: Links ONLY allowed within CARF-INDEX markers
 *
 * External links (http/https) are always allowed.
 */
export class ForbiddenLinksValidator extends LocalValidator {
  id = "forbidden-links";
  name = "Forbidden Links";
  description = "Links internos são permitidos apenas em README (seção de índice)";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    const isReadme = document.file.name === "README.md";

    for (const link of document.links) {
      // Skip external links (http/https) - those are allowed anywhere
      if (link.target.startsWith("http://") || link.target.startsWith("https://")) {
        continue;
      }

      if (!isReadme) {
        // Non-README files: NO internal links allowed
        issues.push(Issue.error(
          document.file,
          this.id,
          `Link interno "${link.target}" não permitido`,
          link.line,
          "Links internos só são permitidos em README.md"
        ));
      } else {
        // README files: links only allowed inside index section
        const content = document.content;
        const indexStart = content.indexOf("<!-- CARF-INDEX-START -->");
        const indexEnd = content.indexOf("<!-- CARF-INDEX-END -->");
        const hasValidSection = indexStart !== -1 && indexEnd !== -1 && indexStart < indexEnd;

        const linkPosition = this.getLinkPosition(content, link.line);
        const isOutsideSection = !hasValidSection ||
          linkPosition < indexStart ||
          linkPosition > indexEnd;

        if (isOutsideSection) {
          issues.push(Issue.error(
            document.file,
            this.id,
            `Link "${link.target}" fora da seção de índice`,
            link.line,
            "Use 'Regenerate README index' para gerar links automaticamente"
          ));
        }
      }
    }

    return issues;
  }

  /**
   * Get the character position for a given line number
   */
  private getLinkPosition(content: string, line: number): number {
    const lines = content.split("\n");
    let pos = 0;
    for (let i = 0; i < line - 1 && i < lines.length; i++) {
      pos += lines[i].length + 1; // +1 for newline character
    }
    return pos;
  }
}
