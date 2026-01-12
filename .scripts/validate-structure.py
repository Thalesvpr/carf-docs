#!/usr/bin/env python3
"""
Valida estrutura de diretórios padronizada PROJECTS/*/DOCS/
"""
import sys
from pathlib import Path

REQUIRED_DIRS = ["ARCHITECTURE", "CONCEPTS", "HOW-TO"]
REQUIRED_FILES = ["README.md"]

# Exceções conhecidas
EXCEPTIONS = {
    "WEBDOCS": {"missing_dirs": ["FEATURES"]},  # Site documentação
    "LIB": {"has_subdirs": True},  # LIB/TS/* tem subdirs
}

def validate_project_structure():
    errors = []
    warnings = []

    projects_dir = Path("PROJECTS")
    if not projects_dir.exists():
        return {"errors": ["PROJECTS/ directory not found"], "warnings": []}

    # Projetos principais
    projects = ["ADMIN", "GEOAPI", "GEOGIS", "GEOWEB", "KEYCLOAK", "REURBCAD", "WEBDOCS"]

    for project in projects:
        project_docs = projects_dir / project / "DOCS"

        if not project_docs.exists():
            errors.append(f"{project}/DOCS/ not found")
            continue

        # Verifica diretórios obrigatórios
        for required_dir in REQUIRED_DIRS:
            dir_path = project_docs / required_dir
            if not dir_path.exists():
                errors.append(f"{project}/DOCS/{required_dir}/ missing")
            else:
                # Verifica README dentro do subdiretório
                readme = dir_path / "README.md"
                if not readme.exists():
                    errors.append(f"{project}/DOCS/{required_dir}/README.md missing")

        # Verifica README principal
        main_readme = project_docs / "README.md"
        if not main_readme.exists():
            errors.append(f"{project}/DOCS/README.md missing")

        # Verifica diretórios vazios
        for subdir in project_docs.iterdir():
            if subdir.is_dir() and subdir.name not in [".git", "node_modules"]:
                if not any(subdir.iterdir()):
                    warnings.append(f"{project}/DOCS/{subdir.name}/ is empty")

    # Valida LIB (estrutura especial)
    lib_dir = projects_dir / "LIB" / "TS"
    if lib_dir.exists():
        for lib in lib_dir.iterdir():
            if lib.is_dir():
                lib_docs = lib / "DOCS"
                if not lib_docs.exists():
                    errors.append(f"LIB/TS/{lib.name}/DOCS/ not found")

    return {"errors": errors, "warnings": warnings}

def main():
    print("="*80)
    print("[VALIDATION] Project Structure")
    print("="*80)
    print()

    result = validate_project_structure()

    errors = result["errors"]
    warnings = result["warnings"]

    if errors:
        print(f"[ERRORS] {len(errors)} structure violations:")
        for error in errors:
            print(f"  [X] {error}")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} potential issues:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    if not errors and not warnings:
        print("[[OK]] All project structures are valid")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
