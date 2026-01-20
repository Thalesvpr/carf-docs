import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";
import { REQUIRED_SECTIONS, DocType } from "../models/types";

/**
 * Validates that documents have required sections based on their type
 */
export class StructureValidator extends LocalValidator {
  id = "structure";
  name = "Structure";
  description = "Seções obrigatórias por tipo (## Critérios, etc)";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Skip non-CARF documents
    if (!document.isCARFDocument) {
      return issues;
    }

    const requiredSections = REQUIRED_SECTIONS[document.type];
    if (!requiredSections || requiredSections.length === 0) {
      return issues;
    }

    const existingSections = Array.from(document.sections.keys())
      .map(s => this.normalizeSection(s));

    for (const required of requiredSections) {
      const normalizedRequired = this.normalizeSection(required);
      const found = existingSections.some(s => s.includes(normalizedRequired) || normalizedRequired.includes(s));

      if (!found) {
        issues.push(Issue.warning(
          document.file,
          this.id,
          `Seção obrigatória '${required}' não encontrada`,
          undefined,
          `Adicione a seção '## ${required}' ao documento`
        ));
      }
    }

    return issues;
  }

  /**
   * Normalize section name for comparison
   */
  private normalizeSection(section: string): string {
    return section
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "") // Remove accents
      .replace(/[^a-z0-9]/g, ""); // Remove non-alphanumeric
  }
}
