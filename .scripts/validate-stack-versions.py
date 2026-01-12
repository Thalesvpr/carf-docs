#!/usr/bin/env python3
"""
Valida consistência de versões de tecnologias entre documentos
"""
import sys
import re
from pathlib import Path

# Versões esperadas por projeto
EXPECTED_VERSIONS = {
    "GEOWEB": {
        "React": "18",
        "Vite": "5",
        "TanStack Query": ["v5", "5"],
        "TypeScript": "5",
    },
    "GEOAPI": {
        ".NET": "9",
        "EF Core": "9",
        "PostgreSQL": "16",
        "PostGIS": "3",
    },
    "REURBCAD": {
        "React Native": "0.74",
        "Expo": ["51", "SDK 51"],
        "WatermelonDB": "0.27",
    },
    "KEYCLOAK": {
        "Keycloak": "23",
        "Java": "17",
        "Quarkus": "3",
    },
    "GEOGIS": {
        "Python": "3.11",
        "QGIS": "3.34",
    },
    "ADMIN": {
        "React": "18",
        "Vite": "5",
    },
    "WEBDOCS": {
        "VitePress": "1",
        "Vue": "3",
    },
}

def find_version_mentions(docs, tech_name):
    """Encontra todas menções de uma tecnologia e suas versões"""
    mentions = []

    # Pattern: "React 18" ou "React Native 0.74"
    pattern = re.compile(rf"\b{re.escape(tech_name)}\s+(?:SDK\s+)?(?:v)?(\d+(?:\.\d+)?)")

    for doc in docs:
        try:
            content = doc.read_text(encoding="utf-8")
            matches = pattern.findall(content)
            if matches:
                mentions.append({
                    "file": str(doc).replace("\\", "/"),
                    "versions": matches,
                })
        except:
            pass

    return mentions

def validate_stack_versions():
    errors = []
    warnings = []

    for project, expected_techs in EXPECTED_VERSIONS.items():
        project_docs = list(Path(f"PROJECTS/{project}/DOCS").glob("**/*.md"))

        if not project_docs:
            warnings.append(f"{project}/DOCS/ not found")
            continue

        for tech, expected_version in expected_techs.items():
            mentions = find_version_mentions(project_docs, tech)

            if not mentions:
                # Tecnologia não mencionada - pode ser ok
                continue

            # Normaliza expected_version para lista
            if not isinstance(expected_version, list):
                expected_version = [expected_version]

            # Verifica inconsistências
            for mention in mentions:
                for found_version in mention["versions"]:
                    if found_version not in [str(v) for v in expected_version]:
                        errors.append(
                            f"{project}: {tech} version mismatch in {mention['file']}"
                            f" - found '{found_version}', expected {expected_version[0]}"
                        )

    return {"errors": errors, "warnings": warnings}

def main():
    print("="*80)
    print("[VALIDATION] Stack Versions")
    print("="*80)
    print()

    result = validate_stack_versions()

    errors = result["errors"]
    warnings = result["warnings"]

    if errors:
        print(f"[ERRORS] {len(errors)} version inconsistencies:")
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
        print("[[OK]] All stack versions are consistent")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
