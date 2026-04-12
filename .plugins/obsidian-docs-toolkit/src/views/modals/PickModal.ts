import { App, Modal, Setting } from "obsidian";

/**
 * Modal for selecting one or multiple options
 * Used for PICK type fixes (e.g., selecting status, type, modules)
 */
export class PickModal extends Modal {
  private title: string;
  private options: string[];
  private multiSelect: boolean;
  private selected: Set<string> = new Set();
  private onSubmit: (selected: string | string[] | null) => void;

  constructor(
    app: App,
    title: string,
    options: string[],
    onSubmit: (selected: string | string[] | null) => void,
    multiSelect: boolean = false,
    preselected?: string[]
  ) {
    super(app);
    this.title = title;
    this.options = options;
    this.onSubmit = onSubmit;
    this.multiSelect = multiSelect;

    if (preselected) {
      preselected.forEach(v => this.selected.add(v));
    }
  }

  onOpen(): void {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("docs-pick-modal");

    // Title
    contentEl.createEl("h3", { text: this.title, cls: "docs-modal-title" });

    // Description
    if (this.multiSelect) {
      contentEl.createEl("p", {
        text: "Select one or more options:",
        cls: "docs-modal-desc"
      });
    } else {
      contentEl.createEl("p", {
        text: "Select an option:",
        cls: "docs-modal-desc"
      });
    }

    // Options container
    const optionsContainer = contentEl.createDiv({ cls: "docs-pick-options" });

    for (const option of this.options) {
      const optionEl = optionsContainer.createDiv({ cls: "docs-pick-option" });

      if (this.multiSelect) {
        // Checkbox for multi-select
        const checkbox = optionEl.createEl("input", {
          type: "checkbox",
          cls: "docs-pick-checkbox"
        });
        checkbox.checked = this.selected.has(option);
        checkbox.addEventListener("change", () => {
          if (checkbox.checked) {
            this.selected.add(option);
          } else {
            this.selected.delete(option);
          }
          this.updateButtonState();
        });

        const label = optionEl.createEl("label", {
          text: option,
          cls: "docs-pick-label"
        });
        label.addEventListener("click", () => {
          checkbox.checked = !checkbox.checked;
          checkbox.dispatchEvent(new Event("change"));
        });
      } else {
        // Radio-style button for single select
        const button = optionEl.createEl("button", {
          text: option,
          cls: `docs-pick-btn ${this.selected.has(option) ? "selected" : ""}`
        });
        button.addEventListener("click", () => {
          this.selected.clear();
          this.selected.add(option);
          // Submit immediately on single select
          this.submit();
        });
      }
    }

    // Buttons for multi-select
    if (this.multiSelect) {
      const buttonRow = contentEl.createDiv({ cls: "docs-modal-buttons" });

      const cancelBtn = buttonRow.createEl("button", {
        text: "Cancel",
        cls: "docs-modal-btn"
      });
      cancelBtn.addEventListener("click", () => {
        this.onSubmit(null);
        this.close();
      });

      const submitBtn = buttonRow.createEl("button", {
        text: "Apply",
        cls: "docs-modal-btn docs-modal-btn-primary"
      });
      submitBtn.addEventListener("click", () => this.submit());
      submitBtn.id = "docs-pick-submit";
      this.updateButtonState();
    }
  }

  private updateButtonState(): void {
    const submitBtn = this.contentEl.querySelector("#docs-pick-submit") as HTMLButtonElement;
    if (submitBtn) {
      submitBtn.disabled = this.selected.size === 0;
    }
  }

  private submit(): void {
    if (this.selected.size === 0) {
      this.onSubmit(null);
    } else if (this.multiSelect) {
      this.onSubmit(Array.from(this.selected));
    } else {
      this.onSubmit(Array.from(this.selected)[0]);
    }
    this.close();
  }

  onClose(): void {
    const { contentEl } = this;
    contentEl.empty();
  }
}

/**
 * Helper function to show pick modal and return promise
 */
export function showPickModal(
  app: App,
  title: string,
  options: string[],
  multiSelect: boolean = false,
  preselected?: string[]
): Promise<string | string[] | null> {
  return new Promise((resolve) => {
    const modal = new PickModal(app, title, options, resolve, multiSelect, preselected);
    modal.open();
  });
}
