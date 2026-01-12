#!/usr/bin/env python3
"""
Valida seções obrigatórias em PROJECTS/*/DOCS/FEATURES/*.md
"""
import sys
import re
from pathlib import Path

# Seções obrigatórias em features (padrões regex)
REQUIRED_SECTIONS = [
    (r"##\s+Validações", "## Validações"),
    (r"##\s+(API Integration|Integração API)", "## API Integration ou ## Integração API"),
    (r"##\s+(Relacionamentos|Domain Model)", "## Relacionamentos ou ## Domain Model"),
]

def validate_feature_sections():
    errors = []
    warnings = []

    # Busca todos features (exceto README.md)
    features = list(Path("PROJECTS").glob("*/DOCS/FEATURES/*.md"))
    features = [f for f in features if f.name != "README.md"]

    if not features:
        warnings.append("No feature files found in PROJECTS/*/DOCS/FEATURES/")
        return {"errors": errors, "warnings": warnings}

    print(f"[*] Validating {len(features)} feature files...")
    print()

    missing_sections = []

    for feature_file in features:
        try:
            content = feature_file.read_text(encoding="utf-8")
            rel_path = str(feature_file).replace("\\", "/")

            for pattern, section_name in REQUIRED_SECTIONS:
                if not re.search(pattern, content, re.IGNORECASE):
                    missing_sections.append({
                        "file": rel_path,
                        "section": section_name,
                    })

        except Exception as e:
            warnings.append(f"Could not read {feature_file}: {e}")

    if missing_sections:
        for missing in missing_sections:
            errors.append(
                f"{missing['file']} missing required section: {missing['section']}"
            )

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_features": len(features),
            "features_with_missing_sections": len(set(m["file"] for m in missing_sections)),
            "total_missing_sections": len(missing_sections),
        }
    }

def main():
    print("="*80)
    print("[VALIDATION] Feature Sections")
    print("="*80)
    print()

    result = validate_feature_sections()

    errors = result["errors"]
    warnings = result["warnings"]
    stats = result.get("stats", {})

    if stats:
        print(f"Total features: {stats['total_features']}")
        print(f"Features with missing sections: {stats['features_with_missing_sections']}")
        print(f"Total missing sections: {stats['total_missing_sections']}")
        print()

    if errors:
        print(f"[ERRORS] {len(errors)} missing sections:")
        for error in errors[:15]:
            print(f"  [X] {error}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} issues:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    if not errors and not warnings:
        print("[[OK]] All features have required sections")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
