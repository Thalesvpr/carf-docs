import { App, TFile, parseYaml } from "obsidian";

/**
 * Locale messages structure (nested object with string values)
 */
export type LocaleMessages = Record<string, unknown>;

/**
 * Supported locales
 */
export type SupportedLocale = "en" | "pt-BR" | "es";

/**
 * Service for internationalization (i18n)
 */
export class I18nService {
  private app: App;
  private currentLocale: SupportedLocale = "en";
  private messages: Map<SupportedLocale, LocaleMessages> = new Map();
  private fallbackLocale: SupportedLocale = "en";

  constructor(app: App) {
    this.app = app;
  }

  /**
   * Initialize by loading locale files
   */
  async initialize(locale: string = "en"): Promise<void> {
    this.currentLocale = this.normalizeLocale(locale);

    // Load built-in messages
    this.messages.set("en", this.getEnglishMessages());
    this.messages.set("pt-BR", this.getPortugueseMessages());
    this.messages.set("es", this.getSpanishMessages());

    // Try to load custom locale files from vault
    await this.loadCustomLocales();
  }

  /**
   * Set the current locale
   */
  setLocale(locale: string): void {
    this.currentLocale = this.normalizeLocale(locale);
  }

  /**
   * Get current locale
   */
  getLocale(): SupportedLocale {
    return this.currentLocale;
  }

  /**
   * Translate a key with optional parameter interpolation
   */
  t(key: string, params?: Record<string, unknown>): string {
    // Try current locale
    let message = this.getMessage(key, this.currentLocale);

    // Fall back to fallback locale if not found
    if (message === key && this.currentLocale !== this.fallbackLocale) {
      message = this.getMessage(key, this.fallbackLocale);
    }

    // Interpolate parameters
    if (params && message !== key) {
      return this.interpolate(message, params);
    }

    return message;
  }

  /**
   * Get a message by key from a specific locale
   */
  private getMessage(key: string, locale: SupportedLocale): string {
    const messages = this.messages.get(locale);
    if (!messages) return key;

    // Navigate nested keys (e.g., "validators.frontmatter.name")
    const parts = key.split(".");
    let current: unknown = messages;

    for (const part of parts) {
      if (current && typeof current === "object" && part in current) {
        current = (current as Record<string, unknown>)[part];
      } else {
        return key;
      }
    }

    return typeof current === "string" ? current : key;
  }

  /**
   * Interpolate parameters into a message
   */
  private interpolate(message: string, params: Record<string, unknown>): string {
    return message.replace(/\{(\w+)\}/g, (match, key) => {
      return params[key] !== undefined ? String(params[key]) : match;
    });
  }

  /**
   * Normalize locale string to supported locale
   */
  private normalizeLocale(locale: string): SupportedLocale {
    const normalized = locale.toLowerCase();

    if (normalized === "en" || normalized.startsWith("en-")) {
      return "en";
    }

    if (normalized === "pt-br" || normalized === "pt" || normalized.startsWith("pt-")) {
      return "pt-BR";
    }

    if (normalized === "es" || normalized.startsWith("es-")) {
      return "es";
    }

    return "en";
  }

  /**
   * Load custom locale files from vault
   */
  private async loadCustomLocales(): Promise<void> {
    const localePath = ".plugins/obsidian-docs-toolkit/src/i18n/locales";

    for (const locale of ["en", "pt-BR", "es"] as SupportedLocale[]) {
      const filePath = `${localePath}/${locale}.yaml`;
      const file = this.app.vault.getAbstractFileByPath(filePath);

      if (file instanceof TFile) {
        try {
          const content = await this.app.vault.read(file);
          const customMessages = parseYaml(content) as LocaleMessages;

          // Merge with built-in messages
          const existing = this.messages.get(locale) || {};
          this.messages.set(locale, this.deepMerge(existing, customMessages));
        } catch (e) {
          console.warn(`Failed to load custom locale ${locale}:`, e);
        }
      }
    }
  }

  /**
   * Deep merge two objects
   */
  private deepMerge(target: LocaleMessages, source: LocaleMessages): LocaleMessages {
    const result = { ...target };

    for (const key of Object.keys(source)) {
      if (
        source[key] &&
        typeof source[key] === "object" &&
        !Array.isArray(source[key])
      ) {
        result[key] = this.deepMerge(
          (result[key] as LocaleMessages) || {},
          source[key] as LocaleMessages
        );
      } else {
        result[key] = source[key];
      }
    }

    return result;
  }

  /**
   * Get English messages (built-in)
   */
  private getEnglishMessages(): LocaleMessages {
    return {
      validators: {
        frontmatter: {
          name: "Lint: YAML Frontmatter",
          description: "Validates required frontmatter fields",
          missing: "File has no YAML frontmatter",
          missing_suggestion: "Add frontmatter with required fields",
          required_field: "Required field '{field}' is missing",
          required_field_suggestion: "Add the '{field}' field to frontmatter",
          wrong_type: "Field '{field}' should be {expected}, got {actual}",
          pattern_mismatch: "Field '{field}' value '{value}' doesn't match pattern '{pattern}'",
          invalid_enum: "Field '{field}' value '{value}' is not allowed. Valid values: {allowed}",
          invalid_array_item: "Field '{field}' contains invalid item '{item}'. Valid values: {allowed}",
          array_item_pattern_mismatch: "Field '{field}' item '{item}' doesn't match pattern '{pattern}'",
          below_min: "Field '{field}' value {value} is below minimum {min}",
          above_max: "Field '{field}' value {value} is above maximum {max}",
          too_short: "Field '{field}' length {length} is below minimum {min}",
          too_long: "Field '{field}' length {length} is above maximum {max}",
          array_too_short: "Field '{field}' has {length} items, minimum is {min}",
          array_too_long: "Field '{field}' has {length} items, maximum is {max}"
        },
        sections: {
          name: "Lint: Required Sections",
          description: "Validates required document sections",
          missing_required: "Required section '{section}' is missing",
          missing_required_suggestion: "Add section '## {section}' to the document",
          forbidden: "Section '{section}' is not allowed in this document type"
        },
        naming: {
          name: "Lint: File Naming",
          description: "Validates file naming conventions",
          pattern_mismatch: "Filename '{filename}' doesn't match expected pattern for {typeName}",
          pattern_mismatch_suggestion: "Rename file to match pattern: {pattern}"
        },
        title: {
          name: "Lint: Document Title",
          description: "Validates document title",
          missing: "Document has no title (# heading)",
          missing_suggestion: "Add a title with '# Title' at the start",
          pattern_mismatch: "Title '{title}' doesn't match expected pattern",
          pattern_mismatch_suggestion: "Update title to match pattern: {pattern}"
        },
        wordCount: {
          name: "Lint: Word Count",
          description: "Validates word count limits",
          exceeds_max: "Document has {count} words, maximum is {max}",
          below_min: "Document has {count} words, minimum is {min}",
          section_exceeds_max: "Section '{section}' has {count} words, maximum is {max}"
        },
        forbiddenPatterns: {
          name: "Lint: Forbidden Patterns",
          description: "Checks for forbidden text patterns",
          found: "Forbidden pattern '{pattern}' found: '{match}'",
          found_suggestion: "Remove or replace the forbidden pattern '{pattern}'"
        },
        links: {
          name: "Lint: Broken Links",
          description: "Validates internal links",
          broken: "Broken link to '{target}'",
          broken_suggestion: "Fix or remove the link to '{target}'"
        },
        stale: {
          name: "Lint: Freshness Check",
          description: "Checks for outdated documents",
          outdated: "Document hasn't been updated in {days} days (threshold: {threshold})",
          outdated_suggestion: "Review and update the document"
        },
        orphans: {
          name: "Lint: Orphan Detection",
          description: "Checks for unlinked documents",
          not_linked: "Document '{filename}' is not linked from any other document",
          not_linked_suggestion: "Add a link to this document from a relevant location"
        },
        emptyFolders: {
          name: "Lint: Empty Folders",
          description: "Checks for empty folders",
          empty: "Folder '{folder}' contains no markdown files",
          empty_suggestion: "Add content or remove the empty folder"
        }
      },
      ui: {
        issues: {
          title: "Issues",
          noIssues: "No issues found",
          errors: "Errors",
          warnings: "Warnings",
          info: "Info"
        },
        curation: {
          title: "Curation",
          approve: "Approve",
          reject: "Reject",
          skip: "Skip",
          progress: "Progress",
          pending: "Pending"
        }
      }
    };
  }

  /**
   * Get Portuguese messages (built-in)
   */
  private getPortugueseMessages(): LocaleMessages {
    return {
      validators: {
        frontmatter: {
          name: "Lint: YAML Frontmatter",
          description: "Valida campos obrigatórios no frontmatter",
          missing: "Arquivo não possui frontmatter YAML",
          missing_suggestion: "Adicione o frontmatter com os campos obrigatórios",
          required_field: "Campo obrigatório '{field}' está faltando",
          required_field_suggestion: "Adicione o campo '{field}' ao frontmatter",
          wrong_type: "Campo '{field}' deveria ser {expected}, mas é {actual}",
          pattern_mismatch: "Valor '{value}' do campo '{field}' não corresponde ao padrão '{pattern}'",
          invalid_enum: "Valor '{value}' do campo '{field}' não é permitido. Valores válidos: {allowed}",
          invalid_array_item: "Campo '{field}' contém item inválido '{item}'. Valores válidos: {allowed}",
          array_item_pattern_mismatch: "Item '{item}' do campo '{field}' não corresponde ao padrão '{pattern}'",
          below_min: "Valor {value} do campo '{field}' está abaixo do mínimo {min}",
          above_max: "Valor {value} do campo '{field}' está acima do máximo {max}",
          too_short: "Tamanho {length} do campo '{field}' está abaixo do mínimo {min}",
          too_long: "Tamanho {length} do campo '{field}' está acima do máximo {max}",
          array_too_short: "Campo '{field}' tem {length} itens, mínimo é {min}",
          array_too_long: "Campo '{field}' tem {length} itens, máximo é {max}"
        },
        sections: {
          name: "Lint: Required Sections",
          description: "Valida seções obrigatórias do documento",
          missing_required: "Seção obrigatória '{section}' não encontrada",
          missing_required_suggestion: "Adicione a seção '## {section}' ao documento",
          forbidden: "Seção '{section}' não é permitida neste tipo de documento"
        },
        naming: {
          name: "Lint: File Naming",
          description: "Valida convenções de nomenclatura de arquivos",
          pattern_mismatch: "Nome do arquivo '{filename}' não corresponde ao padrão esperado para {typeName}",
          pattern_mismatch_suggestion: "Renomeie o arquivo para corresponder ao padrão: {pattern}"
        },
        title: {
          name: "Lint: Document Title",
          description: "Valida título do documento",
          missing: "Documento não possui título (# cabeçalho)",
          missing_suggestion: "Adicione um título com '# Título' no início",
          pattern_mismatch: "Título '{title}' não corresponde ao padrão esperado",
          pattern_mismatch_suggestion: "Atualize o título para corresponder ao padrão: {pattern}"
        },
        wordCount: {
          name: "Lint: Word Count",
          description: "Valida limites de contagem de palavras",
          exceeds_max: "Documento tem {count} palavras, máximo é {max}",
          below_min: "Documento tem {count} palavras, mínimo é {min}",
          section_exceeds_max: "Seção '{section}' tem {count} palavras, máximo é {max}"
        },
        forbiddenPatterns: {
          name: "Lint: Forbidden Patterns",
          description: "Verifica padrões de texto proibidos",
          found: "Padrão proibido '{pattern}' encontrado: '{match}'",
          found_suggestion: "Remova ou substitua o padrão proibido '{pattern}'"
        },
        links: {
          name: "Lint: Broken Links",
          description: "Valida links internos",
          broken: "Link quebrado para '{target}'",
          broken_suggestion: "Corrija ou remova o link para '{target}'"
        },
        stale: {
          name: "Lint: Freshness Check",
          description: "Verifica documentos desatualizados",
          outdated: "Documento não foi atualizado há {days} dias (limite: {threshold})",
          outdated_suggestion: "Revise e atualize o documento"
        },
        orphans: {
          name: "Lint: Orphan Detection",
          description: "Verifica documentos não linkados",
          not_linked: "Documento '{filename}' não está linkado em nenhum outro documento",
          not_linked_suggestion: "Adicione um link para este documento em uma localização relevante"
        },
        emptyFolders: {
          name: "Lint: Empty Folders",
          description: "Verifica pastas vazias",
          empty: "Pasta '{folder}' não contém arquivos markdown",
          empty_suggestion: "Adicione conteúdo ou remova a pasta vazia"
        }
      },
      ui: {
        issues: {
          title: "Problemas",
          noIssues: "Nenhum problema encontrado",
          errors: "Erros",
          warnings: "Avisos",
          info: "Informações"
        },
        curation: {
          title: "Curadoria",
          approve: "Aprovar",
          reject: "Rejeitar",
          skip: "Pular",
          progress: "Progresso",
          pending: "Pendente"
        }
      }
    };
  }

  /**
   * Get Spanish messages (built-in)
   */
  private getSpanishMessages(): LocaleMessages {
    return {
      validators: {
        frontmatter: {
          name: "Frontmatter",
          description: "Valida campos requeridos en frontmatter",
          missing: "Archivo no tiene frontmatter YAML",
          missing_suggestion: "Agregue frontmatter con campos requeridos",
          required_field: "Campo requerido '{field}' falta",
          required_field_suggestion: "Agregue el campo '{field}' al frontmatter",
          wrong_type: "Campo '{field}' debería ser {expected}, es {actual}",
          pattern_mismatch: "Valor '{value}' del campo '{field}' no coincide con patrón '{pattern}'",
          invalid_enum: "Valor '{value}' del campo '{field}' no está permitido. Valores válidos: {allowed}",
          invalid_array_item: "Campo '{field}' contiene item inválido '{item}'. Valores válidos: {allowed}",
          array_item_pattern_mismatch: "Item '{item}' del campo '{field}' no coincide con patrón '{pattern}'",
          below_min: "Valor {value} del campo '{field}' está debajo del mínimo {min}",
          above_max: "Valor {value} del campo '{field}' está arriba del máximo {max}",
          too_short: "Longitud {length} del campo '{field}' está debajo del mínimo {min}",
          too_long: "Longitud {length} del campo '{field}' está arriba del máximo {max}",
          array_too_short: "Campo '{field}' tiene {length} items, mínimo es {min}",
          array_too_long: "Campo '{field}' tiene {length} items, máximo es {max}"
        },
        sections: {
          name: "Secciones",
          description: "Valida secciones requeridas del documento",
          missing_required: "Sección requerida '{section}' no encontrada",
          missing_required_suggestion: "Agregue la sección '## {section}' al documento",
          forbidden: "Sección '{section}' no está permitida en este tipo de documento"
        },
        naming: {
          name: "Nomenclatura",
          description: "Valida convenciones de nomenclatura de archivos",
          pattern_mismatch: "Nombre de archivo '{filename}' no coincide con patrón esperado para {typeName}",
          pattern_mismatch_suggestion: "Renombre el archivo para coincidir con patrón: {pattern}"
        },
        title: {
          name: "Título",
          description: "Valida título del documento",
          missing: "Documento no tiene título (# encabezado)",
          missing_suggestion: "Agregue un título con '# Título' al inicio",
          pattern_mismatch: "Título '{title}' no coincide con patrón esperado",
          pattern_mismatch_suggestion: "Actualice el título para coincidir con patrón: {pattern}"
        },
        wordCount: {
          name: "Conteo de Palabras",
          description: "Valida límites de conteo de palabras",
          exceeds_max: "Documento tiene {count} palabras, máximo es {max}",
          below_min: "Documento tiene {count} palabras, mínimo es {min}",
          section_exceeds_max: "Sección '{section}' tiene {count} palabras, máximo es {max}"
        },
        forbiddenPatterns: {
          name: "Patrones Prohibidos",
          description: "Verifica patrones de texto prohibidos",
          found: "Patrón prohibido '{pattern}' encontrado: '{match}'",
          found_suggestion: "Elimine o reemplace el patrón prohibido '{pattern}'"
        },
        links: {
          name: "Enlaces",
          description: "Valida enlaces internos",
          broken: "Enlace roto a '{target}'",
          broken_suggestion: "Corrija o elimine el enlace a '{target}'"
        },
        stale: {
          name: "Desactualizado",
          description: "Verifica documentos desactualizados",
          outdated: "Documento no se ha actualizado en {days} días (límite: {threshold})",
          outdated_suggestion: "Revise y actualice el documento"
        },
        orphans: {
          name: "Huérfanos",
          description: "Verifica documentos sin enlaces",
          not_linked: "Documento '{filename}' no está enlazado desde ningún otro documento",
          not_linked_suggestion: "Agregue un enlace a este documento desde una ubicación relevante"
        },
        emptyFolders: {
          name: "Carpetas Vacías",
          description: "Verifica carpetas vacías",
          empty: "Carpeta '{folder}' no contiene archivos markdown",
          empty_suggestion: "Agregue contenido o elimine la carpeta vacía"
        }
      },
      ui: {
        issues: {
          title: "Problemas",
          noIssues: "No se encontraron problemas",
          errors: "Errores",
          warnings: "Advertencias",
          info: "Información"
        },
        curation: {
          title: "Curación",
          approve: "Aprobar",
          reject: "Rechazar",
          skip: "Saltar",
          progress: "Progreso",
          pending: "Pendiente"
        }
      }
    };
  }
}
