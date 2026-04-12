"""
CLI entry point para CARF Validator.

Usage:
    python -m carf_validator [OPTIONS]

Examples:
    python -m carf_validator
    python -m carf_validator --format markdown --output report.md
    python -m carf_validator --only broken_links rf_coverage
    python -m carf_validator --disable orphans
    python -m carf_validator --list-validators
"""

import argparse
import sys
from pathlib import Path

from . import ValidationPipeline, get_reporter
from .validators.registry import ValidatorRegistry
from . import validators  # Garante registro de todos os validadores


def main():
    parser = argparse.ArgumentParser(
        prog="carf_validator",
        description="Sistema de validação estrutural e semântica CARF",
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Diretório raiz do repositório (default: diretório atual)",
    )

    parser.add_argument(
        "--format", "-f",
        choices=["console", "markdown", "json"],
        default="console",
        help="Formato de saída (default: console)",
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Arquivo de saída (default: stdout)",
    )

    parser.add_argument(
        "--only",
        nargs="+",
        help="Executar apenas estes validadores",
    )

    parser.add_argument(
        "--disable",
        nargs="+",
        help="Desabilitar estes validadores",
    )

    parser.add_argument(
        "--list-validators",
        action="store_true",
        help="Lista validadores disponíveis",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Desabilita cores no output (console)",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit code 1 se houver warnings (além de errors)",
    )

    args = parser.parse_args()

    # Lista validadores
    if args.list_validators:
        _list_validators()
        return 0

    # Executa validação
    try:
        pipeline = ValidationPipeline(
            root_path=args.root,
            enabled_validators=set(args.only) if args.only else None,
            disabled_validators=set(args.disable) if args.disable else None,
        )

        report = pipeline.run()

        # Gera relatório
        reporter = get_reporter(args.format)
        if args.format == "console" and args.no_color:
            reporter.use_colors = False

        output = reporter.report(report, args.output)

        # Imprime se for console
        if args.format == "console" or not args.output:
            print(output)

        # Exit code
        if report.totals.get("errors", 0) > 0:
            return 1
        if args.strict and report.totals.get("warnings", 0) > 0:
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


def _list_validators():
    """Lista todos os validadores disponíveis."""
    # Importa para garantir registro
    from . import validators

    registry = ValidatorRegistry.instance()
    all_validators = registry.get_all()

    print("Available validators:")
    print()

    local = [v for v in all_validators if hasattr(v, 'validate_document')]
    global_ = [v for v in all_validators if hasattr(v, 'validate') and not hasattr(v, 'validate_document')]

    print("Local validators (per-file):")
    for v in sorted(local, key=lambda x: x.name):
        print(f"  - {v.name}: {v.description}")

    print()
    print("Global validators (graph-based):")
    for v in sorted(global_, key=lambda x: x.name):
        print(f"  - {v.name}: {v.description}")


if __name__ == "__main__":
    sys.exit(main())
