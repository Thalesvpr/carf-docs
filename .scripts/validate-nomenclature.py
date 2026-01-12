#!/usr/bin/env python3
"""
Valida nomenclatura técnica consistente em toda documentação
"""
import sys
import re
from pathlib import Path

# Regras de nomenclatura
NOMENCLATURE_RULES = {
    r"REURB[^-SE\s]": {
        "message": "REURB deve ser qualificado como REURB-S ou REURB-E",
        "correct": "REURB-S (social) ou REURB-E (econômico)",
    },
    r"\bPostgres\b": {
        "message": "Use 'PostgreSQL' ao invés de 'Postgres'",
        "correct": "PostgreSQL",
    },
    r"\bKeyCloak\b": {
        "message": "Use 'Keycloak' ao invés de 'KeyCloak'",
        "correct": "Keycloak",
    },
    r"\breact-native\b": {
        "message": "Use 'React Native' ao invés de 'react-native' em prosa",
        "correct": "React Native",
    },
}

def validate_nomenclature():
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

    print(f"[*] Validating nomenclature in {len(md_files)} files...")
    print()

    violations_by_rule = {pattern: [] for pattern in NOMENCLATURE_RULES}

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")

            for pattern, rule in NOMENCLATURE_RULES.items():
                matches = list(re.finditer(pattern, content))

                if matches:
                    for match in matches:
                        # Encontra linha
                        line_num = content[:match.start()].count('\n') + 1
                        # Contexto (50 chars)
                        start = max(0, match.start() - 25)
                        end = min(len(content), match.end() + 25)
                        context = content[start:end].replace('\n', ' ')

                        violation = {
                            "file": str(md_file).replace("\\", "/"),
                            "line": line_num,
                            "match": match.group(),
                            "context": context,
                            "message": rule["message"],
                            "correct": rule["correct"],
                        }

                        violations_by_rule[pattern].append(violation)

        except Exception as e:
            warnings.append(f"Could not read {md_file}: {e}")

    # Reporta violações
    total_violations = sum(len(v) for v in violations_by_rule.values())

    if total_violations > 0:
        for pattern, violations in violations_by_rule.items():
            if violations:
                rule = NOMENCLATURE_RULES[pattern]
                errors.append(f"{len(violations)} violations of: {rule['message']}")

    return {
        "errors": errors,
        "warnings": warnings,
        "violations": violations_by_rule,
        "total_violations": total_violations,
    }

def main():
    print("="*80)
    print("[VALIDATION] Nomenclature")
    print("="*80)
    print()

    result = validate_nomenclature()

    errors = result["errors"]
    warnings = result["warnings"]
    violations_by_rule = result["violations"]
    total = result["total_violations"]

    if errors:
        print(f"[ERRORS] {total} nomenclature violations:")
        for error in errors:
            print(f"  [X] {error}")
        print()

        # Mostra primeiros 5 exemplos de cada tipo
        for pattern, violations in violations_by_rule.items():
            if violations:
                rule = NOMENCLATURE_RULES[pattern]
                print(f"  Rule: {rule['message']}")
                print(f"  Correct: {rule['correct']}")
                for v in violations[:3]:
                    print(f"    • {v['file']}:{v['line']}")
                    print(f"      Found: '{v['match']}'")
                if len(violations) > 3:
                    print(f"    ... and {len(violations) - 3} more")
                print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} issues:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    if not errors and not warnings:
        print("[[OK]] All nomenclature is consistent")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
