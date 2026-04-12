import { App, TFile, normalizePath } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";

/**
 * Validates that all links in a document point to existing files
 */
export class BrokenLinksValidator extends LocalValidator {
  id = "broken-links";
  name = "Broken Links";
  description = "Links que apontam para arquivos inexistentes";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    for (const link of document.links) {
      const resolved = this.resolveLink(link.target, document.file, app);

      if (!resolved) {
        issues.push(Issue.error(
          document.file,
          this.id,
          `Link "${link.target}" não existe`,
          link.line,
          "Verifique se o caminho está correto ou crie o arquivo"
        ));
      }
    }

    return issues;
  }

  /**
   * Resolve a link to a file
   */
  private resolveLink(target: string, sourceFile: TFile, app: App): TFile | null {
    // Handle wiki links
    if (!target.includes("/") && !target.includes("\\")) {
      // Simple wiki link - search in vault
      const files = app.vault.getMarkdownFiles();
      const targetWithExt = target.endsWith(".md") ? target : `${target}.md`;

      for (const file of files) {
        if (file.name === targetWithExt || file.basename === target) {
          return file;
        }
      }
      return null;
    }

    // Handle relative paths
    let resolvedPath: string;

    if (target.startsWith("./") || target.startsWith("../")) {
      // Relative to current file
      const parentPath = sourceFile.parent?.path || "";
      resolvedPath = this.resolvePath(parentPath, target);
    } else if (target.startsWith("/")) {
      // Absolute from vault root
      resolvedPath = target.substring(1);
    } else {
      // Relative to current file without ./
      const parentPath = sourceFile.parent?.path || "";
      resolvedPath = this.resolvePath(parentPath, "./" + target);
    }

    // Add .md extension if missing
    if (!resolvedPath.endsWith(".md")) {
      resolvedPath += ".md";
    }

    resolvedPath = normalizePath(resolvedPath);
    return app.vault.getAbstractFileByPath(resolvedPath) as TFile | null;
  }

  /**
   * Resolve a relative path from a base path
   */
  private resolvePath(basePath: string, relativePath: string): string {
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
