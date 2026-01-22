import { App } from "obsidian";
import { Document } from "../../core/Document";
import { DocsLinterConfig, DocumentTypeConfig, TemplateValidation } from "../../config/ConfigSchema";
import { ValidatorContext } from "./Validator";
import { TypeRegistry } from "../../services/TypeRegistry";

/**
 * Factory function to create a ValidatorContext for a document
 *
 * Uses TypeRegistry for centralized type detection.
 */
export function createValidatorContext(
  app: App,
  config: DocsLinterConfig,
  doc: Document,
  t: (key: string, params?: Record<string, unknown>) => string,
  templateValidation: TemplateValidation | null = null,
  allDocuments?: Document[],
  typeRegistry?: TypeRegistry
): ValidatorContext {
  // Use TypeRegistry for type detection if available
  let documentTypeConfig: DocumentTypeConfig | null = null;

  if (typeRegistry) {
    const typeId = typeRegistry.detectType(doc.file, doc.frontmatter);
    doc.detectedType = typeId;
    documentTypeConfig = typeRegistry.getValidationConfig(typeId);
  } else {
    // Fallback to legacy detection (for backwards compatibility)
    documentTypeConfig = findDocumentTypeConfigLegacy(doc, config);
  }

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
 * Legacy document type detection (deprecated, use TypeRegistry)
 *
 * @deprecated Use TypeRegistry.detectType() instead
 */
export function findDocumentTypeConfigLegacy(
  doc: Document,
  config: DocsLinterConfig
): DocumentTypeConfig | null {
  for (const [typeId, typeConfig] of Object.entries(config.documentTypes)) {
    if (matchesDocumentTypeLegacy(doc, typeConfig)) {
      doc.detectedType = typeId;
      return typeConfig;
    }
  }
  return null;
}

/**
 * Legacy type matching (deprecated)
 * @deprecated
 */
function matchesDocumentTypeLegacy(doc: Document, typeConfig: DocumentTypeConfig): boolean {
  const detection = typeConfig.detection;

  // Check filename pattern (new structure)
  if (detection.filename?.pattern) {
    try {
      const regex = new RegExp(detection.filename.pattern);
      if (regex.test(doc.file.name)) {
        return true;
      }
    } catch { /* invalid regex */ }
  }

  if (detection.filename?.exact) {
    if (doc.file.name === detection.filename.exact) {
      return true;
    }
  }

  // Check path (new structure)
  if (detection.path?.contains) {
    if (doc.file.path.toLowerCase().includes(detection.path.contains.toLowerCase())) {
      return true;
    }
  }

  if (detection.path?.pattern) {
    try {
      const pathPattern = detection.path.pattern
        .replace(/\*\*/g, ".*")
        .replace(/\*/g, "[^/]*");
      const regex = new RegExp(pathPattern);
      if (regex.test(doc.file.path)) {
        return true;
      }
    } catch { /* invalid pattern */ }
  }

  // Check frontmatter (new structure)
  if (detection.frontmatter?.type) {
    const fmType = doc.getFrontmatterField<string>("type");
    if (fmType?.toLowerCase() === detection.frontmatter.type.toLowerCase()) {
      return true;
    }
  }

  if (detection.frontmatter?.field && detection.frontmatter?.value) {
    const actualValue = doc.getFrontmatterField<string>(detection.frontmatter.field);
    if (actualValue?.toLowerCase() === detection.frontmatter.value.toLowerCase()) {
      return true;
    }
  }

  return false;
}
