#!/usr/bin/env python3
"""
Valida metadados obrigatórios (Última atualização: YYYY-MM-DD)
"""
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

# Arquivos importantes que DEVEM ter metadata
IMPORTANT_FILE_PATTERNS = [
    "*/README.md",
    "CENTRAL/REQUIREMENTS/**/*.md",
    "PROJECTS/*/DOCS/FEATURES/*.md",
    "PROJECTS/*/DOCS/ARCHITECTURE/*.md",
    "CENTRAL/ARCHITECTURE/**/*.md",
]

def extract_last_update_date(content):
    """Extrai data de 'Última atualização: YYYY-MM-DD'"""
    pattern = r"Última atualização:\s*(\d{4}-\d{2}-\d{2})"
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None

def is_outdated(date_str, months=12):
    """Verifica se data está desatualizada (> N meses)"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        cutoff = datetime.now() - timedelta(days=months * 30)
        return date < cutoff
    except:
        return False

def validate_metadata():
    errors = []
    warnings = []

    # Coleta arquivos importantes
    important_files = []
    for pattern in IMPORTANT_FILE_PATTERNS:
        important_files.extend(Path(".").glob(pattern))

    # Remove duplicatas
    important_files = list(set(important_files))

    # Exclui node_modules, SRC-CODE
    important_files = [
        f for f in important_files
        if "node_modules" not in str(f) and "SRC-CODE" not in str(f)
    ]

    print(f"[*] Validating metadata in {len(important_files)} important files...")
    print()

    missing_metadata = []
    outdated_metadata = []

    for file_path in important_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            rel_path = str(file_path).replace("\\", "/")

            date = extract_last_update_date(content)

            if not date:
                missing_metadata.append(rel_path)
            elif is_outdated(date, months=12):
                outdated_metadata.append({
                    "file": rel_path,
                    "date": date,
                })

        except Exception as e:
            warnings.append(f"Could not read {file_path}: {e}")

    if missing_metadata:
        for file in missing_metadata:
            errors.append(f"{file} missing 'Última atualização: YYYY-MM-DD'")

    if outdated_metadata:
        for item in outdated_metadata:
            warnings.append(
                f"{item['file']} outdated metadata (last update: {item['date']})"
            )

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_checked": len(important_files),
            "missing_metadata": len(missing_metadata),
            "outdated_metadata": len(outdated_metadata),
        }
    }

def main():
    print("="*80)
    print("[VALIDATION] Metadata")
    print("="*80)
    print()

    result = validate_metadata()

    errors = result["errors"]
    warnings = result["warnings"]
    stats = result["stats"]

    print(f"Total files checked: {stats['total_checked']}")
    print(f"Missing metadata: {stats['missing_metadata']}")
    print(f"Outdated metadata (>12 months): {stats['outdated_metadata']}")
    print()

    if errors:
        print(f"[ERRORS] {len(errors)} files missing metadata:")
        for error in errors[:15]:
            print(f"  [X] {error}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} outdated metadata:")
        for warning in warnings[:10]:
            print(f"  [WARN] {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more")
        print()

    if not errors and not warnings:
        print("[[OK]] All metadata is present and up to date")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
