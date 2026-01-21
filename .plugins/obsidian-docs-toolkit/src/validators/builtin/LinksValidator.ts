import { TFile } from "obsidian";
import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { LocalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates that internal links resolve to existing files
 */
export class LinksValidator extends LocalValidator {
  readonly id = "broken-links";
  readonly nameKey = "validators.links.name";
  readonly descriptionKey = "validators.links.description";
  readonly defaultSeverity = Severity.ERROR;

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);

    for (const link of doc.links) {
      // Skip external links
      if (link.target.startsWith("http://") || link.target.startsWith("https://")) {
        continue;
      }

      // Skip anchor-only links
      if (link.target.startsWith("#")) {
        continue;
      }

      // Resolve the link
      const resolved = this.resolveLink(link.target, doc.file, ctx);

      if (!resolved) {
        issues.push(new Issue(
          doc.file,
          this.id,
          severity,
          "validators.links.broken",
          { target: link.target },
          link.line,
          link.column,
          "validators.links.broken_suggestion",
          { target: link.target }
        ));
      }
    }

    return issues;
  }

  /**
   * Resolve a link target to a file
   */
  private resolveLink(target: string, sourceFile: TFile, ctx: ValidatorContext): TFile | null {
    // Remove anchor from target
    const [path] = target.split("#");
    if (!path) return null; // anchor-only links handled above

    // Try to resolve as wiki link (just filename)
    const metadataCache = ctx.app.metadataCache;
    const linkedFile = metadataCache.getFirstLinkpathDest(path, sourceFile.path);

    if (linkedFile) {
      return linkedFile;
    }

    // Try to resolve as relative path
    const resolvedPath = this.resolveRelativePath(path, sourceFile);
    const file = ctx.app.vault.getAbstractFileByPath(resolvedPath);

    if (file instanceof TFile) {
      return file;
    }

    // Try adding .md extension
    if (!path.endsWith(".md")) {
      const withMd = ctx.app.vault.getAbstractFileByPath(resolvedPath + ".md");
      if (withMd instanceof TFile) {
        return withMd;
      }
    }

    return null;
  }

  /**
   * Resolve a relative path from a source file
   */
  private resolveRelativePath(path: string, sourceFile: TFile): string {
    if (path.startsWith("/")) {
      // Absolute path from vault root
      return path.slice(1);
    }

    // Handle url-encoded paths
    const decodedPath = decodeURIComponent(path);

    // Relative path from source file's folder
    const sourceDir = sourceFile.parent?.path || "";

    if (decodedPath.startsWith("./")) {
      return sourceDir ? `${sourceDir}/${decodedPath.slice(2)}` : decodedPath.slice(2);
    }

    if (decodedPath.startsWith("../")) {
      // Navigate up directories
      const parts = sourceDir.split("/");
      let relativeParts = decodedPath.split("/");
      let finalParts = [...parts];

      while (relativeParts[0] === "..") {
        finalParts.pop();
        relativeParts.shift();
      }

      return [...finalParts, ...relativeParts].join("/");
    }

    // Assume it's a path relative to source directory
    return sourceDir ? `${sourceDir}/${decodedPath}` : decodedPath;
  }
}
