#!/usr/bin/env python3
"""
Valida idioma português em documentação (exceto termos técnicos e ADRs)
"""
import sys
import re
from pathlib import Path

# Palavras comuns em inglês que não deveriam aparecer em prosa
ENGLISH_WORDS = [
    "the", "and", "for", "with", "this", "that", "from", "have", "has",
    "will", "can", "should", "would", "could", "but", "not", "are", "were",
    "been", "being", "does", "did", "done", "such", "than", "then", "these",
    "those", "their", "there", "which", "what", "when", "where", "who", "why",
]

# Termos técnicos permitidos (sempre em inglês)
TECHNICAL_TERMS = [
    "API", "REST", "HTTP", "HTTPS", "JSON", "XML", "SQL", "NoSQL",
    "Docker", "Kubernetes", "Git", "CI/CD", "JWT", "OAuth", "OIDC",
    "React", "TypeScript", "JavaScript", "Node.js", "npm", "yarn",
    "PostgreSQL", "PostGIS", "Redis", "MongoDB",
    ".NET", "C#", "Entity Framework", "EF Core",
    "React Native", "Expo", "Android", "iOS",
    "Keycloak", "LDAP", "SAML",
    "QGIS", "GeoJSON", "WKT", "Shapefile",
    "Controller", "Service", "Repository", "Entity", "DTO",
    "frontend", "backend", "fullstack", "middleware",
    "endpoint", "payload", "schema", "migration",
]

def extract_prose_only(content):
    """Remove code blocks, links, e termos técnicos"""
    # Remove code blocks
    content = re.sub(r"```[\s\S]*?```", "", content)
    content = re.sub(r"`[^`]+`", "", content)

    # Remove links markdown [texto](url)
    content = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", content)

    # Remove URLs
    content = re.sub(r"https?://\S+", "", content)

    # Remove termos técnicos conhecidos
    for term in TECHNICAL_TERMS:
        content = re.sub(rf"\b{re.escape(term)}\b", "", content, flags=re.IGNORECASE)

    return content

def validate_language():
    errors = []
    warnings = []

    # Busca todos .md em CENTRAL e PROJECTS/*/DOCS (exceto ADRs)
    md_files = list(Path("CENTRAL").glob("**/*.md"))
    md_files += list(Path("PROJECTS").glob("*/DOCS/**/*.md"))

    # Exclui ADRs (podem ter inglês), node_modules, SRC-CODE
    md_files = [
        f for f in md_files
        if "ADRs" not in str(f)
        and "node_modules" not in str(f)
        and "SRC-CODE" not in str(f)
    ]

    print(f"[*] Validating language in {len(md_files)} files...")
    print()

    violations = []

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            prose = extract_prose_only(content)

            # Procura palavras inglesas comuns
            for word in ENGLISH_WORDS:
                pattern = rf"\b{word}\b"
                matches = list(re.finditer(pattern, prose, re.IGNORECASE))

                if matches:
                    for match in matches[:3]:  # Limita a 3 por palavra por arquivo
                        # Contexto (30 chars cada lado)
                        start = max(0, match.start() - 30)
                        end = min(len(prose), match.end() + 30)
                        context = prose[start:end].replace('\n', ' ').strip()

                        violations.append({
                            "file": str(md_file).replace("\\", "/"),
                            "word": match.group(),
                            "context": context,
                        })

        except Exception as e:
            warnings.append(f"Could not read {md_file}: {e}")

    if violations:
        # Agrupa por arquivo
        by_file = {}
        for v in violations:
            file = v["file"]
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(v)

        for file, file_violations in by_file.items():
            words = ", ".join(set(v["word"] for v in file_violations))
            errors.append(f"{file} contains English words: {words}")

    return {
        "errors": errors,
        "warnings": warnings,
        "violations": violations,
        "total_violations": len(violations),
    }

def main():
    print("="*80)
    print("[VALIDATION] Language (Portuguese)")
    print("="*80)
    print()
    print("[NOTE] Ignoring ADRs, code blocks, technical terms")
    print()

    result = validate_language()

    errors = result["errors"]
    warnings = result["warnings"]
    violations = result["violations"]
    total = result["total_violations"]

    if errors:
        print(f"[ERRORS] {total} English word occurrences in {len(errors)} files:")
        for error in errors[:10]:
            print(f"  [X] {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more files")
        print()

        # Mostra 3 exemplos com contexto
        print("Examples:")
        for v in violations[:3]:
            print(f"  • {v['file']}")
            print(f"    Word: '{v['word']}'")
            print(f"    Context: ...{v['context']}...")
        if len(violations) > 3:
            print(f"  ... and {len(violations) - 3} more")
        print()

    if warnings:
        print(f"[WARNINGS] {len(warnings)} issues:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
        print()

    if not errors and not warnings:
        print("[[OK]] All documentation is in Portuguese")

    print("="*80)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("="*80)

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
