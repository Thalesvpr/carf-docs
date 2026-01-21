import { App, TFile, TFolder, parseYaml } from "obsidian";
import { Document } from "../models/Document";
import { Issue } from "../models/Issue";
import { LocalValidator } from "./Validator";

interface ValidationRules {
  max_words?: number;
  max_words_per_section?: number;
  required_sections?: string[];
  forbidden?: string[];
  title_pattern?: string;
  filename_pattern?: string;
}

/**
 * Template Validator - validates documents against template rules
 */
export class TemplateValidator extends LocalValidator {
  id = "template-rules";
  name = "Template Rules";
  description = "Valida documentos conforme regras do template";

  async validateFile(document: Document, app: App): Promise<Issue[]> {
    const issues: Issue[] = [];

    // Get document type
    const docType = this.getDocType(document);
    console.log(`[TemplateValidator] ${document.file.name} -> type: ${docType}`);

    // Skip templates themselves
    if (docType === "template") {
      return issues;
    }

    // Find and load template rules
    const rules = await this.findTemplateRules(document.file, docType, app);
    console.log(`[TemplateValidator] ${document.file.name} -> rules:`, rules);

    if (!rules) {
      return issues; // No template found
    }

    // Validate filename
    if (rules.filename_pattern) {
      try {
        const regex = new RegExp(rules.filename_pattern);
        if (!regex.test(document.file.name)) {
          issues.push(Issue.error(
            document.file,
            this.id,
            `Nome não segue padrão do template`
          ));
        }
      } catch { /* invalid regex */ }
    }

    // Validate title
    if (rules.title_pattern) {
      const title = document.title;
      if (!title) {
        issues.push(Issue.error(document.file, this.id, `Falta título H1`));
      } else {
        try {
          const regex = new RegExp(rules.title_pattern);
          if (!regex.test(title)) {
            issues.push(Issue.error(
              document.file,
              this.id,
              `Título não segue padrão do template`
            ));
          }
        } catch { /* invalid regex */ }
      }
    }

    // Validate required sections
    if (rules.required_sections && rules.required_sections.length > 0) {
      const presentSections = Array.from(document.sections.keys()).map(s => this.norm(s));

      for (const required of rules.required_sections) {
        if (!presentSections.includes(this.norm(required))) {
          issues.push(Issue.error(
            document.file,
            this.id,
            `Seção ausente: "## ${required}"`
          ));
        }
      }
    }

    // Validate max words
    if (rules.max_words) {
      const body = document.content.replace(/^---[\s\S]*?---\n*/, "");
      const words = this.countWords(body);
      if (words > rules.max_words) {
        issues.push(Issue.warning(
          document.file,
          this.id,
          `${words} palavras (máx: ${rules.max_words})`
        ));
      }
    }

    // Validate max words per section
    if (rules.max_words_per_section) {
      for (const [section, content] of document.sections) {
        if (this.norm(section) === "regras") continue;
        const words = this.countWords(content);
        if (words > rules.max_words_per_section) {
          issues.push(Issue.warning(
            document.file,
            this.id,
            `Seção "${section}": ${words} palavras (máx: ${rules.max_words_per_section})`
          ));
        }
      }
    }

    // Validate forbidden patterns
    if (rules.forbidden && rules.forbidden.length > 0) {
      const body = document.content.replace(/^---[\s\S]*?---\n*/, "");

      for (const pattern of rules.forbidden) {
        if (body.includes(pattern)) {
          const label = this.getForbiddenLabel(pattern);
          issues.push(Issue.error(
            document.file,
            this.id,
            `${label} não permitido em documento deste tipo`
          ));
        }
      }
    }

    return issues;
  }

  /**
   * Get document type from frontmatter or filename
   */
  private getDocType(document: Document): string {
    // Check frontmatter
    const content = document.content;
    const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (match) {
      try {
        const yaml = parseYaml(match[1]);
        if (yaml?.type) return yaml.type.toLowerCase();
      } catch { /* ignore */ }
    }

    // Infer from filename
    const name = document.file.name;
    if (name.includes("-000-template")) return "template";
    if (name.startsWith("ADR-")) return "adr";
    if (name.startsWith("RF-")) return "rf";
    if (name.startsWith("RNF-")) return "rnf";
    if (name.startsWith("UC-") || /^\d{2}-UC-/.test(name)) return "uc";
    if (name.startsWith("US-")) return "us";
    if (name === "README.md") return "readme";
    return "doc";
  }

  /**
   * Find template rules for document type
   */
  private async findTemplateRules(file: TFile, docType: string, app: App): Promise<ValidationRules | null> {
    let folder: TFolder | null = file.parent;

    while (folder) {
      // Look for template in this folder
      for (const child of folder.children) {
        if (!(child instanceof TFile)) continue;
        if (!child.name.endsWith(".md")) continue;

        // Check if it's a template for our type
        const rules = await this.checkIfTemplate(child, docType, app);
        if (rules) {
          return rules;
        }
      }

      // Go up to parent
      folder = folder.parent;
    }

    return null;
  }

  /**
   * Check if file is a template for given type and return its rules
   */
  private async checkIfTemplate(file: TFile, docType: string, app: App): Promise<ValidationRules | null> {
    try {
      const content = await app.vault.read(file);
      const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
      if (!match) return null;

      const yaml = parseYaml(match[1]);
      if (!yaml) return null;

      // Check if it's a template
      const isTemplate = yaml.type === "template" ||
                        yaml.status === "template" ||
                        file.name.includes("-000-template");

      if (!isTemplate) return null;

      // Check if template_for matches our type
      const templateFor = yaml.template_for?.toLowerCase();
      if (templateFor !== docType) return null;

      // Return validation rules
      return yaml.validation || null;
    } catch {
      return null;
    }
  }

  private countWords(text: string): number {
    const clean = text.replace(/^#+\s+.+$/gm, "");
    return clean.trim().split(/\s+/).filter(w => w.length > 0).length;
  }

  private norm(text: string): string {
    return text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
  }

  private getForbiddenLabel(pattern: string): string {
    const map: Record<string, string> = {
      "```": "Bloco de código",
      "http": "Link",
      "|--|": "Tabela",
      "- [": "Checklist"
    };
    return map[pattern] || `"${pattern}"`;
  }
}
