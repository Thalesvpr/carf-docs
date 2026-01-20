import { App } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { GlobalValidator } from "./Validator";
import { DocType } from "../models/types";

/**
 * Validates that CARF documents are not orphaned (have at least one incoming link)
 */
export class OrphansValidator extends GlobalValidator {
  id = "orphans";
  name = "Orphans";
  description = "Arquivos sem nenhum link apontando para eles";

  async validateAll(documents: Document[], app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Build a map of all files that are linked to
    const linkedFiles = new Set<string>();

    for (const doc of documents) {
      for (const link of doc.links) {
        // Normalize the link target
        const resolved = this.resolveLink(link.target, doc, documents);
        if (resolved) {
          linkedFiles.add(resolved.file.path);
        }
      }
    }

    // Check each CARF document for incoming links
    for (const doc of documents) {
      // Skip non-CARF documents and READMEs
      if (!doc.isCARFDocument) continue;
      if (doc.type === DocType.README) continue;

      if (!linkedFiles.has(doc.file.path)) {
        issues.push(Issue.warning(
          doc.file,
          this.id,
          "Nenhum arquivo aponta para este documento",
          undefined,
          "Adicione um link para este documento em outro arquivo relacionado"
        ));
      }
    }

    return issues;
  }

  /**
   * Resolve a link target to a document
   */
  private resolveLink(target: string, sourceDoc: Document, documents: Document[]): Document | null {
    // Normalize target
    const targetName = target.replace(/\.md$/, "");

    for (const doc of documents) {
      // Match by full path
      if (doc.file.path === target || doc.file.path === `${target}.md`) {
        return doc;
      }

      // Match by basename
      if (doc.file.basename === targetName) {
        return doc;
      }

      // Match by relative path from source
      const sourcePath = sourceDoc.file.parent?.path || "";
      const resolvedPath = this.resolvePath(sourcePath, target);
      if (doc.file.path === resolvedPath || doc.file.path === `${resolvedPath}.md`) {
        return doc;
      }
    }

    return null;
  }

  /**
   * Resolve a relative path from a base path
   */
  private resolvePath(basePath: string, relativePath: string): string {
    if (!relativePath.startsWith("./") && !relativePath.startsWith("../")) {
      return relativePath;
    }

    const parts = basePath.split("/").filter(p => p);
    const relParts = relativePath.split("/");

    for (const part of relParts) {
      if (part === "." || part === "") {
        continue;
      } else if (part === "..") {
        parts.pop();
      } else {
        parts.push(part);
      }
    }

    return parts.join("/");
  }
}
