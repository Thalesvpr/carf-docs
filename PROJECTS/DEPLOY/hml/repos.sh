#!/bin/bash
# CARF HML — Clona/atualiza todos os repos na estrutura correta
#
# Uso:
#   bash repos.sh          # clone inicial
#   bash repos.sh pull     # atualizar todos
#
# Resultado:
#   ~/carf/
#   ├── CENTRAL/INTEGRATION/KEYCLOAK/realm-export.json  (deste repo)
#   ├── PROJECTS/
#   │   ├── DEPLOY/hml/          (deste repo)
#   │   ├── GEOAPI/SRC-CODE/CARF-GEOAPI/
#   │   ├── REURBWEB/SRC-CODE/carf-reurbweb/
#   │   ├── REURBMASTER/SRC-CODE/carf-reurbmaster/
#   │   └── KEYCLOAK/SRC-CODE/carf-keycloak/
#   └── ...
#
# Libs (@carffundiaria/tscore, @carffundiaria/geoapi-client, @carffundiaria/ui) are NOT cloned here.
# They are installed from GitHub Packages during Docker build.

set -euo pipefail

# ─── Configuração ────────────────────────────────────
GH_ORG="carffundiaria"
BASE_DIR="${HOME}/carf"
ACTION="${1:-clone}"

# Repo → pasta destino (relativo a BASE_DIR) → branch
declare -A REPOS=(
  ["CARF"]=".|main"
  ["carf-geoapi"]="PROJECTS/GEOAPI/SRC-CODE/CARF-GEOAPI|main"
  ["carf-reurbweb"]="PROJECTS/REURBWEB/SRC-CODE/carf-reurbweb|main"
  ["carf-reurbmaster"]="PROJECTS/REURBMASTER/SRC-CODE/carf-reurbmaster|main"
  ["carf-keycloak"]="PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak|main"
)

# ─── Funções ─────────────────────────────────────────

clone_repo() {
  local name=$1
  local config=${REPOS[$name]}
  local dest="${BASE_DIR}/${config%%|*}"
  local branch="${config##*|}"

  if [ "$name" = "CARF" ]; then
    if [ ! -d "$dest/.git" ]; then
      echo "[clone] $name → $dest (branch: $branch)"
      git clone --branch "$branch" "https://github.com/${GH_ORG}/${name}.git" "$dest"
    else
      echo "[skip]  $name já existe em $dest"
    fi
  else
    if [ ! -d "$dest/.git" ]; then
      echo "[clone] $name → $dest (branch: $branch)"
      mkdir -p "$(dirname "$dest")"
      git clone --branch "$branch" "https://github.com/${GH_ORG}/${name}.git" "$dest"
    else
      echo "[skip]  $name já existe em $dest"
    fi
  fi
}

pull_repo() {
  local name=$1
  local config=${REPOS[$name]}
  local dest="${BASE_DIR}/${config%%|*}"
  local branch="${config##*|}"

  if [ -d "$dest/.git" ]; then
    echo "[pull]  $name ($branch) em $dest"
    git -C "$dest" fetch origin
    git -C "$dest" checkout "$branch"
    git -C "$dest" pull origin "$branch"
  else
    echo "[warn]  $name não encontrado em $dest — rodando clone"
    clone_repo "$name"
  fi
}

# ─── Execução ────────────────────────────────────────

echo "=== CARF HML — Repos (${ACTION}) ==="
echo "Base: ${BASE_DIR}"
echo ""

# CARF (repo principal) primeiro
if [ "$ACTION" = "pull" ]; then
  pull_repo "CARF"
else
  clone_repo "CARF"
fi

# Depois os sub-repos
for repo in "${!REPOS[@]}"; do
  [ "$repo" = "CARF" ] && continue
  if [ "$ACTION" = "pull" ]; then
    pull_repo "$repo"
  else
    clone_repo "$repo"
  fi
done

echo ""
echo "=== Pronto! Estrutura: ==="
echo "$BASE_DIR/"
for repo in "${!REPOS[@]}"; do
  config=${REPOS[$repo]}
  dest="${config%%|*}"
  echo "  ├── $dest/ ($repo)"
done
echo ""
echo "Próximo passo:"
echo "  cd ${BASE_DIR}/PROJECTS/DEPLOY/hml"
echo "  cp .env.example .env && nano .env"
echo "  docker compose up -d --build"
