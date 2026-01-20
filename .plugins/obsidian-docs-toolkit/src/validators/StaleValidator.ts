import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";
import { STALE_THRESHOLD_DAYS } from "../models/types";

/**
 * Validates that documents are not stale (not updated in a long time)
 */
export class StaleValidator extends LocalValidator {
  id = "stale";
  name = "Stale";
  description = "Arquivos não atualizados há >6 meses";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Skip non-CARF documents
    if (!document.isCARFDocument) {
      return issues;
    }

    // Check if document has updated date in frontmatter
    if (!document.frontmatter?.updated) {
      return issues;
    }

    const updatedDate = new Date(document.frontmatter.updated);
    const now = new Date();
    const daysSinceUpdate = Math.floor(
      (now.getTime() - updatedDate.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysSinceUpdate > STALE_THRESHOLD_DAYS) {
      const months = Math.floor(daysSinceUpdate / 30);
      issues.push(Issue.info(
        document.file,
        this.id,
        `Documento não atualizado há ${months} meses`,
        undefined,
        "Revise o documento e atualize se necessário"
      ));
    }

    return issues;
  }
}
