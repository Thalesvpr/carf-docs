#!/bin/bash
# =============================================================================
# Setup REURBMASTER Authentication Flow
# Restricts login to users with admin, super-admin, or dev realm roles.
# Run against a local Keycloak instance (http://localhost:8080).
#
# ⚠️  DISABLED (Feb 2026): This custom flow causes ALL browser logins to fail
# with `invalid_user_credentials` (User: anon). Root cause: the conditional
# sub-flow structure breaks the browser flow execution in Keycloak 26.x.
# The reurbmaster client now uses the default realm browser flow, and role
# restriction is enforced via RoleGuard in the frontend instead.
# DO NOT run this script unless the flow issue has been fixed.
# =============================================================================

set -euo pipefail

KC_URL="${KC_URL:-http://localhost:8080}"
KC_REALM="carf"
KC_ADMIN_USER="${KC_ADMIN_USER:-admin}"
KC_ADMIN_PASS="${KC_ADMIN_PASS:-admin}"
CLIENT_ID="reurbmaster"

echo "=== REURBMASTER Auth Flow Setup ==="
echo "Keycloak: $KC_URL"
echo "Realm:    $KC_REALM"
echo ""

# 1. Get admin token
echo "[1/8] Getting admin token..."
TOKEN=$(curl -s -X POST "$KC_URL/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$KC_ADMIN_USER" \
  -d "password=$KC_ADMIN_PASS" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "ERROR: Failed to get admin token. Check KC_ADMIN_USER/KC_ADMIN_PASS."
  exit 1
fi
echo "  OK"

AUTH="Authorization: Bearer $TOKEN"
CT="Content-Type: application/json"

# 2. Check if flow already exists
echo "[2/8] Checking if reurbmaster-browser flow already exists..."
EXISTING=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows" \
  -H "$AUTH" | python3 -c "
import sys, json
flows = json.load(sys.stdin)
for f in flows:
    if f.get('alias') == 'reurbmaster-browser':
        print(f['id'])
        break
" 2>/dev/null || echo "")

if [ -n "$EXISTING" ]; then
  echo "  Flow already exists (id=$EXISTING). Deleting to recreate..."
  # First unbind from client
  CLIENT_UUID=$(curl -s "$KC_URL/admin/realms/$KC_REALM/clients" \
    -H "$AUTH" | python3 -c "
import sys, json
clients = json.load(sys.stdin)
for c in clients:
    if c.get('clientId') == '$CLIENT_ID':
        print(c['id'])
        break
" 2>/dev/null || echo "")
  if [ -n "$CLIENT_UUID" ]; then
    curl -s -X PUT "$KC_URL/admin/realms/$KC_REALM/clients/$CLIENT_UUID" \
      -H "$AUTH" -H "$CT" \
      -d "{\"id\":\"$CLIENT_UUID\",\"clientId\":\"$CLIENT_ID\",\"authenticationFlowBindingOverrides\":{}}" > /dev/null
  fi
  curl -s -X DELETE "$KC_URL/admin/realms/$KC_REALM/authentication/flows/$EXISTING" \
    -H "$AUTH" > /dev/null
  echo "  Deleted."
fi

# 3. Create top-level flow: reurbmaster-browser
echo "[3/8] Creating reurbmaster-browser flow..."
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-browser",
    "description": "Browser flow for REURBMASTER — restricted to admin/super-admin/dev roles",
    "providerId": "basic-flow",
    "topLevel": true,
    "builtIn": false
  }' > /dev/null
echo "  OK"

# Get the flow ID
FLOW_ID=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows" \
  -H "$AUTH" | python3 -c "
import sys, json
flows = json.load(sys.stdin)
for f in flows:
    if f.get('alias') == 'reurbmaster-browser':
        print(f['id'])
        break
" 2>/dev/null)
echo "  Flow ID: $FLOW_ID"

# 4. Add Cookie authenticator (ALTERNATIVE)
echo "[4/8] Adding Cookie authenticator..."
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "auth-cookie"}' > /dev/null

# Set Cookie to ALTERNATIVE
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions" -H "$AUTH")
COOKIE_EXEC_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
for e in execs:
    if e.get('providerId') == 'auth-cookie':
        print(e['id'])
        break
" 2>/dev/null)
curl -s -X PUT "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions" \
  -H "$AUTH" -H "$CT" \
  -d "{\"id\":\"$COOKIE_EXEC_ID\",\"requirement\":\"ALTERNATIVE\"}" > /dev/null
echo "  OK"

# 5. Add Forms sub-flow (ALTERNATIVE)
echo "[5/8] Adding forms sub-flow..."
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions/flow" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-forms",
    "description": "Username/password + optional OTP",
    "provider": "registration-page-form",
    "type": "basic-flow"
  }' > /dev/null

# Set forms sub-flow to ALTERNATIVE
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions" -H "$AUTH")
FORMS_EXEC_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
for e in execs:
    if e.get('displayName') == 'reurbmaster-forms':
        print(e['id'])
        break
" 2>/dev/null)
curl -s -X PUT "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions" \
  -H "$AUTH" -H "$CT" \
  -d "{\"id\":\"$FORMS_EXEC_ID\",\"requirement\":\"ALTERNATIVE\"}" > /dev/null

# Add username-password-form to forms sub-flow
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-forms/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "auth-username-password-form"}' > /dev/null
echo "  OK"

# 6. Add conditional OTP sub-flow inside forms
echo "[6/8] Adding conditional OTP sub-flow..."
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-forms/executions/flow" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-conditional-otp",
    "description": "OTP if user has configured it",
    "provider": "registration-page-form",
    "type": "basic-flow"
  }' > /dev/null

# Set OTP sub-flow to CONDITIONAL
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-forms/executions" -H "$AUTH")
OTP_FLOW_EXEC_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
for e in execs:
    if e.get('displayName') == 'reurbmaster-conditional-otp':
        print(e['id'])
        break
" 2>/dev/null)
curl -s -X PUT "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-forms/executions" \
  -H "$AUTH" -H "$CT" \
  -d "{\"id\":\"$OTP_FLOW_EXEC_ID\",\"requirement\":\"CONDITIONAL\"}" > /dev/null

# Add conditional-user-configured and auth-otp-form
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-conditional-otp/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "conditional-user-configured"}' > /dev/null
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-conditional-otp/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "auth-otp-form"}' > /dev/null
echo "  OK"

# 7. Add role check sub-flow (CONDITIONAL) — deny non-admin/non-dev
echo "[7/8] Adding role check deny sub-flow..."
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions/flow" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-deny-non-admin",
    "description": "Deny access if user lacks admin or dev role",
    "provider": "registration-page-form",
    "type": "basic-flow"
  }' > /dev/null

# Set to CONDITIONAL
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions" -H "$AUTH")
DENY_FLOW_EXEC_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
for e in execs:
    if e.get('displayName') == 'reurbmaster-deny-non-admin':
        print(e['id'])
        break
" 2>/dev/null)
curl -s -X PUT "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-browser/executions" \
  -H "$AUTH" -H "$CT" \
  -d "{\"id\":\"$DENY_FLOW_EXEC_ID\",\"requirement\":\"CONDITIONAL\"}" > /dev/null

# Add condition: NOT admin
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-deny-non-admin/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "conditional-user-role"}' > /dev/null

# Configure the condition
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-deny-non-admin/executions" -H "$AUTH")
COND_ADMIN_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
for e in execs:
    if e.get('providerId') == 'conditional-user-role':
        print(e['id'])
        break
" 2>/dev/null)

# Create config for NOT admin
NEW_CONFIG=$(curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/executions/$COND_ADMIN_ID/config" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-not-admin",
    "config": {
      "condUserRole": "admin",
      "negate": "true"
    }
  }')
echo "  Condition NOT admin configured"

# Add condition: NOT dev
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-deny-non-admin/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "conditional-user-role"}' > /dev/null

# Get the second conditional-user-role execution
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-deny-non-admin/executions" -H "$AUTH")
COND_DEV_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
found = []
for e in execs:
    if e.get('providerId') == 'conditional-user-role':
        found.append(e['id'])
# Second one is the NOT dev condition
if len(found) >= 2:
    print(found[1])
" 2>/dev/null)

# Create config for NOT dev
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/executions/$COND_DEV_ID/config" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-not-dev",
    "config": {
      "condUserRole": "dev",
      "negate": "true"
    }
  }' > /dev/null
echo "  Condition NOT dev configured"

# Add deny-access-authenticator
curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-deny-non-admin/executions/execution" \
  -H "$AUTH" -H "$CT" \
  -d '{"provider": "deny-access-authenticator"}' > /dev/null

# Configure deny message
EXECUTIONS=$(curl -s "$KC_URL/admin/realms/$KC_REALM/authentication/flows/reurbmaster-deny-non-admin/executions" -H "$AUTH")
DENY_EXEC_ID=$(echo "$EXECUTIONS" | python3 -c "
import sys, json
execs = json.load(sys.stdin)
for e in execs:
    if e.get('providerId') == 'deny-access-authenticator':
        print(e['id'])
        break
" 2>/dev/null)

curl -s -X POST "$KC_URL/admin/realms/$KC_REALM/authentication/executions/$DENY_EXEC_ID/config" \
  -H "$AUTH" -H "$CT" \
  -d '{
    "alias": "reurbmaster-deny-message",
    "config": {
      "error_message": "Acesso restrito. Apenas administradores e desenvolvedores podem acessar o REURBMASTER."
    }
  }' > /dev/null
echo "  Deny Access configured"

# 8. Bind flow to reurbmaster client
echo "[8/8] Binding flow to reurbmaster client..."
CLIENT_UUID=$(curl -s "$KC_URL/admin/realms/$KC_REALM/clients" \
  -H "$AUTH" | python3 -c "
import sys, json
clients = json.load(sys.stdin)
for c in clients:
    if c.get('clientId') == '$CLIENT_ID':
        print(c['id'])
        break
" 2>/dev/null)

if [ -z "$CLIENT_UUID" ]; then
  echo "  ERROR: Client '$CLIENT_ID' not found!"
  exit 1
fi

# Get full client representation and update
CLIENT_JSON=$(curl -s "$KC_URL/admin/realms/$KC_REALM/clients/$CLIENT_UUID" -H "$AUTH")
UPDATED_CLIENT=$(echo "$CLIENT_JSON" | python3 -c "
import sys, json
client = json.load(sys.stdin)
client['authenticationFlowBindingOverrides'] = {'browser': '$FLOW_ID'}
print(json.dumps(client))
")

curl -s -X PUT "$KC_URL/admin/realms/$KC_REALM/clients/$CLIENT_UUID" \
  -H "$AUTH" -H "$CT" \
  -d "$UPDATED_CLIENT" > /dev/null
echo "  OK — Flow bound to client '$CLIENT_ID'"

echo ""
echo "=== DONE ==="
echo "The reurbmaster client now uses the custom authentication flow."
echo "Non-admin/non-dev users will see: 'Acesso restrito...'"
echo ""
echo "Test: try logging into http://localhost:5174 with a non-admin user."
