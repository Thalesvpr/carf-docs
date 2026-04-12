import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";
import { DocType, VALID_MODULES } from "../models/types";

/**
 * Validates that CARF documents have valid frontmatter
 */
export class FrontmatterValidator extends LocalValidator {
  id = "frontmatter";
  name = "Frontmatter";
  description = "Campos obrigatórios no frontmatter";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Skip non-CARF documents
    if (!document.isCARFDocument) {
      return issues;
    }

    // Check if frontmatter exists
    if (!document.frontmatter) {
      issues.push(Issue.error(
        document.file,
        this.id,
        "Arquivo não possui frontmatter YAML",
        1,
        "Execute 'Docs Toolkit: Init Metadata' para criar o frontmatter"
      ));
      return issues;
    }

    const fm = document.frontmatter;

    // Check required fields
    if (!fm.id) {
      issues.push(Issue.error(
        document.file,
        this.id,
        "Campo 'id' obrigatório no frontmatter",
        1,
        "Adicione o campo 'id' com o identificador do documento (ex: RF-001)"
      ));
    }

    if (!fm.type) {
      issues.push(Issue.error(
        document.file,
        this.id,
        "Campo 'type' obrigatório no frontmatter",
        1,
        "Adicione o campo 'type' com o tipo do documento (RF, RNF, UC, US)"
      ));
    }

    if (!fm.status) {
      issues.push(Issue.error(
        document.file,
        this.id,
        "Campo 'status' obrigatório no frontmatter",
        1,
        "Adicione o campo 'status' (review, approved, rejected)"
      ));
    }

    // Validate modules
    if (!fm.modules || fm.modules.length === 0) {
      issues.push(Issue.warning(
        document.file,
        this.id,
        "Campo 'modules' está vazio",
        1,
        `Adicione os módulos relacionados: ${VALID_MODULES.join(", ")}`
      ));
    } else {
      for (const module of fm.modules) {
        if (!VALID_MODULES.includes(module as any)) {
          issues.push(Issue.warning(
            document.file,
            this.id,
            `Módulo '${module}' não é válido`,
            1,
            `Módulos válidos: ${VALID_MODULES.join(", ")}`
          ));
        }
      }
    }

    // Validate ID matches filename
    const expectedId = this.extractIdFromFilename(document.file.name);
    if (expectedId && fm.id !== expectedId) {
      issues.push(Issue.warning(
        document.file,
        this.id,
        `ID no frontmatter '${fm.id}' não corresponde ao nome do arquivo '${expectedId}'`,
        1,
        `Corrija o ID para '${expectedId}'`
      ));
    }

    // Validate type matches filename
    const expectedType = Document.inferTypeFromFilename(document.file.name);
    if (expectedType !== DocType.OTHER && fm.type !== expectedType) {
      issues.push(Issue.warning(
        document.file,
        this.id,
        `Tipo no frontmatter '${fm.type}' não corresponde ao nome do arquivo`,
        1,
        `Corrija o tipo para '${expectedType}'`
      ));
    }

    return issues;
  }

  /**
   * Extract ID from filename
   */
  private extractIdFromFilename(filename: string): string | null {
    const match = filename.match(/^(RF|RNF|UC|US)-\d{3}/);
    return match ? match[0] : null;
  }
}
