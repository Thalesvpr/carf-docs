#!/usr/bin/env python3
"""
Lint documentation quality for CARF project

Validates:
1. CENTRAL/ has ZERO code blocks (except tables/lists)
2. PROJECTS/FEATURES/ have >= 100 words (not stub files)
3. PROJECTS/CONCEPTS/ and HOW-TO/ follow dense paragraph pattern
4. PROJECTS/LIB/TS/*/CONCEPTS/ can have code blocks (API reference exception)
5. READMEs have <= 5 links per paragraph
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

class DocumentationLinter:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.errors = []
        self.warnings = []

    def check_code_blocks_in_central(self) -> List[Tuple[Path, int, str]]:
        """Check for code blocks in CENTRAL/ (should be ZERO)"""
        violations = []
        central_dir = self.root / "CENTRAL"

        if not central_dir.exists():
            return violations

        for md_file in central_dir.rglob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            in_code_block = False
            for i, line in enumerate(lines, 1):
                if line.startswith('```'):
                    if not in_code_block:
                        # Found code block start
                        lang = line[3:].strip()
                        violations.append((md_file, i, f"Code block (language: {lang or 'none'})"))
                    in_code_block = not in_code_block

        return violations

    def check_features_word_count(self) -> List[Tuple[Path, int]]:
        """Check FEATURES files have >= 100 words"""
        violations = []

        for features_dir in self.root.glob("PROJECTS/*/DOCS/FEATURES"):
            if not features_dir.exists():
                continue

            for md_file in features_dir.glob("*.md"):
                if md_file.name == "README.md":
                    continue

                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Remove markdown links, headers, frontmatter
                text = re.sub(r'\[.*?\]\(.*?\)', '', content)
                text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
                text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)

                words = text.split()
                word_count = len(words)

                if word_count < 100:
                    violations.append((md_file, word_count))

        return violations

    def check_links_per_paragraph(self) -> List[Tuple[Path, int, int]]:
        """Check READMEs have <= 5 links per paragraph"""
        violations = []

        readme_files = list(self.root.glob("**/README.md"))

        for readme in readme_files:
            # Skip WEBDOCS/SRC-CODE
            if "WEBDOCS/SRC-CODE" in str(readme):
                continue

            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split by double newline to get paragraphs
            paragraphs = re.split(r'\n\s*\n', content)

            for i, para in enumerate(paragraphs, 1):
                # Count markdown links
                links = re.findall(r'\[.*?\]\(.*?\)', para)
                link_count = len(links)

                if link_count > 5:
                    violations.append((readme, i, link_count))

        return violations

    def check_lib_concepts_exception(self, file_path: Path) -> bool:
        """Check if file is in PROJECTS/LIB/TS/*/CONCEPTS/ (allowed to have code blocks)"""
        parts = file_path.parts
        try:
            if "PROJECTS" in parts and "LIB" in parts and "TS" in parts and "CONCEPTS" in parts:
                return True
        except:
            pass
        return False

    def check_excessive_line_breaks(self) -> List[Tuple[Path, int]]:
        """Check for excessive consecutive line breaks (not dense paragraph)"""
        violations = []

        # Check CENTRAL/ and PROJECTS/*/DOCS/ (exclude SRC-CODE, node_modules)
        patterns = [
            self.root / "CENTRAL" / "**" / "*.md",
            self.root / "PROJECTS" / "*" / "DOCS" / "**" / "*.md"
        ]

        for pattern in patterns:
            for md_file in self.root.glob(str(pattern.relative_to(self.root))):
                # Skip WEBDOCS/SRC-CODE
                if "SRC-CODE" in str(md_file) or "node_modules" in str(md_file):
                    continue

                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Count consecutive empty lines (3+ is excessive for dense paragraph)
                    max_consecutive = 0
                    current_consecutive = 0

                    for line in content.split('\n'):
                        if line.strip() == '':
                            current_consecutive += 1
                            max_consecutive = max(max_consecutive, current_consecutive)
                        else:
                            current_consecutive = 0

                    if max_consecutive >= 3:
                        violations.append((md_file, max_consecutive))
                except:
                    pass

        return violations

    def run(self):
        """Run all lint checks"""
        print("Running CARF documentation linter...")
        print("=" * 80)

        # Check 1: Code blocks in CENTRAL/
        print("\n[1/3] Checking CENTRAL/ for code blocks...")
        code_block_violations = self.check_code_blocks_in_central()

        if code_block_violations:
            print(f"  [ERROR] Found {len(code_block_violations)} code block violations in CENTRAL/")
            for file_path, line_num, lang in code_block_violations:
                rel_path = file_path.relative_to(self.root)
                self.errors.append(f"{rel_path}:{line_num} - {lang}")
        else:
            print("  [OK] No code blocks found in CENTRAL/")

        # Check 2: FEATURES word count
        print("\n[2/3] Checking PROJECTS/*/DOCS/FEATURES/ word count...")
        features_violations = self.check_features_word_count()

        if features_violations:
            print(f"  [ERROR] Found {len(features_violations)} stub FEATURES files (< 100 words)")
            for file_path, word_count in features_violations:
                rel_path = file_path.relative_to(self.root)
                self.errors.append(f"{rel_path} - Only {word_count} words (minimum 100)")
        else:
            print("  [OK] All FEATURES files have adequate content")

        # Check 3: Excessive line breaks (dense paragraph)
        print("\n[3/4] Checking for excessive line breaks (non-dense)...")
        linebreak_violations = self.check_excessive_line_breaks()

        if linebreak_violations:
            print(f"  [WARN] Found {len(linebreak_violations)} files with 3+ consecutive blank lines")
            for file_path, max_breaks in linebreak_violations:
                rel_path = file_path.relative_to(self.root)
                self.warnings.append(f"{rel_path} - {max_breaks} consecutive blank lines (dense paragraph violation)")
        else:
            print("  [OK] No excessive line breaks found")

        # Check 4: Links per paragraph
        print("\n[4/4] Checking README files for excessive links...")
        link_violations = self.check_links_per_paragraph()

        if link_violations:
            print(f"  [WARN] Found {len(link_violations)} paragraphs with > 5 links")
            for file_path, para_num, link_count in link_violations:
                rel_path = file_path.relative_to(self.root)
                self.warnings.append(f"{rel_path}:para{para_num} - {link_count} links (max 5 recommended)")
        else:
            print("  [OK] No excessive link paragraphs found")

        # Print summary
        print("\n" + "=" * 80)
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print("\n[ERRORS]:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("\n[WARNINGS]:")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print("\n[SUCCESS] All checks passed!")
            return 0
        elif self.errors:
            print("\n[FAIL] Lint failed with errors")
            return 1
        else:
            print("\n[SUCCESS] Lint passed with warnings")
            return 0

def main():
    linter = DocumentationLinter()
    exit_code = linter.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
