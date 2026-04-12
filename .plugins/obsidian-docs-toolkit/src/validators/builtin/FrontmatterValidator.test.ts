import { describe, it, expect, vi, beforeEach } from "vitest";
import { App, TFile } from "obsidian";
import { FrontmatterValidator, FRONTMATTER_RULES } from "./FrontmatterValidator";
import { ValidatorContext } from "../base/Validator";
import { Document } from "../../core/Document";
import { Severity } from "../../core/Severity";
import { DocsLinterConfig, DEFAULT_CONFIG } from "../../config/ConfigSchema";

// Helper to create mock document
function createMockDocument(options: {
  path: string;
  hasFrontmatter: boolean;
  frontmatter?: Record<string, unknown>;
  content?: string;
}): Document {
  const file = new TFile(options.path);
  const frontmatter = options.frontmatter || {};
  const content = options.content || "";

  return {
    file,
    content,
    frontmatter,
    hasFrontmatter: options.hasFrontmatter,
    title: "Test Document",
    bodyContent: content,
    links: [],
    sections: [],
    hasFrontmatterField: (field: string) => field in frontmatter,
    getFrontmatterField: <T>(field: string) => frontmatter[field] as T,
    getSectionNames: () => [],
    hasSection: () => false,
    countWords: () => 100,
    countWordsInSection: () => 50,
    daysSinceUpdated: 1,
    daysSinceModified: 1
  } as unknown as Document;
}

// Helper to create validator context
function createContext(config?: Partial<DocsLinterConfig>): ValidatorContext {
  const fullConfig: DocsLinterConfig = {
    ...DEFAULT_CONFIG,
    ...config
  };

  return {
    app: new App(),
    config: fullConfig,
    documentTypeConfig: null,
    templateValidation: null,
    t: (key: string) => key,
    allDocuments: undefined
  };
}

describe("FrontmatterValidator", () => {
  let validator: FrontmatterValidator;

  beforeEach(() => {
    validator = new FrontmatterValidator();
  });

  describe("basic properties", () => {
    it("should have correct id and scope", () => {
      expect(validator.id).toBe("frontmatter");
      expect(validator.scope).toBe("file");
      expect(validator.isGlobal).toBe(false);
    });

    it("should have ERROR as default severity", () => {
      expect(validator.defaultSeverity).toBe(Severity.ERROR);
    });
  });

  describe("missing frontmatter", () => {
    it("should report error when frontmatter is missing", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: false
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      expect(issues).toHaveLength(1);
      expect(issues[0].messageKey).toBe("validators.frontmatter.missing");
      expect(issues[0].severity).toBe(Severity.ERROR);
    });

    it("should provide scaffold fix for missing frontmatter", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: false
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      expect(issues[0].hasFixes).toBe(true);
      expect(issues[0].fixes[0].kind).toBe("auto");
      expect(issues[0].fixes[0].id).toBe("insert-frontmatter");
      expect(issues[0].fixes[0].autoValue).toContain("status:");
      expect(issues[0].fixes[0].autoValue).toContain("updated:");
    });

    it("should include today's date in scaffold", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: false
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const scaffold = issues[0].fixes[0].autoValue as string;
      const today = new Date().toISOString().split("T")[0];

      expect(scaffold).toContain(`updated: ${today}`);
    });
  });

  describe("missing required fields", () => {
    it("should report error when status is missing", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { updated: "2024-01-01" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      const statusIssue = issues.find(i => i.messageParams.field === "status");
      expect(statusIssue).toBeDefined();
      expect(statusIssue?.messageKey).toBe("validators.frontmatter.required_field");
    });

    it("should provide auto fix and pick fix for missing status", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { updated: "2024-01-01" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const statusIssue = issues.find(i => i.messageParams.field === "status");

      expect(statusIssue?.fixes.length).toBeGreaterThanOrEqual(1);

      // Should have auto fix with default value
      const autoFix = statusIssue?.fixes.find(f => f.kind === "auto");
      expect(autoFix).toBeDefined();
      expect(autoFix?.autoValue).toBe("review");

      // Should have pick fix
      const pickFix = statusIssue?.fixes.find(f => f.kind === "pick");
      expect(pickFix).toBeDefined();
      expect(pickFix?.options).toContain("review");
      expect(pickFix?.options).toContain("approved");
    });

    it("should report error when updated is missing", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "review" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      const updatedIssue = issues.find(i => i.messageParams.field === "updated");
      expect(updatedIssue).toBeDefined();
    });

    it("should provide auto fix with today's date for missing updated", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "review" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const updatedIssue = issues.find(i => i.messageParams.field === "updated");
      const today = new Date().toISOString().split("T")[0];

      const autoFix = updatedIssue?.fixes.find(f => f.kind === "auto");
      expect(autoFix?.autoValue).toBe(today);
    });
  });

  describe("invalid field values", () => {
    it("should report error for invalid status value", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "invalid-status", updated: "2024-01-01" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      const invalidIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.invalid_enum" &&
        i.messageParams.field === "status"
      );
      expect(invalidIssue).toBeDefined();
    });

    it("should provide pick fix for invalid status", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "invalid", updated: "2024-01-01" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const invalidIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.invalid_enum"
      );

      expect(invalidIssue?.fixes[0].kind).toBe("pick");
      expect(invalidIssue?.fixes[0].options).toBeDefined();
    });

    it("should report error for invalid date format", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "01/15/2024" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      const dateIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.invalid_updated_format"
      );
      expect(dateIssue).toBeDefined();
    });

    it("should provide auto fix for invalid date format", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "January 15, 2024" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const dateIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.invalid_updated_format"
      );

      expect(dateIssue?.hasFixes).toBe(true);
      const autoFix = dateIssue?.fixes.find(f => f.kind === "auto");
      expect(autoFix).toBeDefined();
    });
  });

  describe("ID validation", () => {
    it("should infer ID from filename", async () => {
      const doc = createMockDocument({
        path: "docs/RF-001-requirement.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "2024-01-01" }
      });

      // Add 'id' to alwaysRequired
      const ctx = createContext({
        frontmatter: {
          alwaysRequired: ["status", "updated", "id"],
          defaults: { status: "review" },
          enums: {}
        }
      });

      const issues = await validator.validate(doc, ctx);
      const idIssue = issues.find(i => i.messageParams.field === "id");

      if (idIssue) {
        const autoFix = idIssue.fixes.find(f => f.kind === "auto");
        expect(autoFix?.autoValue).toBe("RF-001");
      }
    });

    it("should report ID mismatch", async () => {
      const doc = createMockDocument({
        path: "docs/RF-001-requirement.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "2024-01-01", id: "RF-002" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      const mismatchIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.id_mismatch"
      );
      expect(mismatchIssue).toBeDefined();
      expect(mismatchIssue?.messageParams.fmId).toBe("RF-002");
      expect(mismatchIssue?.messageParams.expectedId).toBe("RF-001");
    });

    it("should provide auto fix for ID mismatch", async () => {
      const doc = createMockDocument({
        path: "docs/RF-001-requirement.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "2024-01-01", id: "RF-002" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const mismatchIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.id_mismatch"
      );

      const autoFix = mismatchIssue?.fixes.find(f => f.kind === "auto");
      expect(autoFix?.autoValue).toBe("RF-001");
    });
  });

  describe("type validation", () => {
    it("should infer type from filename", async () => {
      const doc = createMockDocument({
        path: "docs/RF-001-requirement.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "2024-01-01", type: "RNF" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      const mismatchIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.type_mismatch"
      );
      expect(mismatchIssue).toBeDefined();
      expect(mismatchIssue?.messageParams.expectedType).toBe("RF");
    });
  });

  describe("valid frontmatter", () => {
    it("should return no issues for valid frontmatter", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: {
          status: "review",
          updated: "2024-01-15"
        }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      expect(issues).toHaveLength(0);
    });

    it("should accept all valid status values", async () => {
      const validStatuses = ["review", "approved", "rejected", "template", "deprecated", "superseded"];

      for (const status of validStatuses) {
        const doc = createMockDocument({
          path: "docs/test.md",
          hasFrontmatter: true,
          frontmatter: { status, updated: "2024-01-15" }
        });
        const ctx = createContext();

        const issues = await validator.validate(doc, ctx);
        const statusIssue = issues.find(i => i.messageParams.field === "status");

        expect(statusIssue).toBeUndefined();
      }
    });

    it("should be case-insensitive for status values", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: true,
        frontmatter: { status: "REVIEW", updated: "2024-01-15" }
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);
      const invalidStatus = issues.find(i =>
        i.messageKey === "validators.frontmatter.invalid_enum"
      );

      expect(invalidStatus).toBeUndefined();
    });
  });

  describe("rule configuration", () => {
    it("should respect disabled rules", async () => {
      const doc = createMockDocument({
        path: "docs/RF-001-test.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "2024-01-01", id: "RF-999" }
      });

      const ctx = createContext({
        validators: {
          frontmatter: {
            enabled: true,
            rules: {
              [FRONTMATTER_RULES.ID_MISMATCH]: { enabled: false }
            }
          }
        }
      });

      const issues = await validator.validate(doc, ctx);

      const mismatchIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.id_mismatch"
      );
      expect(mismatchIssue).toBeUndefined();
    });

    it("should respect custom severity for rules", async () => {
      const doc = createMockDocument({
        path: "docs/RF-001-test.md",
        hasFrontmatter: true,
        frontmatter: { status: "review", updated: "2024-01-01", id: "RF-999" }
      });

      const ctx = createContext({
        validators: {
          frontmatter: {
            enabled: true,
            rules: {
              [FRONTMATTER_RULES.ID_MISMATCH]: { severity: Severity.INFO }
            }
          }
        }
      });

      const issues = await validator.validate(doc, ctx);

      const mismatchIssue = issues.find(i =>
        i.messageKey === "validators.frontmatter.id_mismatch"
      );
      expect(mismatchIssue?.severity).toBe(Severity.INFO);
    });
  });

  describe("evidence", () => {
    it("should include evidence for debugging", async () => {
      const doc = createMockDocument({
        path: "docs/test.md",
        hasFrontmatter: false
      });
      const ctx = createContext();

      const issues = await validator.validate(doc, ctx);

      expect(issues[0].evidence).toBeDefined();
      expect(issues[0].evidence).toContain("No ---");
    });
  });
});
