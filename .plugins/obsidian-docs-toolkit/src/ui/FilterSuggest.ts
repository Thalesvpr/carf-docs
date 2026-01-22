import { App, AbstractInputSuggest, TFile, prepareFuzzySearch, renderResults } from "obsidian";
import { Document } from "../core/Document";

/**
 * Suggestion item for filter input
 */
interface FilterSuggestion {
  text: string;
  displayText: string;
  description?: string;
  type: "operator" | "value";
}

/**
 * Filter input with autocomplete suggestions
 * Mimics Obsidian's native graph view filter behavior
 */
export class FilterSuggest extends AbstractInputSuggest<FilterSuggestion> {
  private getDocuments: () => Document[];
  private onFilterChange: (value: string) => void;

  // Available operators
  private operators: FilterSuggestion[] = [
    { text: "path:", displayText: "path:", description: "Search in file path", type: "operator" },
    { text: "file:", displayText: "file:", description: "Search in file name", type: "operator" },
    { text: "tag:", displayText: "tag:", description: "Search by tag", type: "operator" },
    { text: "status:", displayText: "status:", description: "Filter by status", type: "operator" },
    { text: "id:", displayText: "id:", description: "Search by document ID", type: "operator" },
    { text: "section:", displayText: "section:", description: "Search in section titles", type: "operator" },
    { text: "-", displayText: "-", description: "Exclude (negate)", type: "operator" },
    { text: "OR", displayText: "OR", description: "Match either condition", type: "operator" },
  ];

  // Status values
  private statuses = ["approved", "rejected", "review", "none"];

  constructor(
    app: App,
    inputEl: HTMLInputElement,
    getDocuments: () => Document[],
    onFilterChange: (value: string) => void
  ) {
    super(app, inputEl);
    this.getDocuments = getDocuments;
    this.onFilterChange = onFilterChange;
    this.limit = 20;
  }

  getSuggestions(query: string): FilterSuggestion[] {
    const suggestions: FilterSuggestion[] = [];
    const cursorPos = (this as any).textInputEl?.selectionStart || query.length;

    // Find the current token being typed
    const beforeCursor = query.substring(0, cursorPos);
    const tokens = beforeCursor.split(/\s+/);
    const currentToken = tokens[tokens.length - 1] || "";

    // Check if we're typing after an operator
    const operatorMatch = currentToken.match(/^(-?)(path|file|tag|status|id|section):(.*)$/i);

    if (operatorMatch) {
      // We have an operator, suggest values
      const [, negation, operator, valueQuery] = operatorMatch;
      const opLower = operator.toLowerCase();

      if (opLower === "status") {
        // Suggest status values
        for (const status of this.statuses) {
          if (!valueQuery || status.toLowerCase().startsWith(valueQuery.toLowerCase())) {
            suggestions.push({
              text: `${negation}${operator}:${status}`,
              displayText: status,
              description: `Status: ${status}`,
              type: "value"
            });
          }
        }
      } else if (opLower === "tag") {
        // Suggest tags from documents
        const tags = this.collectTags();
        const search = valueQuery ? prepareFuzzySearch(valueQuery) : null;
        for (const tag of tags) {
          if (!search || search(tag)) {
            suggestions.push({
              text: `${negation}${operator}:${tag}`,
              displayText: tag,
              description: `Tag`,
              type: "value"
            });
          }
        }
      } else if (opLower === "path") {
        // Suggest folder paths
        const paths = this.collectPaths();
        const search = valueQuery ? prepareFuzzySearch(valueQuery) : null;
        for (const path of paths) {
          if (!search || search(path)) {
            suggestions.push({
              text: `${negation}${operator}:"${path}"`,
              displayText: path,
              description: `Folder`,
              type: "value"
            });
          }
        }
      } else if (opLower === "id") {
        // Suggest document IDs
        const ids = this.collectIds();
        const search = valueQuery ? prepareFuzzySearch(valueQuery) : null;
        for (const id of ids) {
          if (!search || search(id)) {
            suggestions.push({
              text: `${negation}${operator}:${id}`,
              displayText: id,
              description: `Document ID`,
              type: "value"
            });
          }
        }
      } else if (opLower === "file") {
        // Suggest file names
        const files = this.collectFileNames();
        const search = valueQuery ? prepareFuzzySearch(valueQuery) : null;
        for (const file of files.slice(0, 50)) {
          if (!search || search(file)) {
            suggestions.push({
              text: `${negation}${operator}:${file}`,
              displayText: file,
              description: `File`,
              type: "value"
            });
          }
        }
      } else if (opLower === "section") {
        // Suggest section titles
        const sections = this.collectSections();
        const search = valueQuery ? prepareFuzzySearch(valueQuery) : null;
        for (const section of sections) {
          if (!search || search(section)) {
            suggestions.push({
              text: `${negation}${operator}:"${section}"`,
              displayText: section,
              description: `Section`,
              type: "value"
            });
          }
        }
      }
    } else {
      // Suggest operators
      const search = currentToken ? prepareFuzzySearch(currentToken) : null;
      for (const op of this.operators) {
        if (!search || search(op.text)) {
          suggestions.push(op);
        }
      }

      // Also suggest commonly used paths/tags when no operator
      if (currentToken && currentToken.length >= 2) {
        const docs = this.getDocuments();
        const searchFn = prepareFuzzySearch(currentToken);

        // Suggest matching file names
        for (const doc of docs.slice(0, 10)) {
          if (searchFn(doc.file.basename)) {
            suggestions.push({
              text: doc.file.basename,
              displayText: doc.file.basename,
              description: doc.file.parent?.path || "",
              type: "value"
            });
          }
        }
      }
    }

    return suggestions.slice(0, this.limit);
  }

  renderSuggestion(suggestion: FilterSuggestion, el: HTMLElement): void {
    el.addClass("mod-complex");

    const content = el.createDiv({ cls: "suggestion-content" });
    content.createDiv({ cls: "suggestion-title", text: suggestion.displayText });

    if (suggestion.description) {
      content.createDiv({ cls: "suggestion-note", text: suggestion.description });
    }

    if (suggestion.type === "operator") {
      el.createDiv({ cls: "suggestion-aux", text: "operator" });
    }
  }

  selectSuggestion(suggestion: FilterSuggestion, evt: MouseEvent | KeyboardEvent): void {
    const currentValue = this.getValue();
    const cursorPos = (this as any).textInputEl?.selectionStart || currentValue.length;

    // Find where the current token starts
    const beforeCursor = currentValue.substring(0, cursorPos);
    const tokens = beforeCursor.split(/\s+/);
    const currentToken = tokens[tokens.length - 1] || "";
    const tokenStart = beforeCursor.lastIndexOf(currentToken);

    // Replace current token with suggestion
    const newValue =
      currentValue.substring(0, tokenStart) +
      suggestion.text +
      (suggestion.type === "operator" && !suggestion.text.endsWith(":") ? " " : "") +
      currentValue.substring(cursorPos);

    this.setValue(newValue);
    this.onFilterChange(newValue);
    this.close();
  }

  // Helper methods to collect suggestions from documents
  private collectTags(): string[] {
    const tags = new Set<string>();
    for (const doc of this.getDocuments()) {
      if (doc.frontmatter?.tags) {
        const docTags = Array.isArray(doc.frontmatter.tags)
          ? doc.frontmatter.tags
          : [doc.frontmatter.tags];
        for (const tag of docTags) {
          tags.add(String(tag));
        }
      }
    }
    return Array.from(tags).sort();
  }

  private collectPaths(): string[] {
    const paths = new Set<string>();
    for (const doc of this.getDocuments()) {
      const parts = doc.file.path.split("/");
      // Add each folder level
      for (let i = 1; i < parts.length; i++) {
        paths.add(parts.slice(0, i).join("/"));
      }
    }
    return Array.from(paths).sort();
  }

  private collectIds(): string[] {
    const ids: string[] = [];
    for (const doc of this.getDocuments()) {
      if (doc.id) {
        ids.push(doc.id);
      }
    }
    return ids.sort();
  }

  private collectFileNames(): string[] {
    const names: string[] = [];
    for (const doc of this.getDocuments()) {
      names.push(doc.file.basename);
    }
    return names.sort();
  }

  private collectSections(): string[] {
    const sections = new Set<string>();
    for (const doc of this.getDocuments()) {
      if (doc.sections) {
        for (const title of doc.sections.keys()) {
          sections.add(title);
        }
      }
    }
    return Array.from(sections).sort();
  }
}
