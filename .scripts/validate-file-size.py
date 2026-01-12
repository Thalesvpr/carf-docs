#!/usr/bin/env python3
"""
Valida tamanho de arquivos (min/max palavras) conforme tipo
"""
import sys
import re
from pathlib import Path

# Regras de tamanho por tipo de arquivo (baseado em VALIDATION-RULES.md)
SIZE_RULES = {
    "README": {"min": 150, "max": 500},
    "ADR": {"min": 450, "max": 700},
    "UC": {"min": 400, "max": 700},
    "RF": {"min": 100, "max": 350},
    "US": {"min": 80, "max": 250},
    "Entity": {"min": 200, "max": 500},
    "Feature": {"min": 500, "max": 1000},
    "HOW-TO": {"min": 300, "max": 900},
    "Concept": {"min": 250, "max": 550},
    "Business Rule": {"min": 300, "max": 700},
    "Architecture": {"min": 400, "max": 900},
}

def count_words(content):
    """Conta palavras excluindo code blocks e metadados"""
    # Remove code blocks
    content = re.sub(r"```[\s\S]*?```", "", content)

    # Remove frontmatter YAML
    content = re.sub(r"^---\n[\s\S]*?\n---\n", "", content)

    # Conta palavras
    words = content.split()
    return len(words)

def detect_file_type(file_path):
    """Detecta tipo de arquivo baseado em path e nome"""
    path_str = str(file_path).replace("\\", "/")
    name = file_path.name

    if name == "README.md":
        return "README"
    elif "/ADRs/" in path_str and name.startswith("ADR-"):
        return "ADR"
    elif "/USE-CASES/" in path_str and name.startswith("UC-"):
        return "UC"
    elif "/FUNCTIONAL-REQUIREMENTS/" in path_str and name.startswith("RF-"):
        return "RF"
    elif "/USER-STORIES/" in path_str and name.startswith("US-"):
        return "US"
    elif "/ENTITIES/" in path_str and re.match(r"\d{2}-", name):
        return "Entity"
    elif "/FEATURES/" in path_str and name != "README.md":
        return "Feature"
    elif "/HOW-TO/" in path_str and re.match(r"\d{2}-", name):
        return "HOW-TO"
    elif "/CONCEPTS/" in path_str and re.match(r"\d{2}-", name):
        return "Concept"
    elif "/BUSINESS-RULES/" in path_str:
        return "Business Rule"
    elif "/ARCHITECTURE/" in path_str and name != "README.md":
        return "Architecture"

    return None

def validate_file_size():
    errors = []
    warnings = []

    # Busca todos .md em CENTRAL e PROJECTS/*/DOCS
    md_files = list(Path("CENTRAL").glob("**/*.md"))
    md_files += list(Path("PROJECTS").glob("*/DOCS/**/*.md"))

    # Exclui node_modules, SRC-CODE
    md_files = [
        f for f in md_files
        if "node_modules" not in str(f) and "SRC-CODE" not in str(f)
    ]

    print(f"[*] Validating file sizes in {len(md_files)} files...")
    print()

    too_small = []
    too_large = []

    for md_file in md_files:
        file_type = detect_file_type(md_file)

        if not file_type:
            continue  # Tipo desconhecido, pula

        rules = SIZE_RULES.get(file_type)
        if not rules:
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            word_count = count_words(content)
            rel_path = str(md_file).replace("\\", "/")

            if word_count < rules["min"]:
                too_small.append({
                    "file": rel_path,
                    "type": file_type,
                    "actual": word_count,
                    "min": rules["min"],
                    "diff": rules["min"] - word_count,
                })
            elif word_count > rules["max"]:
                too_large.append({
                    "file": rel_path,
                    "type": file_type,
                    "actual": word_count,
                    "max": rules["max"],
                    "diff": word_count - rules["max"],
                })

        except Exception as e:
            warnings.append(f"Could not read {md_file}: {e}")

    if too_small:
        for item in too_small:
            errors.append(
                f"{item['file']} ({item['type']}) too small: "
                f"{item['actual']}w < {item['min']}w (missing {item['diff']}w)"
            )

    if too_large:
        for item in too_large:
            warnings.append(
                f"{item['file']} ({item['type']}) too large: "
                f"{item['actual']}w > {item['max']}w (exceeds by {item['diff']}w)"
            )

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_checked": len([f for f in md_files if detect_file_type(f)]),
            "too_small": len(too_small),
            "too_large": len(too_large),
        }
    }

def main():
    print("="*80)
    print("[VALIDATION] File Size")
    print("="*80)
    print()

    result = validate_file_size()

    errors = result["errors"]
    warnings = result["warnings"]
    stats = result["stats"]

    print(f"Total files checked: {stats['total_checked']}")
    print(f"Too small: {stats['too_small']}")
    print(f"Too large: {stats['too_large']}")
    print()

    if errors:
        print(f"[ERRORS] {len(errors)} files below minimum:")
        for error in errors[:15]:
            print(f"  [X] {error}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} files above maximum:")
        for warning in warnings[:10]:
            print(f"  [WARN] {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more")
        print()

    if not errors and not warnings:
        print("[[OK]] All files are within size limits")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
