#!/bin/bash
# CARF HML — Deploy script
#
# Uso:
#   bash deploy.sh geoapi       # rebuild apenas geoapi
#   bash deploy.sh reurbweb     # pull + rebuild reurbweb
#   bash deploy.sh reurbmaster  # pull + rebuild reurbmaster
#   bash deploy.sh keycloak     # rebuild keycloak
#   bash deploy.sh frontends    # rebuild ambos frontends
#   bash deploy.sh all          # pull tudo + rebuild tudo
#
# Espera estar em ~/carf/ ou receber BASE como env var.
# Branch padrão: hml (ajustar BRANCH se necessário).
#
# Libs (@carffundiaria/tscore, @carffundiaria/geoapi-client, @carffundiaria/ui) are installed from
# GitHub Packages during Docker build — no need to clone them on the VPS.

set -euo pipefail

SERVICE="${1:-all}"
BASE="${BASE:-$HOME/carf}"
COMPOSE="$BASE/PROJECTS/DEPLOY/hml"
BRANCH="${BRANCH:-hml}"

# ─── Helpers ────────────────────────────────────────

pull() {
  local repo_dir="$BASE/$1"
  if [ ! -d "$repo_dir/.git" ]; then
    echo "[warn] $repo_dir não existe — ignorando"
    return 0
  fi
  echo "[pull] $1 (branch: $BRANCH)"
  git -C "$repo_dir" fetch origin
  git -C "$repo_dir" reset --hard "origin/$BRANCH"
}

rebuild() {
  echo "[build] $*"
  cd "$COMPOSE"
  docker compose up -d --build --no-deps "$@"
}

# ─── Paths dos repos ───────────────────────────────

GEOAPI="PROJECTS/GEOAPI/SRC-CODE/CARF-GEOAPI"
REURBWEB="PROJECTS/REURBWEB/SRC-CODE/carf-reurbweb"
REURBMASTER="PROJECTS/REURBMASTER/SRC-CODE/carf-reurbmaster"
KEYCLOAK="PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak"

# ─── Deploy por serviço ────────────────────────────

case "$SERVICE" in
  geoapi)
    pull "$GEOAPI"
    rebuild geoapi
    ;;

  reurbweb)
    pull "$REURBWEB"
    rebuild reurbweb
    ;;

  reurbmaster)
    pull "$REURBMASTER"
    rebuild reurbmaster
    ;;

  keycloak)
    pull "$KEYCLOAK"
    rebuild keycloak
    ;;

  frontends)
    pull "$REURBWEB"
    pull "$REURBMASTER"
    rebuild reurbweb reurbmaster
    ;;

  all)
    cd "$BASE" && bash PROJECTS/DEPLOY/hml/repos.sh pull
    cd "$COMPOSE" && docker compose up -d --build
    ;;

  *)
    echo "Uso: bash deploy.sh {geoapi|reurbweb|reurbmaster|keycloak|frontends|all}"
    exit 1
    ;;
esac

echo ""
echo "[ok] $SERVICE deployed at $(date)"
