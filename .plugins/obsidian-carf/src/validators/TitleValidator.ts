import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";
import { TITLE_PATTERNS, DocType } from "../models/types";

/**
 * Validates that document titles follow the expected pattern
 */
export class TitleValidator extends LocalValidator {
  id = "title";
  name = "Title";
  description = "H1 deve seguir padrão (# RF-001: Título)";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Skip non-CARF documents
    if (!document.isCARFDocument) {
      return issues;
    }

    // Check if title exists
    if (!document.title) {
      issues.push(Issue.error(
        document.file,
        this.id,
        "Documento não possui título (H1)",
        undefined,
        "Adicione um título no formato '# ID: Título'"
      ));
      return issues;
    }

    // Check title pattern
    const pattern = TITLE_PATTERNS[document.type];
    if (pattern && !pattern.test(`# ${document.title}`)) {
      const expectedFormat = this.getExpectedFormat(document.type);
      issues.push(Issue.error(
        document.file,
        this.id,
        `Título não segue o padrão esperado`,
        this.findTitleLine(document.content),
        `Formato esperado: ${expectedFormat}`
      ));
    }

    // Check if title ID matches frontmatter ID
    if (document.frontmatter?.id) {
      const titleId = this.extractIdFromTitle(document.title);
      if (titleId && titleId !== document.frontmatter.id) {
        issues.push(Issue.warning(
          document.file,
          this.id,
          `ID no título '${titleId}' não corresponde ao frontmatter '${document.frontmatter.id}'`,
          this.findTitleLine(document.content),
          `Corrija o ID no título para '${document.frontmatter.id}'`
        ));
      }
    }

    return issues;
  }

  /**
   * Get expected title format for a document type
   */
  private getExpectedFormat(type: DocType): string {
    switch (type) {
      case DocType.RF:
        return "# RF-XXX: Título do Requisito";
      case DocType.RNF:
        return "# RNF-XXX: Título do Requisito";
      case DocType.UC:
        return "# UC-XXX: Título do Caso de Uso";
      case DocType.US:
        return "# US-XXX: Título da User Story";
      default:
        return "# Título";
    }
  }

  /**
   * Extract ID from title
   */
  private extractIdFromTitle(title: string): string | null {
    const match = title.match(/^(RF|RNF|UC|US)-\d{3}/);
    return match ? match[0] : null;
  }

  /**
   * Find the line number of the title
   */
  private findTitleLine(content: string): number {
    const lines = content.split("\n");
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith("# ")) {
        return i + 1;
      }
    }
    return 1;
  }
}
