import { App, TFile, parseYaml } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";

/**
 * Validation rules from ADR-000-template.md frontmatter
 */
interface ADRValidationRules {
  max_words: number;
  max_words_per_section: number;
  required_sections: string[];
  forbidden: string[];
}

const DEFAULT_RULES: ADRValidationRules = {
  max_words: 300,
  max_words_per_section: 80,
  required_sections: ["Contexto", "Decisao", "Consequencias", "Alternativas Rejeitadas"],
  forbidden: ["```", "http", "|--|", "- ["]
};

const ADR_TITLE_PATTERN = /^ADR-\d{3}:/;
const ADR_FILENAME_PATTERN = /^ADR-\d{3}-.+\.md$/;
const TEMPLATE_PATH = "CENTRAL/ARCHITECTURE/ADRs/ADR-000-template.md";

/**
 * Validator for ADR (Architecture Decision Record) documents.
 * Reads validation rules from ADR-000-template.md frontmatter.
 */
export class ADRValidator extends LocalValidator {
  id = "adr-structure";
  name = "ADR Structure";
  description = "Valida estrutura de ADRs conforme template";

  private rulesCache: ADRValidationRules | null = null;

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Only validate files in ADRs folder
    if (!this.isADRFile(document)) {
      return issues;
    }

    // Skip template file
    if (document.file.name === "ADR-000-template.md") {
      return issues;
    }

    // Load rules from template
    const rules = await this.loadRules(app);

    // Run validations
    this.validateFilename(document, issues);
    this.validateTitle(document, issues);
    this.validateRequiredSections(document, rules, issues);
    this.validateWordCount(document, rules, issues);
    this.validateForbiddenPatterns(document, rules, issues);

    return issues;
  }

  /**
   * Load validation rules from template frontmatter
   */
  private async loadRules(app: App): Promise<ADRValidationRules> {
    if (this.rulesCache) {
      return this.rulesCache;
    }

    try {
      const templateFile = app.vault.getAbstractFileByPath(TEMPLATE_PATH) as TFile;
      if (!templateFile) {
        return DEFAULT_RULES;
      }

      const content = await app.vault.read(templateFile);
      const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
      if (!match) {
        return DEFAULT_RULES;
      }

      const yaml = parseYaml(match[1]);
      if (!yaml?.validation) {
        return DEFAULT_RULES;
      }

      this.rulesCache = {
        max_words: yaml.validation.max_words ?? DEFAULT_RULES.max_words,
        max_words_per_section: yaml.validation.max_words_per_section ?? DEFAULT_RULES.max_words_per_section,
        required_sections: yaml.validation.required_sections ?? DEFAULT_RULES.required_sections,
        forbidden: yaml.validation.forbidden ?? DEFAULT_RULES.forbidden
      };

      return this.rulesCache;
    } catch {
      return DEFAULT_RULES;
    }
  }

  /**
   * Check if file is in ADRs folder
   */
  private isADRFile(document: Document): boolean {
    return document.file.path.includes("/ADRs/") &&
           document.file.name.startsWith("ADR-");
  }

  /**
   * Validate filename follows ADR-XXX-name.md pattern
   */
  private validateFilename(document: Document, issues: Issue[]): void {
    if (!ADR_FILENAME_PATTERN.test(document.file.name)) {
      issues.push(Issue.error(
        document.file,
        this.id,
        `Nome deve seguir padrão ADR-XXX-nome.md`,
        1,
        `Renomear arquivo`
      ));
    }
  }

  /**
   * Validate H1 title follows "ADR-XXX: Titulo" pattern
   */
  private validateTitle(document: Document, issues: Issue[]): void {
    const title = document.title;

    if (!title) {
      issues.push(Issue.error(
        document.file,
        this.id,
        `ADR deve ter título H1`,
        1,
        `Adicionar: # ADR-XXX: Titulo`
      ));
      return;
    }

    if (!ADR_TITLE_PATTERN.test(title)) {
      issues.push(Issue.error(
        document.file,
        this.id,
        `Título deve seguir padrão "ADR-XXX: Titulo"`,
        this.findTitleLine(document)
      ));
    }
  }

  /**
   * Validate all required sections are present
   */
  private validateRequiredSections(document: Document, rules: ADRValidationRules, issues: Issue[]): void {
    const presentSections = Array.from(document.sections.keys());

    for (const required of rules.required_sections) {
      const found = presentSections.some(
        s => this.normalizeText(s) === this.normalizeText(required)
      );

      if (!found) {
        issues.push(Issue.error(
          document.file,
          this.id,
          `Seção obrigatória ausente: "## ${required}"`
        ));
      }
    }
  }

  /**
   * Validate word count limits
   */
  private validateWordCount(document: Document, rules: ADRValidationRules, issues: Issue[]): void {
    // Get body without frontmatter
    const body = document.content.replace(/^---[\s\S]*?---\n*/, "");

    // Total word count (excluding headers)
    const totalWords = this.countWords(body);
    if (totalWords > rules.max_words) {
      issues.push(Issue.warning(
        document.file,
        this.id,
        `${totalWords} palavras (máx: ${rules.max_words})`,
        undefined,
        `Reduzir texto para no máximo ${rules.max_words} palavras`
      ));
    }

    // Per-section word count
    for (const [section, content] of document.sections) {
      // Skip "Regras" section (template instructions)
      if (this.normalizeText(section) === "regras") continue;

      const sectionWords = this.countWords(content);
      if (sectionWords > rules.max_words_per_section) {
        const line = this.findSectionLine(document, section);
        issues.push(Issue.warning(
          document.file,
          this.id,
          `"${section}": ${sectionWords} palavras (máx: ${rules.max_words_per_section})`,
          line,
          `Reduzir seção para no máximo ${rules.max_words_per_section} palavras`
        ));
      }
    }
  }

  /**
   * Validate forbidden patterns are not present
   */
  private validateForbiddenPatterns(document: Document, rules: ADRValidationRules, issues: Issue[]): void {
    const body = document.content.replace(/^---[\s\S]*?---\n*/, "");
    const lines = body.split("\n");

    for (const pattern of rules.forbidden) {
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes(pattern)) {
          const patternLabel = this.getForbiddenLabel(pattern);
          issues.push(Issue.error(
            document.file,
            this.id,
            `${patternLabel} não permitido em ADR`,
            i + 1,
            `Remover e usar apenas texto corrido`
          ));
          break; // One error per pattern is enough
        }
      }
    }
  }

  /**
   * Get human-readable label for forbidden pattern
   */
  private getForbiddenLabel(pattern: string): string {
    switch (pattern) {
      case "```": return "Bloco de código";
      case "http": return "Link externo";
      case "|--|": return "Tabela";
      case "- [": return "Checklist";
      default: return `Padrão "${pattern}"`;
    }
  }

  /**
   * Count words in text (excluding markdown syntax)
   */
  private countWords(text: string): number {
    // Remove headers
    const noHeaders = text.replace(/^#+\s+.+$/gm, "");
    // Remove extra whitespace and count
    const words = noHeaders.trim().split(/\s+/).filter(w => w.length > 0);
    return words.length;
  }

  /**
   * Normalize text for comparison (remove accents, lowercase)
   */
  private normalizeText(text: string): string {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .trim();
  }

  /**
   * Find the line number of the H1 title
   */
  private findTitleLine(document: Document): number {
    const lines = document.content.split("\n");
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith("# ")) {
        return i + 1;
      }
    }
    return 1;
  }

  /**
   * Find the line number of a section header
   */
  private findSectionLine(document: Document, section: string): number {
    const lines = document.content.split("\n");
    const normalized = this.normalizeText(section);
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith("## ")) {
        const headerText = lines[i].replace(/^##\s+/, "");
        if (this.normalizeText(headerText) === normalized) {
          return i + 1;
        }
      }
    }
    return 1;
  }
}
