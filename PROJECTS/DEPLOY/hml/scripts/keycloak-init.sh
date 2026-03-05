#!/bin/bash
# ============================================
# keycloak-init.sh — Configuracao automatica do Keycloak HML
# ============================================
# Roda como init container apos Keycloak estar healthy.
# Idempotente: pode rodar multiplas vezes sem efeito colateral.
#
# Variaveis esperadas (via docker-compose environment):
#   KC_ADMIN_USER, KC_ADMIN_PASSWORD, VPS_IP, KC_SEED_USER_PASSWORD

set -euo pipefail

KCADM="/opt/keycloak/bin/kcadm.sh"
SERVER="http://keycloak:8080"
REALM="carf"

log() { echo "[keycloak-init] $1"; }
ok()  { echo "[ok] $1"; }
fail() { echo "[FAIL] $1" >&2; exit 1; }

# --------------------------------------------------
# 1. Autenticar no kcadm (retry loop)
# --------------------------------------------------
log "Aguardando Keycloak ficar pronto..."
MAX_RETRIES=30
for i in $(seq 1 $MAX_RETRIES); do
  if $KCADM config credentials \
    --server "$SERVER" --realm master \
    --user "$KC_ADMIN_USER" --password "$KC_ADMIN_PASSWORD" 2>/dev/null; then
    ok "Autenticado no Keycloak (tentativa $i)"
    break
  fi
  if [ "$i" -eq "$MAX_RETRIES" ]; then
    fail "Nao conseguiu autenticar no Keycloak apos $MAX_RETRIES tentativas"
  fi
  sleep 5
done

# --------------------------------------------------
# 2. Desabilitar SSL required nos realms
# --------------------------------------------------
for r in master "$REALM"; do
  $KCADM update "realms/$r" -s sslRequired=NONE
  ok "sslRequired=NONE no realm '$r'"
done

# --------------------------------------------------
# 2b. Forcar tema CARF no realm
# --------------------------------------------------
$KCADM update "realms/$REALM" \
  -s loginTheme=carf \
  -s accountTheme=carf \
  -s emailTheme=carf
ok "Tema 'carf' aplicado no realm '$REALM'"

# --------------------------------------------------
# 3. Atualizar redirect URIs dos clients
# --------------------------------------------------
update_client_uris() {
  local client_id="$1"
  local hml_host="$2"
  local localhost_port="$3"

  # Buscar o UUID do client
  local uuid
  uuid=$($KCADM get clients -r "$REALM" -q "clientId=$client_id" --fields id \
    | grep '"id"' | head -1 | sed 's/.*: *"//;s/".*//')

  if [ -z "$uuid" ]; then
    log "WARN: Client '$client_id' nao encontrado — pulando"
    return
  fi

  $KCADM update "clients/$uuid" -r "$REALM" \
    -s "redirectUris=[\"http://${hml_host}/*\",\"http://localhost:${localhost_port}/*\"]" \
    -s "webOrigins=[\"http://${hml_host}\",\"http://localhost:${localhost_port}\"]"

  ok "URIs atualizadas para '$client_id' (HML + localhost:${localhost_port})"
}

update_client_uris "reurbweb"    "hml-app.${VPS_IP}.sslip.io"   "3000"
update_client_uris "reurbmaster" "hml-admin.${VPS_IP}.sslip.io" "5174"

# --------------------------------------------------
# 4. Criar usuario seed (se nao existe)
# --------------------------------------------------
SEED_USER="admin.hml"
SEED_PASSWORD="${KC_SEED_USER_PASSWORD:-Dev@1234}"

existing_user=$($KCADM get users -r "$REALM" -q "username=$SEED_USER" --fields id \
  | grep '"id"' | head -1 | sed 's/.*: *"//;s/".*//' || true)

if [ -z "$existing_user" ]; then
  $KCADM create users -r "$REALM" \
    -s "username=$SEED_USER" \
    -s "email=admin@carf.dev" \
    -s "enabled=true" \
    -s "firstName=Admin" \
    -s "lastName=HML" \
    -s "emailVerified=true"
  ok "Usuario '$SEED_USER' criado"

  # Buscar o ID do usuario recem-criado
  existing_user=$($KCADM get users -r "$REALM" -q "username=$SEED_USER" --fields id \
    | grep '"id"' | head -1 | sed 's/.*: *"//;s/".*//')
else
  ok "Usuario '$SEED_USER' ja existe"
fi

# --------------------------------------------------
# 5. Definir senha
# --------------------------------------------------
$KCADM set-password -r "$REALM" \
  --username "$SEED_USER" \
  --new-password "$SEED_PASSWORD"
ok "Senha definida para '$SEED_USER'"

# --------------------------------------------------
# 6. Atribuir roles
# --------------------------------------------------
for role in super-admin admin dev; do
  # Verifica se a role existe antes de tentar atribuir
  if $KCADM get "roles/$role" -r "$REALM" &>/dev/null; then
    $KCADM add-roles -r "$REALM" \
      --uusername "$SEED_USER" \
      --rolename "$role" 2>/dev/null || true
    ok "Role '$role' atribuida a '$SEED_USER'"
  else
    log "WARN: Role '$role' nao existe no realm — pulando"
  fi
done

# --------------------------------------------------
# 7. Definir atributos de tenant
# --------------------------------------------------
cat > /tmp/attrs.json <<EOF
{"attributes":{"current_tenant":["default"],"tenants":["default"]}}
EOF

$KCADM update "users/$existing_user" -r "$REALM" -f /tmp/attrs.json
rm -f /tmp/attrs.json
ok "Atributos de tenant definidos para '$SEED_USER'"

# --------------------------------------------------
echo ""
log "=== Configuracao concluida com sucesso ==="
