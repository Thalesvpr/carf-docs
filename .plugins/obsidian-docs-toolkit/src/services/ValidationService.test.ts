import { describe, it, expect, vi, beforeEach } from "vitest";
import { App, TFile } from "obsidian";
import { ValidationService } from "./ValidationService";
import { ValidatorRegistry } from "../validators/ValidatorRegistry";
import { TemplateService } from "./TemplateService";
import { I18nService } from "../i18n/I18nService";
import { LocalValidator, GlobalValidator, ValidatorContext } from "../validators/base/Validator";
import { Document } from "../core/Document";
import { Issue } from "../core/Issue";
import { Severity } from "../core/Severity";
import { DocsLinterConfig, DEFAULT_CONFIG } from "../config/ConfigSchema";

// Mock validators for testing
class MockLocalValidator extends LocalValidator {
  readonly id = "mock-local";
  readonly nameKey = "mock.local.name";
  readonly descriptionKey = "mock.local.desc";
  readonly defaultSeverity = Severity.WARNING;

  validateFn: (doc: Document, ctx: ValidatorContext) => Promise<Issue[]>;

  constructor(validateFn?: (doc: Document, ctx: ValidatorContext) => Promise<Issue[]>) {
    super();
    this.validateFn = validateFn || (async () => []);
  }

  async validate(doc: Document, ctx: ValidatorContext): Promise<Issue[]> {
    return this.validateFn(doc, ctx);
  }
}

class MockGlobalValidator extends GlobalValidator {
  readonly id = "mock-global";
  readonly nameKey = "mock.global.name";
  readonly descriptionKey = "mock.global.desc";
  readonly defaultSeverity = Severity.INFO;

  validateAllFn: (docs: Document[], ctx: ValidatorContext) => Promise<Issue[]>;

  constructor(validateAllFn?: (docs: Document[], ctx: ValidatorContext) => Promise<Issue[]>) {
    super();
    this.validateAllFn = validateAllFn || (async () => []);
  }

  async validateAll(docs: Document[], ctx: ValidatorContext): Promise<Issue[]> {
    return this.validateAllFn(docs, ctx);
  }
}

class CrashingValidator extends LocalValidator {
  readonly id = "crashing";
  readonly nameKey = "crashing.name";
  readonly descriptionKey = "crashing.desc";
  readonly defaultSeverity = Severity.ERROR;

  async validate(): Promise<Issue[]> {
    throw new Error("Validator crashed!");
  }
}

class CrashingGlobalValidator extends GlobalValidator {
  readonly id = "crashing-global";
  readonly nameKey = "crashing.global.name";
  readonly descriptionKey = "crashing.global.desc";
  readonly defaultSeverity = Severity.ERROR;

  async validateAll(): Promise<Issue[]> {
    throw new Error("Global validator crashed!");
  }
}

// Helper to create mock document
function createMockDocument(path: string): Document {
  const file = new TFile(path);
  return {
    file,
    content: "---\nstatus: review\n---\n# Title\nContent",
    frontmatter: { status: "review" },
    hasFrontmatter: true,
    title: "Title",
    bodyContent: "# Title\nContent",
    links: [],
    sections: [],
    hasFrontmatterField: () => true,
    getFrontmatterField: () => "review",
    getSectionNames: () => [],
    hasSection: () => false,
    countWords: () => 10,
    countWordsInSection: () => 5,
    daysSinceUpdated: 1,
    daysSinceModified: 1
  } as unknown as Document;
}

describe("ValidationService", () => {
  let app: App;
  let registry: ValidatorRegistry;
  let templateService: TemplateService;
  let i18n: I18nService;
  let service: ValidationService;
  let config: DocsLinterConfig;

  beforeEach(() => {
    app = new App();
    registry = new ValidatorRegistry();
    templateService = {
      initialize: vi.fn().mockResolvedValue(undefined),
      getTemplateValidation: vi.fn().mockReturnValue(null),
      isTemplate: vi.fn().mockReturnValue(false),
      refreshTemplate: vi.fn().mockResolvedValue(undefined),
      removeTemplate: vi.fn()
    } as unknown as TemplateService;
    i18n = {
      t: vi.fn((key: string) => key),
      initialize: vi.fn(),
      setLocale: vi.fn()
    } as unknown as I18nService;
    config = { ...DEFAULT_CONFIG };

    service = new ValidationService(app, registry, templateService, i18n);
  });

  describe("validateAll", () => {
    it("should validate all documents with file-scope validators", async () => {
      const validator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "mock-local", Severity.WARNING, "test.message")
      ]);
      registry.register(validator);

      const docs = [
        createMockDocument("docs/a.md"),
        createMockDocument("docs/b.md")
      ];

      const result = await service.validateAll(docs, config);

      expect(result.allIssues).toHaveLength(2);
      expect(result.documentResults.size).toBe(2);
      expect(result.mode).toBe("vault");
    });

    it("should validate all documents with vault-scope validators", async () => {
      const validator = new MockGlobalValidator(async (docs, ctx) => {
        return docs.map(doc => new Issue(doc.file, "mock-global", Severity.INFO, "orphan"));
      });
      registry.register(validator);

      const docs = [createMockDocument("docs/a.md")];
      const result = await service.validateAll(docs, config);

      expect(result.allIssues).toHaveLength(1);
      expect(result.allIssues[0].validator).toBe("mock-global");
    });

    it("should catch validator crashes and create internal issues", async () => {
      const crashingValidator = new CrashingValidator();
      registry.register(crashingValidator);

      const docs = [createMockDocument("docs/test.md")];
      const result = await service.validateAll(docs, config);

      // Should not throw
      expect(result.internalIssues).toHaveLength(1);
      expect(result.internalIssues[0].validator).toBe("internal/crashing");
      expect(result.internalIssues[0].severity).toBe(Severity.ERROR);
    });

    it("should catch global validator crashes and create internal issues", async () => {
      const crashingValidator = new CrashingGlobalValidator();
      registry.register(crashingValidator);

      const docs = [createMockDocument("docs/test.md")];
      const result = await service.validateAll(docs, config);

      // Should not throw
      expect(result.internalIssues).toHaveLength(1);
      expect(result.internalIssues[0].validator).toBe("internal/crashing-global");
    });

    it("should continue validation after one validator crashes", async () => {
      const crashingValidator = new CrashingValidator();
      const workingValidator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "mock-local", Severity.WARNING, "works")
      ]);
      registry.register(crashingValidator);
      registry.register(workingValidator);

      const docs = [createMockDocument("docs/test.md")];
      const result = await service.validateAll(docs, config);

      // Working validator should still produce issues
      expect(result.allIssues).toHaveLength(1);
      expect(result.allIssues[0].validator).toBe("mock-local");
      // Crashing validator should produce internal issue
      expect(result.internalIssues).toHaveLength(1);
    });

    it("should sort issues by severity", async () => {
      const validator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "v", Severity.INFO, "info"),
        new Issue(doc.file, "v", Severity.ERROR, "error"),
        new Issue(doc.file, "v", Severity.WARNING, "warning")
      ]);
      registry.register(validator);

      const docs = [createMockDocument("docs/test.md")];
      const result = await service.validateAll(docs, config);

      expect(result.allIssues[0].severity).toBe(Severity.ERROR);
      expect(result.allIssues[1].severity).toBe(Severity.WARNING);
      expect(result.allIssues[2].severity).toBe(Severity.INFO);
    });

    it("should calculate summary correctly", async () => {
      const validator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "v", Severity.ERROR, "e1"),
        new Issue(doc.file, "v", Severity.ERROR, "e2"),
        new Issue(doc.file, "v", Severity.WARNING, "w1"),
        new Issue(doc.file, "v", Severity.INFO, "i1")
      ]);
      registry.register(validator);

      const docs = [createMockDocument("docs/test.md")];
      const result = await service.validateAll(docs, config);

      expect(result.summary).toEqual({
        total: 4,
        errors: 2,
        warnings: 1,
        info: 1
      });
    });
  });

  describe("validateCurrentFile", () => {
    it("should only run file-scope validators", async () => {
      const localValidator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "mock-local", Severity.WARNING, "local.issue")
      ]);
      const globalValidator = new MockGlobalValidator(async () => []);
      const globalValidateFn = vi.spyOn(globalValidator, "validateAll");

      registry.register(localValidator);
      registry.register(globalValidator);

      const doc = createMockDocument("docs/test.md");
      const result = await service.validateCurrentFile(doc, config);

      expect(result.issues).toHaveLength(1);
      expect(result.issues[0].validator).toBe("mock-local");
      // Global validator should NOT be called
      expect(globalValidateFn).not.toHaveBeenCalled();
    });

    it("should catch validator crashes in single file mode", async () => {
      const crashingValidator = new CrashingValidator();
      registry.register(crashingValidator);

      const doc = createMockDocument("docs/test.md");
      const result = await service.validateCurrentFile(doc, config);

      expect(result.issues).toHaveLength(0);
      expect(result.internalIssues).toHaveLength(1);
      expect(result.internalIssues[0].validator).toBe("internal/crashing");
    });

    it("should return proper summary", async () => {
      const validator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "v", Severity.ERROR, "e"),
        new Issue(doc.file, "v", Severity.WARNING, "w")
      ]);
      registry.register(validator);

      const doc = createMockDocument("docs/test.md");
      const result = await service.validateCurrentFile(doc, config);

      expect(result.summary).toEqual({
        total: 2,
        errors: 1,
        warnings: 1,
        info: 0
      });
    });
  });

  describe("validateDocument", () => {
    it("should validate a single document with file-scope validators", async () => {
      const validator = new MockLocalValidator(async (doc) => [
        new Issue(doc.file, "mock-local", Severity.WARNING, "test")
      ]);
      registry.register(validator);

      const doc = createMockDocument("docs/test.md");
      const issues = await service.validateDocument(doc, config);

      expect(issues).toHaveLength(1);
    });

    it("should pass allDocuments to context when provided", async () => {
      let receivedAllDocs: Document[] | undefined;
      const validator = new MockLocalValidator(async (doc, ctx) => {
        receivedAllDocs = ctx.allDocuments;
        return [];
      });
      registry.register(validator);

      const doc = createMockDocument("docs/test.md");
      const allDocs = [doc, createMockDocument("docs/other.md")];

      await service.validateDocument(doc, config, allDocs);

      expect(receivedAllDocs).toHaveLength(2);
    });
  });

  describe("validator ordering", () => {
    it("should run frontmatter validator first", async () => {
      const order: string[] = [];

      const frontmatterValidator = new MockLocalValidator(async () => {
        order.push("frontmatter");
        return [];
      });
      (frontmatterValidator as any).id = "frontmatter";

      const namingValidator = new MockLocalValidator(async () => {
        order.push("naming");
        return [];
      });
      (namingValidator as any).id = "naming";

      const otherValidator = new MockLocalValidator(async () => {
        order.push("other");
        return [];
      });
      (otherValidator as any).id = "other";

      // Register in wrong order to test sorting
      registry.register(otherValidator);
      registry.register(namingValidator);
      registry.register(frontmatterValidator);

      const docs = [createMockDocument("docs/test.md")];
      await service.validateAll(docs, config);

      expect(order[0]).toBe("frontmatter");
      expect(order[1]).toBe("naming");
      expect(order[2]).toBe("other");
    });
  });
});
