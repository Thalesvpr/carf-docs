import { TFile } from "obsidian";

/**
 * Tipo de fix determina UX e segurança
 * - auto: seguro e determinístico, pode aplicar sem interação
 * - pick: usuário escolhe entre opções predefinidas
 * - prompt: usuário digita valor livre
 */
export type FixKind = "auto" | "pick" | "prompt";

/**
 * Tipo de ação a ser executada no arquivo
 */
export type FixActionType = "set-field" | "insert-frontmatter" | "remove-field";

/**
 * Uma ação de correção associada a uma Issue
 */
export interface FixAction {
  /**
   * ID único dentro da Issue (ex: "add-status", "set-updated")
   */
  id: string;

  /**
   * Label curto para botão (ex: "Add status", "Set to today")
   */
  label: string;

  /**
   * Descrição mais longa (tooltip)
   */
  description?: string;

  /**
   * Tipo de fix: auto (seguro), pick (escolher), prompt (digitar)
   */
  kind: FixKind;

  /**
   * Para kind="pick": opções disponíveis
   * Ex: ["review", "approved", "rejected"]
   */
  options?: string[];

  /**
   * Para kind="prompt": placeholder/hint para input
   * Ex: "Digite o ID (ex: RF-001)"
   */
  promptHint?: string;

  /**
   * Para kind="auto": valor a ser aplicado (se determinístico)
   * Ex: "review" para status default, ou ISO date para updated
   */
  autoValue?: unknown;

  /**
   * Campo do frontmatter afetado (para fixes de frontmatter)
   * Ex: "status", "updated", "id"
   */
  targetField?: string;

  /**
   * Tipo de ação a executar
   * @default "set-field"
   */
  actionType?: FixActionType;
}

/**
 * Contexto para aplicar um fix
 */
export interface FixContext {
  /**
   * Arquivo alvo
   */
  file: TFile;

  /**
   * Ação a ser aplicada
   */
  action: FixAction;

  /**
   * Para kind="pick": opção selecionada pelo usuário
   */
  selectedOption?: string;

  /**
   * Para kind="prompt": valor digitado pelo usuário
   */
  promptValue?: string;
}

/**
 * Resultado de aplicar um fix
 */
export interface FixResult {
  /**
   * Se o fix foi aplicado com sucesso
   */
  success: boolean;

  /**
   * Mensagem para mostrar ao usuário
   */
  message?: string;

  /**
   * Se true, revalidar o arquivo após fix
   * @default true
   */
  shouldRevalidate: boolean;

  /**
   * Erro que ocorreu (se success=false)
   */
  error?: Error;
}

/**
 * Helper para criar um FixAction do tipo AUTO
 */
export function createAutoFix(
  id: string,
  label: string,
  targetField: string,
  autoValue: unknown,
  description?: string
): FixAction {
  return {
    id,
    label,
    kind: "auto",
    targetField,
    autoValue,
    actionType: "set-field",
    description
  };
}

/**
 * Helper para criar um FixAction do tipo PICK
 */
export function createPickFix(
  id: string,
  label: string,
  targetField: string,
  options: string[],
  description?: string
): FixAction {
  return {
    id,
    label,
    kind: "pick",
    targetField,
    options,
    actionType: "set-field",
    description
  };
}

/**
 * Helper para criar um FixAction do tipo PROMPT
 */
export function createPromptFix(
  id: string,
  label: string,
  targetField: string,
  promptHint: string,
  description?: string
): FixAction {
  return {
    id,
    label,
    kind: "prompt",
    targetField,
    promptHint,
    actionType: "set-field",
    description
  };
}

/**
 * Helper para criar um FixAction que insere frontmatter scaffold
 */
export function createScaffoldFix(
  id: string,
  label: string,
  scaffoldContent: string,
  description?: string
): FixAction {
  return {
    id,
    label,
    kind: "auto",
    targetField: "__scaffold__",
    autoValue: scaffoldContent,
    actionType: "insert-frontmatter",
    description
  };
}

// --- Type Guards ---

/**
 * Check if a FixAction is an auto fix (deterministic, safe to apply without interaction)
 */
export function isAutoFix(fix: FixAction): boolean {
  return fix.kind === "auto";
}

/**
 * Check if a FixAction is a pick fix (user selects from options)
 */
export function isPickFix(fix: FixAction): boolean {
  return fix.kind === "pick";
}

/**
 * Check if a FixAction is a prompt fix (user types value)
 */
export function isPromptFix(fix: FixAction): boolean {
  return fix.kind === "prompt";
}
