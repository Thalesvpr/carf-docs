#!/usr/bin/env python3
"""
Auditoria Brutal Completa da Documentação CARF
Executa TODAS validações sem exceção e gera relatório consolidado
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Todas validações (existentes + novas)
VALIDATIONS = [
    # Validações existentes (5)
    ("Dense Paragraph", "python .scripts/lint-dense-paragraph.py"),
    ("Isolated Files", "python .scripts/list-isolated-simple.py"),
    ("Broken Links", "python .scripts/check-links.py"),
    ("Central Isolation", "python .scripts/lint-central-isolation.py"),
    ("UC Coverage", "python .scripts/validate-uc-coverage.py"),

    # Validações novas - Fase 2 (11)
    ("Structure", "python .scripts/validate-structure.py"),
    ("RF Coverage", "python .scripts/validate-rf-coverage.py"),
    ("Nomenclature", "python .scripts/validate-nomenclature.py"),
    ("Stack Versions", "python .scripts/validate-stack-versions.py"),
    ("Cross References", "python .scripts/validate-cross-references.py"),
    ("Features vs Code", "python .scripts/validate-features-vs-code.py"),
    ("Feature Sections", "python .scripts/validate-feature-sections.py"),
    ("Language", "python .scripts/validate-language.py"),
    ("Metadata", "python .scripts/validate-metadata.py"),
    ("File Size", "python .scripts/validate-file-size.py"),
    ("File Structure", "python .scripts/validate-file-structure.py"),
]

def count_errors_warnings(stdout):
    """Extrai número de errors e warnings do output"""
    errors = 0
    warnings = 0

    for line in stdout.split("\n"):
        if line.startswith("Errors:"):
            try:
                errors = int(line.split(":")[1].strip())
            except:
                pass
        elif line.startswith("Warnings:"):
            try:
                warnings = int(line.split(":")[1].strip())
            except:
                pass

    return errors, warnings

def run_audit():
    """Executa todas validações e coleta resultados"""
    print("="*80)
    print("AUDITORIA BRUTAL COMPLETA - CARF DOCUMENTATION")
    print("="*80)
    print()
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Validações: {len(VALIDATIONS)}")
    print()

    results = {}
    total_errors = 0
    total_warnings = 0

    for i, (name, command) in enumerate(VALIDATIONS, 1):
        print(f"[{i}/{len(VALIDATIONS)}] Running {name}...")

        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout por validação
            )

            errors, warnings = count_errors_warnings(result.stdout)
            total_errors += errors
            total_warnings += warnings

            results[name] = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "errors": errors,
                "warnings": warnings,
            }

            if result.returncode == 0:
                if errors == 0 and warnings == 0:
                    print(f"  [OK] PASSED")
                else:
                    print(f"  [OK] PASSED (0 errors, {warnings} warnings)")
            else:
                print(f"  [FAIL] FAILED ({errors} errors, {warnings} warnings)")

        except subprocess.TimeoutExpired:
            print(f"  [FAIL] TIMEOUT (exceeded 5 minutes)")
            results[name] = {
                "returncode": -1,
                "stdout": "",
                "stderr": "Timeout after 5 minutes",
                "errors": 1,
                "warnings": 0,
            }
            total_errors += 1
        except Exception as e:
            print(f"  [FAIL] ERROR ({e})")
            results[name] = {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "errors": 1,
                "warnings": 0,
            }
            total_errors += 1

        print()

    return results, total_errors, total_warnings

def generate_summary_report(results, total_errors, total_warnings):
    """Gera relatório consolidado"""
    report_dir = Path("validation-reports")
    report_dir.mkdir(exist_ok=True)

    report_path = report_dir / "BRUTAL-AUDIT.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Auditoria Brutal Completa - CARF Documentation\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Git info
        try:
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True
            ).stdout.strip()[:8]
            branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True
            ).stdout.strip()
            f.write(f"**Versão:** {branch}@{commit}\n")
        except:
            pass

        f.write(f"**Total Validações:** {len(VALIDATIONS)}\n\n")

        # Resumo Executivo
        f.write("## Resumo Executivo\n\n")
        f.write("| Validação | Status | Erros | Warnings |\n")
        f.write("|-----------|--------|-------|----------|\n")

        passed = 0
        failed = 0

        for name, result in results.items():
            status = "[OK] PASS" if result["returncode"] == 0 else "[FAIL] FAIL"
            if result["returncode"] == 0:
                passed += 1
            else:
                failed += 1

            f.write(f"| {name} | {status} | {result['errors']} | {result['warnings']} |\n")

        f.write("\n")
        f.write(f"**Resultado Final:** {'[FAIL] FAILED' if failed > 0 else '[OK] PASSED'} ")
        f.write(f"({passed} passed, {failed} failed)\n\n")
        f.write(f"**Total Erros:** {total_errors}\n")
        f.write(f"**Total Warnings:** {total_warnings}\n\n")

        # Seção detalhada por validação
        f.write("## Detalhes por Validação\n\n")

        for name, result in results.items():
            f.write(f"### {name}\n\n")

            if result["returncode"] == 0:
                f.write("**Status:** [OK] PASSED\n\n")
            else:
                f.write("**Status:** [FAIL] FAILED\n\n")

            if result["errors"] > 0 or result["warnings"] > 0:
                f.write(f"- Erros: {result['errors']}\n")
                f.write(f"- Warnings: {result['warnings']}\n\n")

            # Output parcial (primeiras 30 linhas)
            if result["stdout"]:
                lines = result["stdout"].split("\n")
                if len(lines) > 40:
                    f.write("<details>\n<summary>Ver detalhes (output truncado)</summary>\n\n")
                    f.write("```\n")
                    f.write("\n".join(lines[:40]))
                    f.write(f"\n... ({len(lines) - 40} linhas omitidas)")
                    f.write("\n```\n</details>\n\n")
                else:
                    f.write("<details>\n<summary>Ver detalhes</summary>\n\n")
                    f.write("```\n")
                    f.write(result["stdout"])
                    f.write("\n```\n</details>\n\n")

        # Recomendações
        f.write("## Recomendações\n\n")
        f.write("### Imediato (Esta Semana)\n")
        f.write("1. Revisar e corrigir erros críticos (validações FAILED)\n")
        f.write("2. Analisar warnings de alta prioridade\n")
        f.write("3. Documentar decisões sobre exceções aceitáveis\n\n")

        f.write("### Curto Prazo (Este Mês)\n")
        f.write("1. Resolver warnings restantes\n")
        f.write("2. Completar diretórios incompletos identificados\n")
        f.write("3. Atualizar metadados desatualizados\n\n")

        f.write("### Médio Prazo (Quarter)\n")
        f.write("1. Estabelecer validação automática em CI/CD\n")
        f.write("2. Criar dashboard de qualidade documentação\n")
        f.write("3. Revisar e atualizar VALIDATION-RULES.md\n\n")

        f.write("---\n")
        f.write(f"**Próxima Auditoria:** {(datetime.now()).strftime('%Y-%m')}-** (monthly)\n")

    return report_path

def save_detailed_outputs(results):
    """Salva outputs detalhados de cada validação"""
    report_dir = Path("validation-reports")
    detail_dir = report_dir / "details"
    detail_dir.mkdir(exist_ok=True)

    for name, result in results.items():
        safe_name = name.lower().replace(" ", "-")
        output_file = detail_dir / f"{safe_name}.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Validação: {name}\n")
            f.write("="*80 + "\n\n")
            f.write("STDOUT:\n")
            f.write(result["stdout"])
            f.write("\n\nSTDERR:\n")
            f.write(result["stderr"])

def main():
    # Verifica se estamos no diretório correto
    if not Path("CENTRAL").exists() or not Path("PROJECTS").exists():
        print("ERROR: Deve executar do diretório raiz do projeto (C:\\DEV\\CARF)")
        return 1

    # Executa auditoria
    results, total_errors, total_warnings = run_audit()

    # Gera relatórios
    print("="*80)
    print("Gerando relatórios...")
    print()

    report_path = generate_summary_report(results, total_errors, total_warnings)
    save_detailed_outputs(results)

    print(f"[OK] Relatório consolidado: {report_path}")
    print(f"[OK] Outputs detalhados: validation-reports/details/")
    print()

    # Resumo final
    passed = sum(1 for r in results.values() if r["returncode"] == 0)
    failed = len(results) - passed

    print("="*80)
    print("RESULTADO FINAL")
    print("="*80)
    print(f"Validações: {passed} passed, {failed} failed")
    print(f"Erros: {total_errors}")
    print(f"Warnings: {total_warnings}")
    print("="*80)

    # Exit code: falha se qualquer validação falhou
    return 1 if failed > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
