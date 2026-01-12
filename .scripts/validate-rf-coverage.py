#!/usr/bin/env python3
"""
Valida coverage de Requisitos Funcionais (RF-XXX) em FEATURES
"""
import sys
import re
from pathlib import Path

def find_all_rfs():
    """Encontra todos RF-XXX em CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/"""
    rf_dir = Path("CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS")
    if not rf_dir.exists():
        return []

    rfs = []
    for rf_file in rf_dir.glob("RF-*.md"):
        # Extrai número RF do filename
        match = re.match(r"RF-(\d{3})", rf_file.stem)
        if match:
            rfs.append(f"RF-{match.group(1)}")

    return sorted(rfs)

def find_rf_mentions_in_features(rf_num):
    """Encontra menções de RF-XXX em PROJECTS/*/DOCS/FEATURES/*.md"""
    features_paths = list(Path("PROJECTS").glob("*/DOCS/FEATURES/*.md"))

    mentions = []
    pattern = re.compile(rf"\b{re.escape(rf_num)}\b")

    for feature_file in features_paths:
        if feature_file.name == "README.md":
            continue

        try:
            content = feature_file.read_text(encoding="utf-8")
            if pattern.search(content):
                # Formato: PROJECTS/GEOWEB/DOCS/FEATURES/unit-management.md
                rel_path = str(feature_file).replace("\\", "/")
                mentions.append(rel_path)
        except Exception as e:
            print(f"[WARN] Could not read {feature_file}: {e}")

    return mentions

def validate_rf_coverage():
    errors = []
    warnings = []

    all_rfs = find_all_rfs()
    print(f"[*] Found {len(all_rfs)} Functional Requirements (RF-001 to RF-{all_rfs[-1].split('-')[1] if all_rfs else '000'})")
    print()

    orphan_rfs = []

    for rf in all_rfs:
        implementations = find_rf_mentions_in_features(rf)

        if not implementations:
            orphan_rfs.append(rf)
        # else:
        #     print(f"  [OK] {rf} covered in {len(implementations)} feature(s)")

    if orphan_rfs:
        errors.extend([f"{rf} not implemented in any FEATURES" for rf in orphan_rfs])

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_rfs": len(all_rfs),
            "covered": len(all_rfs) - len(orphan_rfs),
            "orphans": len(orphan_rfs),
        }
    }

def main():
    print("="*80)
    print("[VALIDATION] RF Coverage")
    print("="*80)
    print()

    result = validate_rf_coverage()

    errors = result["errors"]
    warnings = result["warnings"]
    stats = result["stats"]

    print(f"Total RFs: {stats['total_rfs']}")
    print(f"Covered: {stats['covered']}")
    print(f"Orphans: {stats['orphans']}")
    print()

    if errors:
        print(f"[ERRORS] {len(errors)} orphan RFs (not implemented):")
        for error in errors[:10]:  # Limita output
            print(f"  [X] {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} issues:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    if not errors and not warnings:
        print("[[OK]] All RFs are covered in FEATURES")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
