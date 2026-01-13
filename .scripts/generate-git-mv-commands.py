#!/usr/bin/env python3
"""
Gera comandos git mv para reorganizar arquivos de requisitos em pastas.

Uso:
    python .scripts/generate-git-mv-commands.py > move-commands.sh
    # Revise o arquivo e execute:
    bash move-commands.sh
"""
from pathlib import Path

BASE = Path("CENTRAL/REQUIREMENTS")

# =============================================================================
# FUNCTIONAL-REQUIREMENTS: Mapeamento por range numérico
# =============================================================================
RF_MAPPING = {
    "01-auth-security": range(1, 17),       # RF-001 a RF-016
    "02-tenants": range(17, 21),            # RF-017 a RF-020
    "03-users-teams": range(21, 33),        # RF-021 a RF-032
    "04-notifications": range(33, 34),      # RF-033
    "05-communities": range(34, 49),        # RF-034 a RF-048
    "06-units": range(49, 84),              # RF-049 a RF-083
    "07-holders": range(84, 102),           # RF-084 a RF-101
    "08-documents-media": range(102, 127),  # RF-102 a RF-126
    "09-layers-features": range(127, 142),  # RF-127 a RF-141
    "10-spatial-analysis": range(142, 153), # RF-142 a RF-152
    "11-annotations": range(153, 157),      # RF-153 a RF-156
    "12-surveys": range(157, 172),          # RF-157 a RF-171
    "13-legitimation": range(172, 182),     # RF-172 a RF-181
    "14-offline-sync": range(182, 197),     # RF-182 a RF-196
    "15-data-export": range(197, 203),      # RF-197 a RF-202
    "16-reports": range(203, 212),          # RF-203 a RF-211
    "17-wms-wmts": range(212, 222),         # RF-212 a RF-221
}

# =============================================================================
# USER-STORIES: Mapeamento semântico por US
# =============================================================================
US_MAPPING = {
    "01-auth-security": [1, 2, 3, 4, 5, 6, 7, 8, 124],
    "02-tenants": [83, 84, 116, 117, 118],
    "03-users-teams": [30, 110, 111, 112, 113, 114, 115],
    "04-notifications": [39, 46, 48],
    "05-communities": [100, 129, 130, 131],
    "06-units": [14, 15, 16, 17, 18, 19, 22, 24, 25, 34, 35, 36, 37, 38, 49,
                 125, 126, 127, 128, 132, 133, 134, 135, 136, 137, 140, 141],
    "07-holders": [26, 27, 28, 29, 31, 32, 33, 138, 139],
    "08-documents-media": [42, 43, 65, 66, 67, 68, 69, 70, 71],
    "09-layers-features": [155, 156, 157],
    "10-spatial-analysis": [21, 56, 57, 58, 59, 60, 61, 62, 63, 82],
    "11-annotations": [151, 152, 153, 154],
    "12-surveys": [142, 143, 144, 145, 146, 147, 148, 149, 150],
    "13-legitimation": [78, 79, 80, 81],
    "14-offline-sync": [40, 41, 44, 45, 47, 50, 51, 52, 53, 54, 55],
    "15-data-export": [20, 23, 72, 73, 102, 103, 109],
    "16-reports": [74, 75, 76, 77, 85, 86, 101, 104, 105, 106, 107, 108],
    "17-wms-wmts": [13, 64, 119, 120, 121, 122, 123],
}

# =============================================================================
# NON-FUNCTIONAL-REQUIREMENTS: Mapeamento por categoria
# =============================================================================
RNF_MAPPING = {
    "01-performance": [1, 2, 3, 4, 5, 10, 11, 15],
    "02-security": [16, 17, 18, 19, 20, 22, 23, 24, 25, 27, 28, 29, 30, 31, 33, 34, 35],
    "03-reliability": [36, 37, 38, 39, 40, 41, 42, 43, 45, 51, 55, 65],
    "04-usability": [14, 46, 47, 48, 49, 50, 52, 53, 54, 57, 62, 89, 90],
    "05-scalability": [6, 9, 12, 13, 21, 26, 32, 61, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 87],
    "06-compatibility": [7, 8, 44, 58, 81, 83, 84],
    "07-maintainability": [56, 59, 60, 63, 64, 82],
    "08-interoperability": [85, 86, 88],
}


def to_posix(path):
    """Converte path para formato POSIX (forward slashes)."""
    return str(path).replace("\\", "/")


def generate_rf_commands():
    """Gera comandos git mv para RF."""
    print("# " + "=" * 70)
    print("# FUNCTIONAL-REQUIREMENTS")
    print("# " + "=" * 70)

    rf_dir = BASE / "FUNCTIONAL-REQUIREMENTS"

    for folder, num_range in RF_MAPPING.items():
        print(f"\n# {folder}")
        for num in num_range:
            pattern = f"RF-{num:03d}-*.md"
            files = list(rf_dir.glob(pattern))
            for f in files:
                src = to_posix(f.relative_to(Path(".")))
                dst = to_posix((rf_dir / folder / f.name).relative_to(Path(".")))
                print(f'git mv "{src}" "{dst}"')


def generate_us_commands():
    """Gera comandos git mv para US."""
    print("\n\n# " + "=" * 70)
    print("# USER-STORIES")
    print("# " + "=" * 70)

    us_dir = BASE / "USER-STORIES"

    for folder, nums in US_MAPPING.items():
        print(f"\n# {folder}")
        for num in nums:
            pattern = f"US-{num:03d}-*.md"
            files = list(us_dir.glob(pattern))
            for f in files:
                src = to_posix(f.relative_to(Path(".")))
                dst = to_posix((us_dir / folder / f.name).relative_to(Path(".")))
                print(f'git mv "{src}" "{dst}"')


def generate_uc_commands():
    """Gera comandos git mv para UC (principal + FA + FE)."""
    print("\n\n# " + "=" * 70)
    print("# USE-CASES")
    print("# " + "=" * 70)

    uc_dir = BASE / "USE-CASES"

    # Lista de pastas UC
    uc_folders = [
        "UC-001-cadastrar-unidade-habitacional",
        "UC-002-aprovar-unidade-habitacional",
        "UC-003-vincular-titular-unidade",
        "UC-004-coletar-dados-campo-mobile",
        "UC-005-sincronizar-dados-offline",
        "UC-006-gerar-relatorio-comunidade",
        "UC-007-exportar-dados-geograficos",
        "UC-008-importar-shapefile",
        "UC-009-gerenciar-processo-legitimacao",
        "UC-010-configurar-camadas-wms",
        "UC-011-gerenciar-equipes-tecnicas",
    ]

    for folder in uc_folders:
        # Extrai número UC (ex: "001" de "UC-001-...")
        uc_num = folder.split("-")[1]
        print(f"\n# {folder}")

        # Move UC principal + todos FA e FE com mesmo número
        patterns = [
            f"UC-{uc_num}-*.md",      # UC principal
            f"UC-{uc_num}-FA-*.md",   # Fluxos alternativos
            f"UC-{uc_num}-FE-*.md",   # Fluxos de exceção
        ]

        for pattern in patterns:
            files = list(uc_dir.glob(pattern))
            for f in files:
                # Não mover se já está em subpasta
                if f.parent.name != "USE-CASES":
                    continue
                src = to_posix(f.relative_to(Path(".")))
                dst = to_posix((uc_dir / folder / f.name).relative_to(Path(".")))
                print(f'git mv "{src}" "{dst}"')


def generate_rnf_commands():
    """Gera comandos git mv para RNF."""
    print("\n\n# " + "=" * 70)
    print("# NON-FUNCTIONAL-REQUIREMENTS")
    print("# " + "=" * 70)

    rnf_dir = BASE / "NON-FUNCTIONAL-REQUIREMENTS"

    for folder, nums in RNF_MAPPING.items():
        print(f"\n# {folder}")
        for num in nums:
            pattern = f"RNF-{num:03d}-*.md"
            files = list(rnf_dir.glob(pattern))
            for f in files:
                src = to_posix(f.relative_to(Path(".")))
                dst = to_posix((rnf_dir / folder / f.name).relative_to(Path(".")))
                print(f'git mv "{src}" "{dst}"')


def main():
    print("#!/bin/bash")
    print("# Comandos git mv para reorganizar requisitos em pastas")
    print("# Gerado automaticamente - revise antes de executar")
    print(f"# Total esperado: 512 arquivos")
    print()

    generate_rf_commands()
    generate_us_commands()
    generate_uc_commands()
    generate_rnf_commands()

    print("\n\n# " + "=" * 70)
    print("# FIM")
    print("# " + "=" * 70)
    print('echo "Movimentação concluída!"')


if __name__ == "__main__":
    main()
