# Tratamento de Erros

Especificação do tratamento de erros no WEBDOCS, cobrindo erros de autenticação, API, conteúdo e páginas de erro customizadas.

## Erros de Autenticação

```json
{
  "auth_errors": {
    "token_expired": {
      "detection": "JWT exp claim menor que timestamp atual",
      "action": [
        "Tentar refresh silencioso via /api/refresh",
        "Se sucesso: atualizar cookie, continuar request",
        "Se falha: redirect para /auth/login"
      ],
      "user_message": "Sua sessão expirou. Faça login novamente."
    },
    "token_invalid": {
      "detection": "JWT malformado ou assinatura inválida",
      "action": [
        "Limpar cookies access_token e refresh_token",
        "Redirect para /auth/login"
      ],
      "user_message": "Erro de autenticação. Faça login novamente."
    },
    "token_missing": {
      "detection": "Cookie access_token ausente",
      "action": "Redirect para /auth/login com return_url",
      "user_message": "Você precisa fazer login para acessar esta página."
    },
    "insufficient_role": {
      "detection": "Nenhuma role do usuário permite acesso à seção",
      "action": "Renderizar página 403",
      "user_message": "Você não tem permissão para acessar esta página.",
      "additional_info": "Lista de roles que teriam acesso"
    },
    "keycloak_unavailable": {
      "detection": "Timeout ou erro de rede ao contatar Keycloak",
      "action": "Renderizar página de erro com retry",
      "user_message": "Serviço de autenticação temporariamente indisponível. Tente novamente em alguns minutos."
    },
    "oauth_error": {
      "detection": "Keycloak retorna error param no callback",
      "action": "Renderizar página de erro com descrição",
      "user_message": "Erro durante autenticação: {error_description}",
      "common_errors": {
        "access_denied": "Acesso negado pelo usuário ou administrador",
        "invalid_scope": "Escopo solicitado não permitido",
        "server_error": "Erro interno do servidor de autenticação"
      }
    }
  }
}
```

## Erros de API (GeoAPI)

```json
{
  "api_errors": {
    "network_error": {
      "detection": "fetch throws TypeError ou AbortError (timeout)",
      "action": "Mostrar estado de erro com botão retry",
      "user_message": "Não foi possível conectar ao servidor. Verifique sua conexão.",
      "retry": "Botão para tentar novamente"
    },
    "timeout": {
      "detection": "AbortController timeout após 10s",
      "action": "Mostrar estado de erro com retry",
      "user_message": "A requisição demorou muito. Tente novamente."
    },
    "server_error_5xx": {
      "detection": "Response status 500-599",
      "action": [
        "Log error para monitoramento",
        "Mostrar mensagem genérica ao usuário"
      ],
      "user_message": "Erro interno do servidor. Nossa equipe foi notificada.",
      "logging": "Incluir request_id, status, endpoint"
    },
    "not_found_404": {
      "detection": "Response status 404",
      "action": "Mostrar mensagem específica de recurso não encontrado",
      "user_message": "O recurso solicitado não foi encontrado."
    },
    "unauthorized_401": {
      "detection": "Response status 401",
      "action": "Tentar refresh, se falhar redirect para login",
      "user_message": "Sessão inválida. Fazendo login novamente..."
    },
    "forbidden_403": {
      "detection": "Response status 403",
      "action": "Mostrar mensagem de permissão",
      "user_message": "Você não tem permissão para esta operação."
    },
    "validation_400": {
      "detection": "Response status 400 com body de validação",
      "action": "Exibir erros de validação específicos",
      "user_message": "Dados inválidos: {field}: {message}"
    }
  }
}
```

## Erros de Conteúdo

```json
{
  "content_errors": {
    "page_not_found": {
      "detection": "Slug não existe em content collection",
      "action": "Renderizar página 404 customizada",
      "user_message": "Esta página não existe ou foi movida.",
      "suggestions": [
        "Link para home",
        "Busca do site",
        "Páginas populares"
      ]
    },
    "source_missing": {
      "detection": "Campo source aponta para arquivo inexistente",
      "action": [
        "Log warning durante build",
        "Mostrar banner discreto na página"
      ],
      "user_message": "Documentação fonte não encontrada. Conteúdo pode estar desatualizado.",
      "severity": "Warning (não bloqueia exibição)"
    },
    "frontmatter_invalid": {
      "detection": "Zod validation falha no build",
      "action": "Build falha com erro detalhado",
      "developer_message": "Frontmatter inválido em {file}: {error}",
      "resolution": "Corrigir frontmatter antes de deploy"
    }
  }
}
```

## Páginas de Erro Customizadas

```json
{
  "error_pages": {
    "404": {
      "path": "src/pages/404.astro",
      "http_status": 404,
      "content": {
        "title": "Página não encontrada",
        "message": "A página que você está procurando não existe ou foi movida.",
        "actions": [
          { "label": "Ir para home", "href": "/" },
          { "label": "Buscar no site", "href": "/?search=true" }
        ],
        "suggestions": "Links para páginas populares"
      }
    },
    "403": {
      "path": "src/pages/403.astro",
      "http_status": 403,
      "content": {
        "title": "Acesso negado",
        "message": "Você não tem permissão para acessar esta página.",
        "details": "Esta seção requer uma das seguintes permissões: {roles}",
        "actions": [
          { "label": "Voltar", "href": "javascript:history.back()" },
          { "label": "Ir para home", "href": "/" },
          { "label": "Fazer logout", "href": "/auth/logout" }
        ],
        "contact": "Se você acredita que deveria ter acesso, contate o administrador."
      }
    },
    "500": {
      "path": "src/pages/500.astro",
      "http_status": 500,
      "content": {
        "title": "Erro interno",
        "message": "Algo deu errado. Nossa equipe foi notificada.",
        "actions": [
          { "label": "Tentar novamente", "href": "javascript:location.reload()" },
          { "label": "Ir para home", "href": "/" }
        ],
        "support": "Se o problema persistir, contate suporte@carf.com.br"
      }
    }
  }
}
```

## Logging

```json
{
  "error_logging": {
    "client_side": {
      "method": "console.error + opcional reporting service",
      "include": ["error message", "stack trace", "user action"]
    },
    "server_side": {
      "method": "Structured logging via pino ou similar",
      "include": [
        "timestamp",
        "request_id",
        "error_type",
        "error_message",
        "stack_trace",
        "user_id (if authenticated)",
        "endpoint",
        "method"
      ],
      "exclude": ["tokens", "passwords", "PII"]
    }
  }
}
```

## Error Boundaries (React)

```json
{
  "error_boundaries": {
    "purpose": "Capturar erros em componentes React hidratados",
    "implementation": "React ErrorBoundary wrapper",
    "fallback": "UI de erro com retry button",
    "logging": "Reportar erro para monitoramento"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
