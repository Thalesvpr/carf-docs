import { App, TFolder, TFile } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { GlobalValidator } from "./Validator";

/**
 * Validates that folders with README files have actual content
 */
export class EmptyFoldersValidator extends GlobalValidator {
  id = "empty-folders";
  name = "Empty Folders";
  description = "Pastas com README mas sem conteúdo";

  async validateAll(documents: Document[], app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Build a map of folders to their documents
    const folderDocs = new Map<string, Document[]>();

    for (const doc of documents) {
      const folderPath = doc.file.parent?.path || "";
      if (!folderDocs.has(folderPath)) {
        folderDocs.set(folderPath, []);
      }
      folderDocs.get(folderPath)!.push(doc);
    }

    // Check each folder
    for (const [folderPath, docs] of folderDocs) {
      // Skip root folder
      if (!folderPath) continue;

      // Check if folder is in CARF paths
      if (!folderPath.startsWith("CENTRAL/") && !folderPath.startsWith("PROJECTS/")) {
        continue;
      }

      // Check if folder has a README
      const readme = docs.find(d => d.file.name === "README.md");
      if (!readme) continue;

      // Count non-README markdown files
      const contentFiles = docs.filter(d => d.file.name !== "README.md");

      // Check for subfolders with content
      const folder = app.vault.getAbstractFileByPath(folderPath);
      const hasSubfolders = folder instanceof TFolder &&
        folder.children.some(c => c instanceof TFolder);

      if (contentFiles.length === 0 && !hasSubfolders) {
        issues.push(Issue.warning(
          readme.file,
          this.id,
          "Pasta possui README mas não tem conteúdo",
          undefined,
          "Adicione arquivos de conteúdo ou remova a pasta se não for necessária"
        ));
      }
    }

    return issues;
  }
}
