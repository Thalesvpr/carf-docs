import { App, Modal } from "obsidian";

/**
 * Modal for text input
 * Used for PROMPT type fixes (e.g., entering ID)
 */
export class PromptModal extends Modal {
  private title: string;
  private placeholder: string;
  private initialValue: string;
  private onSubmit: (value: string | null) => void;
  private inputEl: HTMLInputElement | null = null;

  constructor(
    app: App,
    title: string,
    placeholder: string,
    onSubmit: (value: string | null) => void,
    initialValue: string = ""
  ) {
    super(app);
    this.title = title;
    this.placeholder = placeholder;
    this.onSubmit = onSubmit;
    this.initialValue = initialValue;
  }

  onOpen(): void {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("docs-prompt-modal");

    // Title
    contentEl.createEl("h3", { text: this.title, cls: "docs-modal-title" });

    // Input container
    const inputContainer = contentEl.createDiv({ cls: "docs-prompt-input-container" });

    this.inputEl = inputContainer.createEl("input", {
      type: "text",
      placeholder: this.placeholder,
      cls: "docs-prompt-input",
      value: this.initialValue
    });

    this.inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        this.submit();
      } else if (e.key === "Escape") {
        e.preventDefault();
        this.cancel();
      }
    });

    // Focus input
    setTimeout(() => {
      this.inputEl?.focus();
      this.inputEl?.select();
    }, 10);

    // Buttons
    const buttonRow = contentEl.createDiv({ cls: "docs-modal-buttons" });

    const cancelBtn = buttonRow.createEl("button", {
      text: "Cancel",
      cls: "docs-modal-btn"
    });
    cancelBtn.addEventListener("click", () => this.cancel());

    const submitBtn = buttonRow.createEl("button", {
      text: "Apply",
      cls: "docs-modal-btn docs-modal-btn-primary"
    });
    submitBtn.addEventListener("click", () => this.submit());
  }

  private submit(): void {
    const value = this.inputEl?.value.trim() || "";
    if (value) {
      this.onSubmit(value);
    } else {
      this.onSubmit(null);
    }
    this.close();
  }

  private cancel(): void {
    this.onSubmit(null);
    this.close();
  }

  onClose(): void {
    const { contentEl } = this;
    contentEl.empty();
  }
}

/**
 * Helper function to show prompt modal and return promise
 */
export function showPromptModal(
  app: App,
  title: string,
  placeholder: string,
  initialValue: string = ""
): Promise<string | null> {
  return new Promise((resolve) => {
    const modal = new PromptModal(app, title, placeholder, resolve, initialValue);
    modal.open();
  });
}
