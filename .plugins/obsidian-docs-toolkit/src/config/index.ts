export { ConfigLoader } from "./ConfigLoader";
export { ConfigWatcher } from "./ConfigWatcher";
export type {
  DocsLinterConfig,
  PathsConfig,
  DocumentTypeConfig,
  DetectionConfig,
  FrontmatterConfig,
  FieldConfig,
  TitleConfig,
  SectionsConfig,
  ValidatorConfig,
  WorkflowConfig,
  StatusConfig,
  TemplateValidation,
  TemplateFrontmatter
} from "./ConfigSchema";
export { DEFAULT_CONFIG, isTemplateFrontmatter } from "./ConfigSchema";
