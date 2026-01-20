import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";
import { DocType, NAMING_PATTERNS } from "../models/types";

/**
 * Validates that files follow the correct naming convention
 */
export class NamingValidator extends LocalValidator {
  id = "naming";
  name = "Naming";
  description = "Arquivos sem prefixo numérico correto";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Skip README files
    if (document.file.name === "README.md") {
      return issues;
    }

    // Check if file is in a CARF path that requires naming convention
    const path = document.file.path;
    if (!this.requiresNamingConvention(path)) {
      return issues;
    }

    // Determine expected type from path
    const expectedType = this.getExpectedTypeFromPath(path);
    if (!expectedType) {
      return issues;
    }

    // Check naming pattern
    const pattern = NAMING_PATTERNS[expectedType];
    if (pattern && !pattern.test(document.file.name)) {
      const expectedFormat = this.getExpectedFormat(expectedType);
      issues.push(Issue.error(
        document.file,
        this.id,
        `Nome do arquivo não segue o padrão esperado`,
        undefined,
        `Formato esperado: ${expectedFormat}`
      ));
    }

    return issues;
  }

  /**
   * Check if path requires naming convention
   */
  private requiresNamingConvention(path: string): boolean {
    const conventionPaths = [
      "CENTRAL/REQUIREMENTS/FUNCTIONAL",
      "CENTRAL/REQUIREMENTS/NON-FUNCTIONAL",
      "CENTRAL/REQUIREMENTS/USE-CASES",
      "CENTRAL/REQUIREMENTS/USER-STORIES",
      "PROJECTS/"
    ];

    return conventionPaths.some(p => path.includes(p));
  }

  /**
   * Get expected document type from path
   */
  private getExpectedTypeFromPath(path: string): DocType | null {
    if (path.includes("/FUNCTIONAL/")) return DocType.RF;
    if (path.includes("/NON-FUNCTIONAL/")) return DocType.RNF;
    if (path.includes("/USE-CASES/")) return DocType.UC;
    if (path.includes("/USER-STORIES/")) return DocType.US;
    if (path.includes("/ARCHITECTURE/") || path.includes("/DOCS/")) return DocType.ARCH;
    return null;
  }

  /**
   * Get expected file name format
   */
  private getExpectedFormat(type: DocType): string {
    switch (type) {
      case DocType.RF:
        return "RF-XXX-nome-do-requisito.md";
      case DocType.RNF:
        return "RNF-XXX-nome-do-requisito.md";
      case DocType.UC:
        return "XX-UC-XXX-nome-do-caso.md ou UC-XXX-nome-do-caso.md";
      case DocType.US:
        return "US-XXX-nome-da-historia.md";
      case DocType.ARCH:
        return "XX-nome-do-documento.md";
      default:
        return "nome-do-arquivo.md";
    }
  }
}
