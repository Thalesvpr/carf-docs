import { App } from "obsidian";
import { Document } from "../../core/Document";
import { DocsLinterConfig, DocumentTypeConfig, TemplateValidation } from "../../config/ConfigSchema";
import { ValidatorContext } from "./Validator";

/**
 * Factory function to create a ValidatorContext for a document
 */
export function createValidatorContext(
  app: App,
  config: DocsLinterConfig,
  doc: Document,
  t: (key: string, params?: Record<string, unknown>) => string,
  templateValidation: TemplateValidation | null = null,
  allDocuments?: Document[]
): ValidatorContext {
  // Find matching document type config
  const documentTypeConfig = findDocumentTypeConfig(doc, config);

  return {
    app,
    config,
    documentTypeConfig,
    templateValidation,
    t,
    allDocuments
  };
}

/**
 * Find the document type configuration for a document
 */
export function findDocumentTypeConfig(
  doc: Document,
  config: DocsLinterConfig
): DocumentTypeConfig | null {
  for (const [typeId, typeConfig] of Object.entries(config.documentTypes)) {
    if (matchesDocumentType(doc, typeConfig)) {
      doc.detectedType = typeId;
      return typeConfig;
    }
  }
  return null;
}

/**
 * Check if a document matches a document type configuration
 */
function matchesDocumentType(doc: Document, typeConfig: DocumentTypeConfig): boolean {
  const detection = typeConfig.detection;

  // Check filename pattern
  if (detection.filename) {
    const regex = new RegExp(detection.filename);
    if (!regex.test(doc.file.name)) {
      return false;
    }
  }

  // Check path pattern
  if (detection.path) {
    const pathPattern = detection.path
      .replace(/\*\*/g, ".*")
      .replace(/\*/g, "[^/]*");
    const regex = new RegExp(pathPattern);
    if (!regex.test(doc.file.path)) {
      return false;
    }
  }

  // Check frontmatter field
  if (detection.frontmatterField) {
    const { field, value } = detection.frontmatterField;
    const actualValue = doc.getFrontmatterField<string>(field);
    if (actualValue?.toLowerCase() !== value.toLowerCase()) {
      return false;
    }
  }

  // If no detection rules or all rules pass
  return true;
}
