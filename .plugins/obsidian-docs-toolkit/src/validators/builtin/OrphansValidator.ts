import { TFile } from "obsidian";
import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { GlobalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates that documents are linked from at least one other document
 */
export class OrphansValidator extends GlobalValidator {
  readonly id = "orphans";
  readonly nameKey = "validators.orphans.name";
  readonly descriptionKey = "validators.orphans.description";
  readonly defaultSeverity = Severity.WARNING;

  async validateAll(docs: Document[], ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);

    // Get exclude patterns from config
    const validatorConfig = ctx.config.validators[this.id];
    const excludePatterns = (validatorConfig?.exclude as string[]) || [];

    // Build a set of all files that are linked to
    const linkedFiles = new Set<string>();

    for (const doc of docs) {
      for (const link of doc.links) {
        // Resolve the link
        const resolved = this.resolveLink(link.target, doc.file, ctx);
        if (resolved) {
          linkedFiles.add(resolved.path);
        }
      }
    }

    // Check each document
    for (const doc of docs) {
      // Skip excluded files
      if (this.isExcluded(doc.file.path, excludePatterns)) {
        continue;
      }

      // Skip README files (they're often index files)
      if (doc.file.name === "README.md") {
        continue;
      }

      // Check if this file is linked from anywhere
      if (!linkedFiles.has(doc.file.path)) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.orphans.not_linked",
          { filename: doc.file.name },
          undefined,
          null,
          "validators.orphans.not_linked_suggestion"
        ));
      }
    }

    return issues;
  }

  /**
   * Check if a path matches any exclude pattern
   */
  private isExcluded(path: string, patterns: string[]): boolean {
    for (const pattern of patterns) {
      // Simple glob matching
      const regex = pattern
        .replace(/\*\*/g, ".*")
        .replace(/\*/g, "[^/]*");

      if (new RegExp(regex).test(path)) {
        return true;
      }
    }
    return false;
  }

  /**
   * Resolve a link target to a file
   */
  private resolveLink(target: string, sourceFile: TFile, ctx: ValidatorContext): TFile | null {
    // Remove anchor from target
    const [path] = target.split("#");
    if (!path) return null;

    // Skip external links
    if (path.startsWith("http://") || path.startsWith("https://")) {
      return null;
    }

    // Try to resolve as wiki link
    const metadataCache = ctx.app.metadataCache;
    const linkedFile = metadataCache.getFirstLinkpathDest(path, sourceFile.path);

    if (linkedFile) {
      return linkedFile;
    }

    // Try direct path resolution
    let resolvedPath = path;
    if (path.startsWith("./") || path.startsWith("../")) {
      const sourceDir = sourceFile.parent?.path || "";
      resolvedPath = this.resolvePath(path, sourceDir);
    }

    const file = ctx.app.vault.getAbstractFileByPath(resolvedPath);
    if (file instanceof TFile) {
      return file;
    }

    // Try adding .md extension
    if (!resolvedPath.endsWith(".md")) {
      const withMd = ctx.app.vault.getAbstractFileByPath(resolvedPath + ".md");
      if (withMd instanceof TFile) {
        return withMd;
      }
    }

    return null;
  }

  /**
   * Resolve a relative path
   */
  private resolvePath(path: string, sourceDir: string): string {
    const decodedPath = decodeURIComponent(path);

    if (decodedPath.startsWith("./")) {
      return sourceDir ? `${sourceDir}/${decodedPath.slice(2)}` : decodedPath.slice(2);
    }

    if (decodedPath.startsWith("../")) {
      const parts = sourceDir.split("/");
      let relativeParts = decodedPath.split("/");
      let finalParts = [...parts];

      while (relativeParts[0] === "..") {
        finalParts.pop();
        relativeParts.shift();
      }

      return [...finalParts, ...relativeParts].join("/");
    }

    return decodedPath;
  }
}
