# Endpoints de Autenticação

Especificação dos endpoints de autenticação do WEBDOCS que implementam fluxo OAuth2 Authorization Code com PKCE para integração com Keycloak.

## Visão Geral do Fluxo

O fluxo de autenticação segue padrão OAuth2 Authorization Code com PKCE para máxima segurança. Usuário inicia login, é redirecionado ao Keycloak, autentica, retorna com código, que é trocado por tokens salvos em cookies HttpOnly.

```json
{
  "flow": {
    "1": "Usuário clica em login",
    "2": "GET /auth/login gera PKCE e redireciona para Keycloak",
    "3": "Usuário autentica no Keycloak",
    "4": "Keycloak redireciona para /auth/callback com code",
    "5": "POST para Keycloak token endpoint troca code por tokens",
    "6": "Tokens salvos em cookies HttpOnly",
    "7": "Usuário redirecionado para página original"
  }
}
```

## GET /auth/login

Endpoint que inicia fluxo de autenticação gerando PKCE challenge e redirecionando para Keycloak.

```json
{
  "endpoint": "GET /auth/login",
  "path": "src/pages/auth/login.astro",
  "query_params": {
    "redirect": {
      "type": "string",
      "required": false,
      "default": "/",
      "description": "URL para retornar após login bem-sucedido",
      "validation": "Deve ser path relativo do mesmo domínio"
    }
  },
  "behavior": {
    "1_generate_pkce": {
      "code_verifier": "String aleatória de 43-128 caracteres",
      "code_challenge": "SHA256 hash do verifier, base64url encoded",
      "method": "S256"
    },
    "2_save_state": {
      "cookie": "auth_state",
      "content": {
        "code_verifier": "Salvo para validação no callback",
        "redirect": "URL original para retorno",
        "nonce": "Valor aleatório para prevenir replay"
      },
      "options": {
        "httpOnly": true,
        "secure": true,
        "sameSite": "lax",
        "maxAge": 600,
        "path": "/auth"
      }
    },
    "3_redirect": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/auth",
      "params": {
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "redirect_uri": "${PUBLIC_SITE_URL}/auth/callback",
        "response_type": "code",
        "scope": "openid profile email",
        "code_challenge": "${code_challenge}",
        "code_challenge_method": "S256",
        "state": "${nonce}"
      }
    }
  },
  "response": {
    "success": "302 Redirect para Keycloak authorize endpoint",
    "error": "500 se falha ao gerar PKCE"
  }
}
```

## GET /auth/callback

Endpoint que recebe código do Keycloak e troca por tokens.

```json
{
  "endpoint": "GET /auth/callback",
  "path": "src/pages/auth/callback.astro",
  "query_params": {
    "code": {
      "type": "string",
      "required": true,
      "description": "Authorization code do Keycloak"
    },
    "state": {
      "type": "string",
      "required": true,
      "description": "Nonce para validação contra CSRF"
    },
    "error": {
      "type": "string",
      "description": "Código de erro se autenticação falhou"
    },
    "error_description": {
      "type": "string",
      "description": "Descrição do erro"
    }
  },
  "behavior": {
    "1_validate_state": {
      "action": "Ler cookie auth_state e comparar nonce com state param",
      "error": "Redirect para /auth/login se não bater"
    },
    "2_check_error": {
      "action": "Se error param presente, exibir página de erro",
      "display": "Mensagem amigável baseada no error_description"
    },
    "3_exchange_code": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token",
      "method": "POST",
      "body": {
        "grant_type": "authorization_code",
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "client_secret": "${KEYCLOAK_CLIENT_SECRET}",
        "code": "${code}",
        "redirect_uri": "${PUBLIC_SITE_URL}/auth/callback",
        "code_verifier": "${code_verifier_from_cookie}"
      }
    },
    "4_save_tokens": {
      "access_token": {
        "cookie": "access_token",
        "httpOnly": true,
        "secure": true,
        "sameSite": "lax",
        "path": "/",
        "maxAge": "expires_in do response"
      },
      "refresh_token": {
        "cookie": "refresh_token",
        "httpOnly": true,
        "secure": true,
        "sameSite": "lax",
        "path": "/auth",
        "maxAge": "refresh_expires_in do response"
      }
    },
    "5_cleanup": {
      "action": "Deletar cookie auth_state"
    },
    "6_redirect": {
      "action": "Redirect para URL salva no state ou /"
    }
  },
  "response": {
    "success": "302 Redirect para página original",
    "error_state": "302 Redirect para /auth/login",
    "error_exchange": "Página de erro com retry link"
  }
}
```

## POST /auth/logout

Endpoint que limpa tokens e redireciona para logout do Keycloak.

```json
{
  "endpoint": "POST /auth/logout",
  "path": "src/pages/auth/logout.ts",
  "behavior": {
    "1_clear_cookies": {
      "access_token": "Deletar cookie setando maxAge=0",
      "refresh_token": "Deletar cookie setando maxAge=0"
    },
    "2_redirect": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/logout",
      "params": {
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "post_logout_redirect_uri": "${PUBLIC_SITE_URL}"
      }
    }
  },
  "response": {
    "success": "302 Redirect para Keycloak logout"
  }
}
```

## POST /auth/refresh

Endpoint que renova access_token usando refresh_token.

```json
{
  "endpoint": "POST /auth/refresh",
  "path": "src/pages/api/refresh.ts",
  "behavior": {
    "1_read_refresh": {
      "action": "Ler refresh_token do cookie",
      "error": "401 se cookie ausente"
    },
    "2_exchange": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token",
      "method": "POST",
      "body": {
        "grant_type": "refresh_token",
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "client_secret": "${KEYCLOAK_CLIENT_SECRET}",
        "refresh_token": "${refresh_token}"
      }
    },
    "3_update_cookies": {
      "action": "Atualizar access_token e refresh_token cookies com novos valores"
    }
  },
  "response": {
    "success": {
      "status": 200,
      "body": { "success": true, "expiresIn": "number" }
    },
    "error_missing": {
      "status": 401,
      "body": { "error": "no_refresh_token" }
    },
    "error_expired": {
      "status": 401,
      "body": { "error": "refresh_token_expired" }
    },
    "error_keycloak": {
      "status": 502,
      "body": { "error": "keycloak_unavailable" }
    }
  }
}
```

## GET /auth/cms

Endpoint especial para autenticação do Decap CMS via OAuth.

```json
{
  "endpoint": "GET /auth/cms",
  "path": "src/pages/auth/cms.astro",
  "description": "Proxy de autenticação para Decap CMS acessar GitHub",
  "behavior": {
    "flow": "OAuth implicit para GitHub via Decap backend",
    "reference": "Documentado em SPECS/15-decap-cms-config.md"
  }
}
```

## Segurança

Todas as comunicações usam HTTPS em produção. Tokens são armazenados em cookies HttpOnly prevenindo acesso via JavaScript. Refresh token tem path restrito a /auth/ minimizando exposição. PKCE previne ataques de interceptação de código. State/nonce previne CSRF.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
