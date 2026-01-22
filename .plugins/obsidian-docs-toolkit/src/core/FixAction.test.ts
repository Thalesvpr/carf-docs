import { describe, it, expect } from "vitest";
import {
  createAutoFix,
  createPickFix,
  createPromptFix,
  createScaffoldFix,
  isAutoFix,
  isPickFix,
  isPromptFix,
  FixAction
} from "./FixAction";

describe("FixAction", () => {
  describe("createAutoFix", () => {
    it("should create an auto fix with correct properties", () => {
      const fix = createAutoFix(
        "test-fix",
        "Test Fix",
        "status",
        "approved",
        "Set status to approved"
      );

      expect(fix.id).toBe("test-fix");
      expect(fix.label).toBe("Test Fix");
      expect(fix.kind).toBe("auto");
      expect(fix.targetField).toBe("status");
      expect(fix.autoValue).toBe("approved");
      expect(fix.description).toBe("Set status to approved");
    });

    it("should work without optional description", () => {
      const fix = createAutoFix("id", "Label", "field", "value");

      expect(fix.id).toBe("id");
      expect(fix.description).toBeUndefined();
    });
  });

  describe("createPickFix", () => {
    it("should create a pick fix with options", () => {
      const options = ["review", "approved", "rejected"];
      const fix = createPickFix(
        "pick-status",
        "Choose Status",
        "status",
        options,
        "Select a status"
      );

      expect(fix.id).toBe("pick-status");
      expect(fix.label).toBe("Choose Status");
      expect(fix.kind).toBe("pick");
      expect(fix.targetField).toBe("status");
      expect(fix.options).toEqual(options);
      expect(fix.description).toBe("Select a status");
    });

    it("should preserve options array", () => {
      const options = ["a", "b", "c"];
      const fix = createPickFix("id", "Label", "field", options);

      expect(fix.options).toEqual(options);
    });
  });

  describe("createPromptFix", () => {
    it("should create a prompt fix with hint", () => {
      const fix = createPromptFix(
        "prompt-id",
        "Enter ID",
        "id",
        "Enter a document ID (e.g., RF-001)",
        "Type the document identifier"
      );

      expect(fix.id).toBe("prompt-id");
      expect(fix.label).toBe("Enter ID");
      expect(fix.kind).toBe("prompt");
      expect(fix.targetField).toBe("id");
      expect(fix.promptHint).toBe("Enter a document ID (e.g., RF-001)");
      expect(fix.description).toBe("Type the document identifier");
    });
  });

  describe("createScaffoldFix", () => {
    it("should create a scaffold fix with template content", () => {
      const scaffold = "---\nstatus: review\nupdated: 2024-01-01\n---";
      const fix = createScaffoldFix(
        "scaffold-fm",
        "Insert Frontmatter",
        scaffold,
        "Insert YAML frontmatter"
      );

      expect(fix.id).toBe("scaffold-fm");
      expect(fix.label).toBe("Insert Frontmatter");
      expect(fix.kind).toBe("auto");
      expect(fix.targetField).toBe("__scaffold__");
      expect(fix.autoValue).toBe(scaffold);
      expect(fix.description).toBe("Insert YAML frontmatter");
    });
  });

  describe("type guards", () => {
    const autoFix = createAutoFix("auto", "Auto", "field", "value");
    const pickFix = createPickFix("pick", "Pick", "field", ["a", "b"]);
    const promptFix = createPromptFix("prompt", "Prompt", "field", "hint");

    describe("isAutoFix", () => {
      it("should return true for auto fixes", () => {
        expect(isAutoFix(autoFix)).toBe(true);
      });

      it("should return false for non-auto fixes", () => {
        expect(isAutoFix(pickFix)).toBe(false);
        expect(isAutoFix(promptFix)).toBe(false);
      });
    });

    describe("isPickFix", () => {
      it("should return true for pick fixes", () => {
        expect(isPickFix(pickFix)).toBe(true);
      });

      it("should return false for non-pick fixes", () => {
        expect(isPickFix(autoFix)).toBe(false);
        expect(isPickFix(promptFix)).toBe(false);
      });
    });

    describe("isPromptFix", () => {
      it("should return true for prompt fixes", () => {
        expect(isPromptFix(promptFix)).toBe(true);
      });

      it("should return false for non-prompt fixes", () => {
        expect(isPromptFix(autoFix)).toBe(false);
        expect(isPromptFix(pickFix)).toBe(false);
      });
    });
  });

  describe("edge cases", () => {
    it("should handle empty string values", () => {
      const fix = createAutoFix("id", "Label", "field", "");
      expect(fix.autoValue).toBe("");
    });

    it("should handle empty options array", () => {
      const fix = createPickFix("id", "Label", "field", []);
      expect(fix.options).toEqual([]);
    });

    it("should handle special characters in values", () => {
      const fix = createAutoFix(
        "id",
        "Label with \"quotes\"",
        "field",
        "value with\nnewline"
      );
      expect(fix.label).toBe("Label with \"quotes\"");
      expect(fix.autoValue).toBe("value with\nnewline");
    });

    it("should handle array values for autoValue", () => {
      const arrayValue = ["module1", "module2"];
      const fix = createAutoFix("id", "Label", "modules", arrayValue as unknown as string);
      expect(fix.autoValue).toEqual(arrayValue);
    });
  });
});
