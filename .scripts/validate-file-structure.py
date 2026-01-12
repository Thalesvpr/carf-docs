#!/usr/bin/env python3
"""
Valida estrutura interna (seções obrigatórias, frontmatter, padrões)
"""
import sys
import re
from pathlib import Path

# Regras de estrutura por tipo (baseado em VALIDATION-RULES.md)
STRUCTURE_RULES = {
    "README": {
        "required_sections": [r"##?\s+Descrição", r"##?\s+Links"],
        "title_pattern": r"^#\s+[A-Z]",
    },
    "ADR": {
        "required_metadata": ["Data", "Status", "Decisor"],
        "title_pattern": r"^#\s+ADR-\d{3}:",
        "forbidden": {"internal_links": True},
    },
    "UC": {
        "required_frontmatter": ["modules", "epic"],
        "required_sections": [r"##\s+Regras de Negócio", r"##\s+Rastreabilidade"],
        "title_pattern": r"^#\s+UC-\d{3}:",
    },
    "RF": {
        "required_sections": [r"##\s+Critérios de Aceitação", r"##\s+Relacionado a"],
        "title_pattern": r"^#\s+RF-\d{3}:",
    },
    "US": {
        "required_phrases": ["As a", "I want", "So that"],
        "required_sections": [r"##\s+Acceptance Criteria"],
        "title_pattern": r"^#\s+US-\d{3}:",
    },
    "Entity": {
        "title_pattern": r"^#\s+\d{2}-[a-z-]+",
    },
    "Feature": {
        "required_sections": [
            r"##\s+Validações",
            r"##\s+(API Integration|Integração API)",
            r"##\s+(Relacionamentos|Domain Model)",
        ],
    },
    "HOW-TO": {
        "required_sections": [r"##\s+Pré-requisitos", r"##\s+Passos"],
        "title_pattern": r"^#\s+\d{2}-",
    },
}

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

    return None

def extract_frontmatter(content):
    """Extrai frontmatter YAML"""
    match = re.match(r"^---\n([\s\S]*?)\n---\n", content)
    if match:
        frontmatter = {}
        for line in match.group(1).split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()
        return frontmatter
    return {}

def validate_file_structure():
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

    print(f"[*] Validating file structure in {len(md_files)} files...")
    print()

    violations = []

    for md_file in md_files:
        file_type = detect_file_type(md_file)

        if not file_type:
            continue  # Tipo desconhecido, pula

        rules = STRUCTURE_RULES.get(file_type)
        if not rules:
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            rel_path = str(md_file).replace("\\", "/")
            lines = content.split("\n")
            first_line = lines[0] if lines else ""

            # Valida título
            if "title_pattern" in rules:
                if not re.match(rules["title_pattern"], first_line):
                    violations.append({
                        "file": rel_path,
                        "type": "title",
                        "message": f"Title doesn't match pattern: {rules['title_pattern']}",
                    })

            # Valida seções obrigatórias
            if "required_sections" in rules:
                for section_pattern in rules["required_sections"]:
                    if not re.search(section_pattern, content):
                        violations.append({
                            "file": rel_path,
                            "type": "section",
                            "message": f"Missing section: {section_pattern}",
                        })

            # Valida frontmatter
            if "required_frontmatter" in rules:
                frontmatter = extract_frontmatter(content)
                for field in rules["required_frontmatter"]:
                    if field not in frontmatter:
                        violations.append({
                            "file": rel_path,
                            "type": "frontmatter",
                            "message": f"Missing frontmatter field: {field}",
                        })

            # Valida frases obrigatórias
            if "required_phrases" in rules:
                for phrase in rules["required_phrases"]:
                    if phrase not in content:
                        violations.append({
                            "file": rel_path,
                            "type": "phrase",
                            "message": f"Missing required phrase: '{phrase}'",
                        })

            # Valida metadados
            if "required_metadata" in rules:
                for metadata in rules["required_metadata"]:
                    pattern = rf"\*\*{re.escape(metadata)}\*\*:"
                    if not re.search(pattern, content):
                        violations.append({
                            "file": rel_path,
                            "type": "metadata",
                            "message": f"Missing metadata: {metadata}",
                        })

            # Valida proibições
            if "forbidden" in rules:
                if rules["forbidden"].get("internal_links"):
                    # Conta links internos [texto](./arquivo.md ou ../arquivo.md)
                    internal_links = re.findall(r"\[([^\]]+)\]\(\.\.?/[^)]+\)", content)
                    if internal_links:
                        violations.append({
                            "file": rel_path,
                            "type": "forbidden",
                            "message": f"Contains {len(internal_links)} forbidden internal link(s)",
                        })

        except Exception as e:
            warnings.append(f"Could not read {md_file}: {e}")

    if violations:
        for v in violations:
            errors.append(f"{v['file']} ({v['type']}): {v['message']}")

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_checked": len([f for f in md_files if detect_file_type(f)]),
            "total_violations": len(violations),
        }
    }

def main():
    print("="*80)
    print("[VALIDATION] File Structure")
    print("="*80)
    print()

    result = validate_file_structure()

    errors = result["errors"]
    warnings = result["warnings"]
    stats = result["stats"]

    print(f"Total files checked: {stats['total_checked']}")
    print(f"Total violations: {stats['total_violations']}")
    print()

    if errors:
        print(f"[ERRORS] {len(errors)} structure violations:")
        for error in errors[:20]:
            print(f"  [X] {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} issues:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    if not errors and not warnings:
        print("[[OK]] All files have valid structure")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
