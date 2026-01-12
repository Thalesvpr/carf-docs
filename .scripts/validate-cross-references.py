#!/usr/bin/env python3
"""
Valida referências bidirecionais CENTRAL ↔ PROJECTS
- PROJECTS → CENTRAL deve ter links
- CENTRAL → PROJECTS NÃO deve ter links (isolamento)
"""
import sys
import re
from pathlib import Path

def count_links_to(file_path, target_prefix):
    """Conta links para target_prefix em file_path"""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Pattern: [texto](../CENTRAL/... ou ./CENTRAL/... ou CENTRAL/...)
        pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        matches = pattern.findall(content)

        count = 0
        for text, link in matches:
            if target_prefix in link:
                count += 1

        return count
    except:
        return 0

def validate_cross_references():
    errors = []
    warnings = []

    # Valida PROJECTS → CENTRAL (deve ter links)
    print("[*] Validating PROJECTS → CENTRAL references...")
    features = list(Path("PROJECTS").glob("*/DOCS/FEATURES/*.md"))
    features = [f for f in features if f.name != "README.md"]

    no_central_refs = []
    for feature in features:
        central_refs = count_links_to(feature, "CENTRAL/")
        if central_refs == 0:
            no_central_refs.append(str(feature).replace("\\", "/"))

    if no_central_refs:
        for f in no_central_refs:
            warnings.append(f"{f} has no links to CENTRAL/")

    # Valida CENTRAL → PROJECTS (NÃO deve ter links)
    print("[*] Validating CENTRAL → PROJECTS isolation...")
    central_docs = list(Path("CENTRAL").glob("**/*.md"))

    has_project_refs = []
    for doc in central_docs:
        project_refs = count_links_to(doc, "PROJECTS/")
        if project_refs > 0:
            has_project_refs.append((str(doc).replace("\\", "/"), project_refs))

    if has_project_refs:
        for doc, count in has_project_refs:
            errors.append(f"{doc} has {count} forbidden link(s) to PROJECTS/")

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "features_without_central_refs": len(no_central_refs),
            "central_with_project_refs": len(has_project_refs),
        }
    }

def main():
    print("="*80)
    print("[VALIDATION] Cross References")
    print("="*80)
    print()

    result = validate_cross_references()

    errors = result["errors"]
    warnings = result["warnings"]
    stats = result["stats"]

    print(f"Features without CENTRAL refs: {stats['features_without_central_refs']}")
    print(f"CENTRAL docs with PROJECTS refs: {stats['central_with_project_refs']}")
    print()

    if errors:
        print(f"[ERRORS] {len(errors)} isolation violations:")
        for error in errors[:10]:
            print(f"  [X] {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} features without CENTRAL refs:")
        for warning in warnings[:10]:
            print(f"  [WARN] {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more")
        print()

    if not errors and not warnings:
        print("[[OK]] Cross references are valid")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
