import { TFolder } from "obsidian";
import { Document } from "../../core/Document";
import { Issue } from "../../core/Issue";
import { Severity } from "../../core/Severity";
import { GlobalValidator, ValidatorContext, getConfiguredSeverity } from "../base/Validator";

/**
 * Validates that there are no empty folders in the documentation
 */
export class EmptyFoldersValidator extends GlobalValidator {
  readonly id = "empty-folders";
  readonly nameKey = "validators.emptyFolders.name";
  readonly descriptionKey = "validators.emptyFolders.description";
  readonly defaultSeverity = Severity.INFO;

  async validateAll(docs: Document[], ctx: ValidatorContext): Promise<Issue[]> {
    const issues: Issue[] = [];
    const severity = getConfiguredSeverity(this.id, ctx.config, this.defaultSeverity);

    // Get all folders in the vault
    const folders = this.getAllFolders(ctx);

    // Get all folder paths that contain documents
    const foldersWithDocs = new Set<string>();
    for (const doc of docs) {
      if (doc.file.parent) {
        // Add this folder and all parent folders
        let current = doc.file.parent;
        while (current) {
          foldersWithDocs.add(current.path);
          current = current.parent as TFolder;
        }
      }
    }

    // Check each folder
    for (const folder of folders) {
      // Skip excluded paths
      if (this.isExcludedPath(folder.path, ctx.config.paths.exclude)) {
        continue;
      }

      // Skip if folder has markdown files
      if (foldersWithDocs.has(folder.path)) {
        continue;
      }

      // Check if folder has any markdown files (including in subfolders)
      if (!this.hasMarkdownFiles(folder)) {
        // Create a pseudo-issue (folder doesn't have a TFile, so we use a special approach)
        // We'll report it on the parent folder's README or first doc
        const parentDoc = this.findParentDoc(folder, docs);

        if (parentDoc) {
          issues.push(new Issue(
            parentDoc.file,
            this.id,
            severity,
            "validators.emptyFolders.empty",
            { folder: folder.path },
            undefined,
            null,
            "validators.emptyFolders.empty_suggestion"
          ));
        }
      }
    }

    return issues;
  }

  /**
   * Get all folders in the vault
   */
  private getAllFolders(ctx: ValidatorContext): TFolder[] {
    const folders: TFolder[] = [];

    const traverse = (folder: TFolder) => {
      folders.push(folder);
      for (const child of folder.children) {
        if (child instanceof TFolder) {
          traverse(child);
        }
      }
    };

    const root = ctx.app.vault.getRoot();
    for (const child of root.children) {
      if (child instanceof TFolder) {
        traverse(child);
      }
    }

    return folders;
  }

  /**
   * Check if a path should be excluded
   */
  private isExcludedPath(path: string, excludePatterns: string[]): boolean {
    for (const pattern of excludePatterns) {
      const regex = pattern
        .replace(/\*\*/g, ".*")
        .replace(/\*/g, "[^/]*");

      if (new RegExp(`^${regex}`).test(path)) {
        return true;
      }
    }

    // Also exclude common system folders
    const systemFolders = [".obsidian", ".git", "node_modules", ".plugins"];
    for (const sys of systemFolders) {
      if (path.startsWith(sys)) {
        return true;
      }
    }

    return false;
  }

  /**
   * Check if a folder has any markdown files (recursively)
   */
  private hasMarkdownFiles(folder: TFolder): boolean {
    for (const child of folder.children) {
      if (child instanceof TFolder) {
        if (this.hasMarkdownFiles(child)) {
          return true;
        }
      } else if (child.name.endsWith(".md")) {
        return true;
      }
    }
    return false;
  }

  /**
   * Find a document in the parent folder to attach the issue to
   */
  private findParentDoc(folder: TFolder, docs: Document[]): Document | null {
    if (!folder.parent) return null;

    // Look for README in parent
    for (const doc of docs) {
      if (doc.file.parent?.path === folder.parent.path && doc.file.name === "README.md") {
        return doc;
      }
    }

    // Or any doc in parent
    for (const doc of docs) {
      if (doc.file.parent?.path === folder.parent.path) {
        return doc;
      }
    }

    // Recurse to grandparent
    return this.findParentDoc(folder.parent as TFolder, docs);
  }
}
