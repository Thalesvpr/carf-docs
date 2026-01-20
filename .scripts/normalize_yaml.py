#!/usr/bin/env python3
"""
normalize_yaml.py - Normaliza frontmatter YAML em todos os arquivos .md

Migra metadados do footer antigo (** Status:** no body) para YAML frontmatter.
O script e idempotente e pode ser executado multiplas vezes sem efeitos colaterais.

Uso: python .scripts/normalize_yaml.py [--dry-run]

Opcoes:
    --dry-run    Mostra o que seria modificado sem alterar arquivos
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

# Directories to scan
SCAN_DIRS = ["CENTRAL", "PROJECTS"]

# Patterns to ignore (gitignore-style)
IGNORE_PATTERNS = [
    "SRC-CODE",
    "node_modules",
    ".vitepress",
    "dist",
    ".claude",
    ".git",
    ".obsidian",
    ".plugins",
    ".scripts",
    ".assets",
]

# Regex patterns for footer metadata
FOOTER_PATTERNS = {
    "status": re.compile(
        r"\*\*(?:Status(?:\s+do\s+arquivo)?|Status)(?::\*\*|\*\*:)\s*(\w+)", re.IGNORECASE
    ),
    "updated": re.compile(
        r"\*\*(?:Atualizado|Updated|Ultima\s+atualizacao|Última\s+atualização)(?::\*\*|\*\*:)\s*([\d-]+)",
        re.IGNORECASE,
    ),
    "description": re.compile(
        r"\*\*(?:Descricao|Descrição|Description)(?::\*\*|\*\*:)\s*(.+)", re.IGNORECASE
    ),
}

# Status normalization mapping
STATUS_MAPPING = {
    "pronto": "approved",
    "aprovado": "approved",
    "approved": "approved",
    "review": "review",
    "incompleto": "review",
    "incomplete": "review",
    "errado": "rejected",
    "rejected": "rejected",
    "wrong": "rejected",
}


def normalize_status(status: str) -> str:
    """Normalize status to lowercase standard value."""
    return STATUS_MAPPING.get(status.lower().strip(), "review")


def should_ignore(path: Path, root: Path) -> bool:
    """Check if path should be ignored based on patterns."""
    rel_path = path.relative_to(root)
    parts = rel_path.parts

    for pattern in IGNORE_PATTERNS:
        if pattern in parts:
            return True

    return False


def parse_existing_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse existing YAML frontmatter from content.
    Returns (metadata_dict, content_without_frontmatter).
    """
    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    lines = content.split("\n")
    end_idx = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return {}, content

    # Parse YAML manually (simple key: value)
    metadata = {}
    for line in lines[1:end_idx]:
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            metadata[key] = value

    # Content after frontmatter
    rest = "\n".join(lines[end_idx + 1 :]).lstrip("\n")

    return metadata, rest


def extract_footer_metadata(content: str) -> dict:
    """Extract metadata from footer patterns in content body."""
    metadata = {}

    for key, pattern in FOOTER_PATTERNS.items():
        match = pattern.search(content)
        if match:
            value = match.group(1).strip()
            if value:
                metadata[key] = value

    return metadata


def remove_footer(content: str) -> str:
    """Remove all footer metadata sections from content, preserving GENERATED blocks."""
    lines = content.split("\n")
    result_lines = []

    # Track GENERATED block boundaries
    generated_start = -1
    generated_end = -1

    for i, line in enumerate(lines):
        if "<!-- GENERATED:START" in line:
            generated_start = i
        elif "<!-- GENERATED:END" in line:
            generated_end = i

    # Find all footer sections (--- followed by metadata)
    footer_ranges = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check if this is a --- that might start a footer
        if line == "---":
            # Look ahead for metadata patterns
            metadata_found = False
            j = i + 1
            while j < len(lines) and j < i + 5:  # Check next 5 lines
                check_line = lines[j]
                # Stop if we hit GENERATED block
                if "<!-- GENERATED" in check_line:
                    break
                for pattern in FOOTER_PATTERNS.values():
                    if pattern.search(check_line):
                        metadata_found = True
                        break
                if metadata_found:
                    break
                j += 1

            if metadata_found:
                # Find the end of this footer section
                footer_start = i
                footer_end = j

                # Extend to include all consecutive metadata lines
                while footer_end < len(lines):
                    check_line = lines[footer_end]
                    has_meta = False
                    for pattern in FOOTER_PATTERNS.values():
                        if pattern.search(check_line):
                            has_meta = True
                            break
                    if has_meta or check_line.strip() == "":
                        footer_end += 1
                    else:
                        break

                # Don't include ranges that overlap with GENERATED block
                if generated_start == -1 or footer_end <= generated_start or footer_start > generated_end:
                    footer_ranges.append((footer_start, footer_end))
                i = footer_end
                continue
        i += 1

    # Also find trailing metadata without ---
    if not footer_ranges or (footer_ranges and footer_ranges[-1][1] < len(lines)):
        i = len(lines) - 1
        while i >= 0:
            line = lines[i]
            has_meta = False
            for pattern in FOOTER_PATTERNS.values():
                if pattern.search(line):
                    has_meta = True
                    break
            if has_meta or line.strip() == "" or line.strip() == "---":
                i -= 1
            else:
                break

        trailing_start = i + 1
        if trailing_start < len(lines):
            # Check this doesn't overlap with GENERATED block
            if generated_end == -1 or trailing_start > generated_end:
                # Check it's not already covered
                already_covered = any(s <= trailing_start < e for s, e in footer_ranges)
                if not already_covered:
                    footer_ranges.append((trailing_start, len(lines)))

    # Build result excluding footer ranges
    footer_ranges.sort()

    i = 0
    for start, end in footer_ranges:
        result_lines.extend(lines[i:start])
        i = end
    result_lines.extend(lines[i:])

    # Clean up: remove trailing empty lines and standalone ---
    while result_lines and result_lines[-1].strip() in ("", "---"):
        result_lines.pop()

    # Remove standalone metadata lines (not preceded by ---)
    cleaned = []
    for line in result_lines:
        is_metadata_line = False
        for pattern in FOOTER_PATTERNS.values():
            if pattern.search(line):
                is_metadata_line = True
                break
        if not is_metadata_line:
            cleaned.append(line)

    # Clean up --- followed by empty lines before GENERATED block
    result_lines = cleaned
    cleaned = []
    skip_next_separator = False
    for i, line in enumerate(result_lines):
        if line.strip() == "---":
            # Check if next non-empty line is GENERATED
            for j in range(i + 1, len(result_lines)):
                if result_lines[j].strip():
                    if "<!-- GENERATED" in result_lines[j] or "<!-- CARF" in result_lines[j]:
                        skip_next_separator = True
                    break
        if skip_next_separator and line.strip() == "---":
            skip_next_separator = False
            continue
        cleaned.append(line)

    # Final cleanup: remove trailing empty lines
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()

    return "\n".join(cleaned)


def create_frontmatter(metadata: dict) -> str:
    """Create YAML frontmatter string from metadata dict."""
    lines = ["---"]

    # Status (required)
    status = normalize_status(metadata.get("status", "review"))
    lines.append(f"status: {status}")

    # Updated (required)
    updated = metadata.get("updated", date.today().isoformat())
    # Validate date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", updated):
        updated = date.today().isoformat()
    lines.append(f"updated: {updated}")

    # Description (optional)
    description = metadata.get("description", "").strip()
    if description:
        # Escape quotes in description
        description = description.replace('"', '\\"')
        lines.append(f'description: "{description}"')

    lines.append("---")
    return "\n".join(lines)


def process_file(filepath: Path, dry_run: bool = False) -> Optional[str]:
    """
    Process a single markdown file.
    Returns a status message if changes were made, None otherwise.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return f"ERROR: Could not read {filepath}: {e}"

    original_content = content

    # Parse existing frontmatter (if any)
    existing_meta, body = parse_existing_frontmatter(content)

    # Extract footer metadata from body
    footer_meta = extract_footer_metadata(body)

    # Merge metadata (footer takes precedence for migration)
    merged_meta = {**existing_meta}
    for key in ["status", "updated", "description"]:
        if key in footer_meta:
            merged_meta[key] = footer_meta[key]

    # If we already have frontmatter with status and no footer, skip
    if "status" in existing_meta and not footer_meta:
        return None

    # Remove footer from body
    clean_body = remove_footer(body)

    # Create new frontmatter
    new_frontmatter = create_frontmatter(merged_meta)

    # Combine
    new_content = f"{new_frontmatter}\n\n{clean_body}"

    # Normalize line endings and trailing newline
    new_content = new_content.rstrip() + "\n"

    # Check if content changed
    if new_content == original_content:
        return None

    # Write or report
    if dry_run:
        return f"WOULD MODIFY: {filepath}"
    else:
        try:
            filepath.write_text(new_content, encoding="utf-8")
            return f"MODIFIED: {filepath}"
        except Exception as e:
            return f"ERROR: Could not write {filepath}: {e}"


def find_markdown_files(root: Path) -> list[Path]:
    """Find all markdown files in scan directories."""
    files = []

    for scan_dir in SCAN_DIRS:
        dir_path = root / scan_dir
        if not dir_path.exists():
            continue

        for md_file in dir_path.rglob("*.md"):
            if not should_ignore(md_file, root):
                files.append(md_file)

    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="Normalize YAML frontmatter in markdown files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be modified without making changes",
    )
    args = parser.parse_args()

    # Find project root (where CENTRAL/ exists)
    root = Path.cwd()
    if not (root / "CENTRAL").exists():
        print("ERROR: CENTRAL directory not found. Run from project root.")
        sys.exit(1)

    print(f"Scanning {root}...")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    files = find_markdown_files(root)
    print(f"Found {len(files)} markdown files to process")
    print()

    modified = 0
    errors = 0

    for filepath in files:
        result = process_file(filepath, args.dry_run)
        if result:
            print(result)
            if result.startswith("ERROR"):
                errors += 1
            else:
                modified += 1

    print()
    print(f"Summary: {modified} files {'would be ' if args.dry_run else ''}modified, {errors} errors")

    if args.dry_run and modified > 0:
        print()
        print("Run without --dry-run to apply changes")


if __name__ == "__main__":
    main()
