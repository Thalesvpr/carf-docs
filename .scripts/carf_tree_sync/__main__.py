"""CLI entry point for carf_tree_sync."""

import argparse
import sys
from pathlib import Path

from . import TreeSyncPipeline, __version__


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="carf_tree_sync",
        description="Sincroniza indices de READMEs no repositorio CARF",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Diretorio raiz do repositorio (default: diretorio atual)",
    )

    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Subpath especifico para sincronizar (ex: CENTRAL/REQUIREMENTS)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra mudancas sem aplicar",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostra progresso detalhado",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Desabilita cores no output",
    )

    return parser


def print_report(report, use_color: bool = True) -> None:
    """Print sync report to console."""
    # Colors
    if use_color:
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        CYAN = "\033[96m"
        RESET = "\033[0m"
        BOLD = "\033[1m"
    else:
        GREEN = YELLOW = RED = CYAN = RESET = BOLD = ""

    print()
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}CARF Tree Sync Report{RESET}")
    if report.dry_run:
        print(f"{YELLOW}[DRY-RUN] Nenhuma alteracao foi aplicada{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print()

    print(f"{CYAN}Resumo{RESET}")
    print(f"  Nos processados: {report.total_nodes}")
    print(f"  {GREEN}Atualizados: {report.updated_nodes}{RESET}")
    print(f"  Sem alteracao: {report.unchanged_nodes}")
    if report.error_nodes > 0:
        print(f"  {RED}Erros: {report.error_nodes}{RESET}")
    print()

    # Show updated files
    if report.updated_nodes > 0:
        print(f"{CYAN}Arquivos atualizados:{RESET}")
        for result in report.results:
            if result.updated:
                rel_path = result.path
                try:
                    rel_path = result.path.relative_to(Path.cwd())
                except ValueError:
                    pass
                status = f"{GREEN}[OK]{RESET}" if not report.dry_run else f"{YELLOW}[DRY]{RESET}"
                print(f"  {status} {rel_path}")
                print(f"       {result.message}")
        print()

    # Show errors
    if report.error_nodes > 0:
        print(f"{RED}Erros:{RESET}")
        for result in report.results:
            if "Erro" in result.message:
                rel_path = result.path
                try:
                    rel_path = result.path.relative_to(Path.cwd())
                except ValueError:
                    pass
                print(f"  {RED}[ERRO]{RESET} {rel_path}")
                print(f"       {result.message}")
        print()

    # Final status
    if report.error_nodes > 0:
        print(f"{RED}[FAIL] Sincronizacao com erros{RESET}")
    elif report.updated_nodes > 0:
        if report.dry_run:
            print(f"{YELLOW}[DRY-RUN] {report.updated_nodes} arquivos seriam atualizados{RESET}")
        else:
            print(f"{GREEN}[OK] {report.updated_nodes} arquivos atualizados{RESET}")
    else:
        print(f"{GREEN}[OK] Todos os indices estao atualizados{RESET}")


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Resolve root path
    root_dir = args.root.resolve()

    # If subpath specified, adjust root
    if args.path:
        root_dir = root_dir / args.path
        if not root_dir.exists():
            print(f"Erro: Path nao existe: {root_dir}", file=sys.stderr)
            return 2

    if args.verbose:
        print(f"Sincronizando: {root_dir}")
        if args.dry_run:
            print("Modo: dry-run (sem alteracoes)")
        print()

    # Run pipeline
    try:
        pipeline = TreeSyncPipeline(
            root_dir=root_dir,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )
        report = pipeline.run()
    except Exception as e:
        print(f"Erro de execucao: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 2

    # Print report
    print_report(report, use_color=not args.no_color)

    # Return code
    if report.error_nodes > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
