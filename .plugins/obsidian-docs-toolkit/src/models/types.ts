/**
 * Document types in CARF
 */
export enum DocType {
  RF = "RF",       // Requisito Funcional
  RNF = "RNF",     // Requisito Não Funcional
  UC = "UC",       // Use Case
  US = "US",       // User Story
  ARCH = "ARCH",   // Architecture
  README = "README",
  OTHER = "OTHER"
}

/**
 * Document status in workflow
 */
export enum Status {
  REVIEW = "review",
  APPROVED = "approved",
  REJECTED = "rejected",
  TEMPLATE = "template"
}

/**
 * Issue severity levels
 */
export enum Severity {
  ERROR = "error",
  WARNING = "warning",
  INFO = "info"
}

/**
 * Valid modules in CARF
 */
export const VALID_MODULES = [
  "GEOAPI",
  "REURBWEB",
  "ADMIN",
  "KEYCLOAK",
  "WEBDOCS"
] as const;

export type Module = typeof VALID_MODULES[number];

/**
 * Frontmatter structure for CARF documents
 *
 * Campos obrigatórios: status, updated
 * Campos opcionais: id, type, modules, epic, created, description
 */
export interface CARFFrontmatter {
  status: Status;
  updated: string;
  id?: string;
  type?: DocType;
  modules?: Module[];
  epic?: string;
  created?: string;
  description?: string;
}

/**
 * Default paths for CARF structure
 */
export const DEFAULT_PATHS = {
  CENTRAL: "CENTRAL",
  PROJECTS: "PROJECTS",
  REQUIREMENTS: "CENTRAL/REQUIREMENTS",
  FUNCTIONAL: "CENTRAL/REQUIREMENTS/FUNCTIONAL",
  NON_FUNCTIONAL: "CENTRAL/REQUIREMENTS/NON-FUNCTIONAL",
  USE_CASES: "CENTRAL/REQUIREMENTS/USE-CASES",
  USER_STORIES: "CENTRAL/REQUIREMENTS/USER-STORIES"
} as const;

/**
 * Required sections by document type
 */
export const REQUIRED_SECTIONS: Record<DocType, string[]> = {
  [DocType.RF]: ["Critérios de Aceitação", "Regras de Negócio"],
  [DocType.RNF]: ["Critérios de Aceitação", "Métricas"],
  [DocType.UC]: ["Atores", "Pré-condições", "Fluxo Principal", "Fluxos Alternativos", "Pós-condições"],
  [DocType.US]: ["Critérios de Aceitação"],
  [DocType.ARCH]: [],
  [DocType.README]: [],
  [DocType.OTHER]: []
};

/**
 * Title patterns by document type
 */
export const TITLE_PATTERNS: Record<DocType, RegExp> = {
  [DocType.RF]: /^# RF-\d{3}: .+$/,
  [DocType.RNF]: /^# RNF-\d{3}: .+$/,
  [DocType.UC]: /^# UC-\d{3}: .+$/,
  [DocType.US]: /^# US-\d{3}: .+$/,
  [DocType.ARCH]: /^# .+$/,
  [DocType.README]: /^# .+$/,
  [DocType.OTHER]: /^# .+$/
};

/**
 * Naming patterns for files
 */
export const NAMING_PATTERNS: Record<DocType, RegExp> = {
  [DocType.RF]: /^RF-\d{3}-.+\.md$/,
  [DocType.RNF]: /^RNF-\d{3}-.+\.md$/,
  [DocType.UC]: /^\d{2}-UC-\d{3}-.+\.md$|^UC-\d{3}-.+\.md$/,
  [DocType.US]: /^US-\d{3}-.+\.md$/,
  [DocType.ARCH]: /^\d{2}-.+\.md$/,
  [DocType.README]: /^README\.md$/,
  [DocType.OTHER]: /.+\.md$/
};

/**
 * Stale threshold in days
 */
export const STALE_THRESHOLD_DAYS = 180; // 6 months
