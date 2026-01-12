#!/usr/bin/env python3
"""
Compara features documentadas com código implementado
NOTA: Validação heurística baseada em padrões comuns
"""
import sys
from pathlib import Path

def detect_features_in_code(src_path):
    """Detecta features implementadas no código (heurística)"""
    src_dir = Path(src_path)
    if not src_dir.exists():
        return set()

    features = set()

    # React/React Native: procura por *Page.tsx, *Screen.tsx
    for pattern in ["*Page.tsx", "*Screen.tsx", "*Page.jsx", "*Screen.jsx"]:
        for file in src_dir.rglob(pattern):
            # Ex: UnitsListPage.tsx → unit-management
            name = file.stem.replace("Page", "").replace("Screen", "")
            # Converte PascalCase para kebab-case
            kebab = "".join(["-" + c.lower() if c.isupper() else c for c in name]).lstrip("-")
            features.add(kebab)

    # .NET: procura por *Controller.cs
    for file in src_dir.rglob("*Controller.cs"):
        name = file.stem.replace("Controller", "")
        kebab = "".join(["-" + c.lower() if c.isupper() else c for c in name]).lstrip("-")
        features.add(kebab)

    return features

def validate_features_vs_code():
    errors = []
    warnings = []

    projects = ["GEOWEB", "REURBCAD", "GEOAPI", "ADMIN", "GEOGIS"]

    for project in projects:
        docs_dir = Path(f"PROJECTS/{project}/DOCS/FEATURES")
        src_dir = Path(f"PROJECTS/{project}/SRC-CODE")

        if not docs_dir.exists():
            continue

        if not src_dir.exists():
            warnings.append(f"{project}/SRC-CODE/ not found, skipping code validation")
            continue

        # Features documentadas
        doc_features = set()
        for feature_file in docs_dir.glob("*.md"):
            if feature_file.name != "README.md":
                doc_features.add(feature_file.stem)

        # Features no código (heurística)
        code_features = detect_features_in_code(src_dir)

        # Órfãos
        orphan_docs = doc_features - code_features
        orphan_code = code_features - doc_features

        # for orphan in orphan_docs:
        #     warnings.append(
        #         f"{project}: {orphan}.md documented but no matching code found (heuristic)"
        #     )

        for orphan in orphan_code:
            warnings.append(
                f"{project}: {orphan} code found but not documented in FEATURES/ (heuristic)"
            )

    return {"errors": errors, "warnings": warnings}

def main():
    print("="*80)
    print("[VALIDATION] Features vs Code (Heuristic)")
    print("="*80)
    print()
    print("[NOTE] This is a heuristic validation based on common patterns.")
    print("[NOTE] False positives/negatives are expected.")
    print()

    result = validate_features_vs_code()

    errors = result["errors"]
    warnings = result["warnings"]

    if errors:
        print(f"[ERRORS] {len(errors)} mismatches:")
        for error in errors:
            print(f"  [X] {error}")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} potential mismatches:")
        for warning in warnings[:15]:
            print(f"  [WARN] {warning}")
        if len(warnings) > 15:
            print(f"  ... and {len(warnings) - 15} more")
        print()

    if not errors and not warnings:
        print("[[OK]] Features and code appear aligned (heuristic)")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
