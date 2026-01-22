---
type: leaf
status: review
updated: 2026-01-21
---

# Configurar Autenticação

Guia para configurar integração com Keycloak habilitando proteção da seção /dev/ e autenticação do CMS.

Obter credenciais do Keycloak com equipe de infraestrutura incluindo URL do realm CARF, client ID do client carf-webdocs, e URLs de redirect autorizadas para ambiente de desenvolvimento.

Configurar variáveis de ambiente em arquivo .env. Variável KEYCLOAK_URL define URL base do Keycloak incluindo realm (ex: auth.carf.example.com/realms/carf). Variável KEYCLOAK_CLIENT_ID define client ID (carf-webdocs). Variável PUBLIC_URL define URL do site para callbacks.

Testar fluxo de login acessando rota protegida /dev/ no navegador. Redirect para Keycloak indica configuração correta de URL. Login com credenciais de desenvolvedor. Retorno para site indica callback configurado.

Verificar role dev acessando página que requer role. Usuário sem role deve ver página 403. Usuário com role deve ver conteúdo normalmente. Se role não atribuída, solicitar ao admin do Keycloak.

Testar logout acessando /auth/logout. Redirect para Keycloak logout e retorno para home indica fluxo completo funcionando. Tentar acessar /dev/ após logout deve redirecionar para login.

Configurar CMS em admin/config.yml ajustando backend para usar OAuth via Keycloak ao invés de GitHub nativo. Redirect URI do admin deve estar na lista de URIs autorizadas do client no Keycloak.

Troubleshooting comum inclui erro de redirect_uri quando URL não está autorizada no Keycloak, erro de CORS quando origem não está em Web Origins do client, e loop de redirect quando cookies não são salvos (verificar HTTPS e SameSite).

## Configuração Detalhada

### Variáveis de Ambiente

```bash
# .env.local para desenvolvimento
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=carf
KEYCLOAK_CLIENT_ID=carf-webdocs

# Para produção (Vercel)
# KEYCLOAK_URL=https://auth.carf.com.br
# KEYCLOAK_REALM=carf
# KEYCLOAK_CLIENT_ID=carf-webdocs
```

### Verificar Client no Keycloak

1. Acessar Keycloak Admin Console
2. Selecionar Realm "carf"
3. Ir para Clients → carf-webdocs
4. Verificar configurações:

```json
{
  "client_settings_required": {
    "Client Protocol": "openid-connect",
    "Access Type": "public",
    "Standard Flow Enabled": true,
    "Direct Access Grants Enabled": false,
    "Valid Redirect URIs": [
      "http://localhost:4321/auth/callback",
      "https://docs.carf.com.br/auth/callback"
    ],
    "Web Origins": [
      "http://localhost:4321",
      "https://docs.carf.com.br"
    ],
    "PKCE Code Challenge Method": "S256"
  }
}
```

### Fluxo de Teste Completo

```json
{
  "test_flow": [
    {
      "step": 1,
      "action": "Acessar http://localhost:4321/dev/",
      "expected": "Redirect para Keycloak login"
    },
    {
      "step": 2,
      "action": "Fazer login com credenciais dev",
      "expected": "Redirect de volta para /dev/"
    },
    {
      "step": 3,
      "action": "Verificar cookie no DevTools",
      "expected": "carf_access_token presente"
    },
    {
      "step": 4,
      "action": "Acessar /auth/logout",
      "expected": "Redirect para Keycloak logout, depois home"
    },
    {
      "step": 5,
      "action": "Acessar /dev/ novamente",
      "expected": "Redirect para login (não autenticado)"
    }
  ]
}
```

### Troubleshooting Detalhado

```json
{
  "troubleshooting": {
    "redirect_uri_error": {
      "error": "Invalid parameter: redirect_uri",
      "check": "URI exata deve estar em Valid Redirect URIs do client",
      "fix": "Adicionar http://localhost:4321/auth/callback no Keycloak"
    },
    "cors_error": {
      "error": "Access-Control-Allow-Origin not present",
      "check": "Origin deve estar em Web Origins do client",
      "fix": "Adicionar http://localhost:4321 em Web Origins"
    },
    "redirect_loop": {
      "error": "Too many redirects",
      "checks": [
        "Cookie está sendo salvo? (DevTools → Application → Cookies)",
        "SameSite=Lax está configurado?",
        "Em localhost HTTP, Secure deve ser false"
      ]
    },
    "403_forbidden": {
      "error": "Acesso negado mesmo logado",
      "check": "Usuário tem role 'dev' no Keycloak?",
      "fix": "Keycloak → Users → seu user → Role Mappings → adicionar 'dev'"
    },
    "token_expired": {
      "error": "401 após alguns minutos",
      "check": "Refresh está funcionando?",
      "fix": "Verificar refresh_token cookie e endpoint /auth/refresh"
    }
  }
}
```

### Debug de JWT

Para inspecionar o token JWT:

1. Abrir DevTools → Application → Cookies
2. Copiar valor de `carf_access_token`
3. Colar em https://jwt.io
4. Verificar claims:
   - `realm_access.roles` deve conter suas roles
   - `exp` deve ser futuro
   - `iss` deve ser URL do Keycloak

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
