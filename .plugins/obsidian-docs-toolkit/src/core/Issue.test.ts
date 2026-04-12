import { describe, it, expect } from "vitest";
import { TFile } from "obsidian";
import { Issue, calculateIssueSummary, IssueSummary } from "./Issue";
import { Severity } from "./Severity";
import { createAutoFix, createPickFix, createPromptFix } from "./FixAction";

// Helper to create a mock TFile
function createMockFile(path: string): TFile {
  const file = new TFile(path);
  return file;
}

describe("Issue", () => {
  const mockFile = createMockFile("docs/test.md");

  describe("constructor", () => {
    it("should create an issue with all properties", () => {
      const fixes = [createAutoFix("fix1", "Fix", "field", "value")];
      const issue = new Issue(
        mockFile,
        "frontmatter",
        Severity.ERROR,
        "validators.frontmatter.missing",
        { field: "status" },
        5,
        10,
        "validators.frontmatter.suggestion",
        { hint: "add status" },
        fixes,
        "No frontmatter found"
      );

      expect(issue.file).toBe(mockFile);
      expect(issue.validator).toBe("frontmatter");
      expect(issue.severity).toBe(Severity.ERROR);
      expect(issue.messageKey).toBe("validators.frontmatter.missing");
      expect(issue.messageParams).toEqual({ field: "status" });
      expect(issue.line).toBe(5);
      expect(issue.column).toBe(10);
      expect(issue.suggestionKey).toBe("validators.frontmatter.suggestion");
      expect(issue.suggestionParams).toEqual({ hint: "add status" });
      expect(issue.fixes).toEqual(fixes);
      expect(issue.evidence).toBe("No frontmatter found");
    });

    it("should use default values for optional parameters", () => {
      const issue = new Issue(
        mockFile,
        "naming",
        Severity.WARNING,
        "validators.naming.invalid"
      );

      expect(issue.messageParams).toEqual({});
      expect(issue.line).toBeNull();
      expect(issue.column).toBeNull();
      expect(issue.suggestionKey).toBeNull();
      expect(issue.suggestionParams).toEqual({});
      expect(issue.fixes).toEqual([]);
      expect(issue.evidence).toBeUndefined();
    });
  });

  describe("static factory methods", () => {
    describe("error", () => {
      it("should create an error issue", () => {
        const issue = Issue.error(
          mockFile,
          "frontmatter",
          "validators.frontmatter.missing",
          { field: "status" }
        );

        expect(issue.severity).toBe(Severity.ERROR);
        expect(issue.validator).toBe("frontmatter");
      });

      it("should support all optional parameters", () => {
        const fixes = [createAutoFix("fix", "Fix", "field", "value")];
        const issue = Issue.error(
          mockFile,
          "validator",
          "message.key",
          { param: "value" },
          10,
          "suggestion.key",
          { hint: "fix it" },
          fixes,
          "evidence"
        );

        expect(issue.line).toBe(10);
        expect(issue.suggestionKey).toBe("suggestion.key");
        expect(issue.fixes).toEqual(fixes);
        expect(issue.evidence).toBe("evidence");
      });
    });

    describe("warning", () => {
      it("should create a warning issue", () => {
        const issue = Issue.warning(
          mockFile,
          "naming",
          "validators.naming.pattern_mismatch"
        );

        expect(issue.severity).toBe(Severity.WARNING);
      });
    });

    describe("info", () => {
      it("should create an info issue", () => {
        const issue = Issue.info(
          mockFile,
          "stale",
          "validators.stale.outdated"
        );

        expect(issue.severity).toBe(Severity.INFO);
      });
    });
  });

  describe("fix-related getters", () => {
    describe("hasFixes", () => {
      it("should return true when issue has fixes", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message",
          {},
          null,
          null,
          null,
          {},
          [createAutoFix("fix", "Fix", "field", "value")]
        );

        expect(issue.hasFixes).toBe(true);
      });

      it("should return false when issue has no fixes", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message"
        );

        expect(issue.hasFixes).toBe(false);
      });
    });

    describe("hasOnlyAutoFixes", () => {
      it("should return true when all fixes are auto", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message",
          {},
          null,
          null,
          null,
          {},
          [
            createAutoFix("fix1", "Fix 1", "field1", "value1"),
            createAutoFix("fix2", "Fix 2", "field2", "value2")
          ]
        );

        expect(issue.hasOnlyAutoFixes).toBe(true);
      });

      it("should return false when some fixes are not auto", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message",
          {},
          null,
          null,
          null,
          {},
          [
            createAutoFix("fix1", "Fix 1", "field1", "value1"),
            createPickFix("fix2", "Fix 2", "field2", ["a", "b"])
          ]
        );

        expect(issue.hasOnlyAutoFixes).toBe(false);
      });

      it("should return false when no fixes", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message"
        );

        expect(issue.hasOnlyAutoFixes).toBe(false);
      });
    });

    describe("autoFixes", () => {
      it("should return only auto fixes", () => {
        const autoFix1 = createAutoFix("auto1", "Auto 1", "field1", "value1");
        const autoFix2 = createAutoFix("auto2", "Auto 2", "field2", "value2");
        const pickFix = createPickFix("pick", "Pick", "field3", ["a", "b"]);
        const promptFix = createPromptFix("prompt", "Prompt", "field4", "hint");

        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message",
          {},
          null,
          null,
          null,
          {},
          [autoFix1, pickFix, autoFix2, promptFix]
        );

        expect(issue.autoFixes).toEqual([autoFix1, autoFix2]);
      });

      it("should return empty array when no auto fixes", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message",
          {},
          null,
          null,
          null,
          {},
          [createPickFix("pick", "Pick", "field", ["a", "b"])]
        );

        expect(issue.autoFixes).toEqual([]);
      });
    });
  });

  describe("display getters", () => {
    describe("location", () => {
      it("should return filename with line number when line is set", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message",
          {},
          42
        );

        expect(issue.location).toBe("test.md:42");
      });

      it("should return only filename when line is null", () => {
        const issue = new Issue(
          mockFile,
          "validator",
          Severity.ERROR,
          "message"
        );

        expect(issue.location).toBe("test.md");
      });
    });

    describe("icon", () => {
      it("should return ✗ for errors", () => {
        const issue = new Issue(mockFile, "v", Severity.ERROR, "m");
        expect(issue.icon).toBe("✗");
      });

      it("should return ⚠ for warnings", () => {
        const issue = new Issue(mockFile, "v", Severity.WARNING, "m");
        expect(issue.icon).toBe("⚠");
      });

      it("should return ℹ for info", () => {
        const issue = new Issue(mockFile, "v", Severity.INFO, "m");
        expect(issue.icon).toBe("ℹ");
      });
    });

    describe("severityClass", () => {
      it("should return correct class for each severity", () => {
        expect(new Issue(mockFile, "v", Severity.ERROR, "m").severityClass).toBe("docs-error");
        expect(new Issue(mockFile, "v", Severity.WARNING, "m").severityClass).toBe("docs-warning");
        expect(new Issue(mockFile, "v", Severity.INFO, "m").severityClass).toBe("docs-info");
      });
    });
  });

  describe("compare", () => {
    it("should sort by severity first (errors before warnings before info)", () => {
      const error = new Issue(createMockFile("z.md"), "z", Severity.ERROR, "m");
      const warning = new Issue(createMockFile("a.md"), "a", Severity.WARNING, "m");
      const info = new Issue(createMockFile("b.md"), "b", Severity.INFO, "m");

      const sorted = [info, warning, error].sort(Issue.compare);

      expect(sorted[0].severity).toBe(Severity.ERROR);
      expect(sorted[1].severity).toBe(Severity.WARNING);
      expect(sorted[2].severity).toBe(Severity.INFO);
    });

    it("should sort by validator name within same severity", () => {
      const a = new Issue(createMockFile("z.md"), "alpha", Severity.ERROR, "m");
      const b = new Issue(createMockFile("a.md"), "beta", Severity.ERROR, "m");
      const c = new Issue(createMockFile("m.md"), "gamma", Severity.ERROR, "m");

      const sorted = [c, a, b].sort(Issue.compare);

      expect(sorted[0].validator).toBe("alpha");
      expect(sorted[1].validator).toBe("beta");
      expect(sorted[2].validator).toBe("gamma");
    });

    it("should sort by file path within same severity and validator", () => {
      const a = new Issue(createMockFile("docs/a.md"), "v", Severity.ERROR, "m");
      const b = new Issue(createMockFile("docs/b.md"), "v", Severity.ERROR, "m");
      const c = new Issue(createMockFile("docs/c.md"), "v", Severity.ERROR, "m");

      const sorted = [c, a, b].sort(Issue.compare);

      expect(sorted[0].file.path).toBe("docs/a.md");
      expect(sorted[1].file.path).toBe("docs/b.md");
      expect(sorted[2].file.path).toBe("docs/c.md");
    });

    it("should sort by line number within same file", () => {
      const file = createMockFile("docs/test.md");
      const a = new Issue(file, "v", Severity.ERROR, "m", {}, 10);
      const b = new Issue(file, "v", Severity.ERROR, "m", {}, 5);
      const c = new Issue(file, "v", Severity.ERROR, "m", {}, 20);

      const sorted = [c, a, b].sort(Issue.compare);

      expect(sorted[0].line).toBe(5);
      expect(sorted[1].line).toBe(10);
      expect(sorted[2].line).toBe(20);
    });

    it("should handle null line numbers", () => {
      const file = createMockFile("docs/test.md");
      const a = new Issue(file, "v", Severity.ERROR, "m", {}, 10);
      const b = new Issue(file, "v", Severity.ERROR, "m", {}, null);

      const sorted = [a, b].sort(Issue.compare);

      expect(sorted[0].line).toBeNull();
      expect(sorted[1].line).toBe(10);
    });
  });
});

describe("calculateIssueSummary", () => {
  const mockFile = createMockFile("docs/test.md");

  it("should calculate correct summary", () => {
    const issues = [
      new Issue(mockFile, "v", Severity.ERROR, "m"),
      new Issue(mockFile, "v", Severity.ERROR, "m"),
      new Issue(mockFile, "v", Severity.WARNING, "m"),
      new Issue(mockFile, "v", Severity.WARNING, "m"),
      new Issue(mockFile, "v", Severity.WARNING, "m"),
      new Issue(mockFile, "v", Severity.INFO, "m")
    ];

    const summary = calculateIssueSummary(issues);

    expect(summary).toEqual({
      total: 6,
      errors: 2,
      warnings: 3,
      info: 1
    });
  });

  it("should return zeros for empty array", () => {
    const summary = calculateIssueSummary([]);

    expect(summary).toEqual({
      total: 0,
      errors: 0,
      warnings: 0,
      info: 0
    });
  });

  it("should handle issues of single severity", () => {
    const issues = [
      new Issue(mockFile, "v", Severity.WARNING, "m"),
      new Issue(mockFile, "v", Severity.WARNING, "m")
    ];

    const summary = calculateIssueSummary(issues);

    expect(summary.total).toBe(2);
    expect(summary.errors).toBe(0);
    expect(summary.warnings).toBe(2);
    expect(summary.info).toBe(0);
  });
});
