---
id: ""
type: ARCH
modules: []
epic: ""
status: review
created: 2026-01-21
updated: 2026-01-21
---

# Componentes Customizados

Especificação dos componentes Astro customizados usados no WEBDOCS além dos fornecidos pelo Starlight. Cada componente define propósito, props esperadas, comportamento e estados visuais.

## StatusGrid

Componente que exibe grid de cards mostrando status em tempo real dos serviços CARF na página de status.

```json
{
  "name": "StatusGrid",
  "path": "src/components/status/StatusGrid.astro",
  "props": {
    "services": {
      "type": "Service[]",
      "required": true,
      "description": "Array de serviços a monitorar"
    }
  },
  "service_type": {
    "name": { "type": "string", "description": "Nome exibido do serviço" },
    "url": { "type": "string", "description": "URL do health endpoint" },
    "timeout": { "type": "number", "default": 5000, "description": "Timeout em ms" },
    "critical": { "type": "boolean", "default": false, "description": "Se falha é crítica" }
  },
  "behavior": {
    "ssr": "Fetch paralelo de todos serviços com Promise.allSettled",
    "client": "Polling a cada 30s via client:idle hidratação",
    "timeout": "5 segundos por serviço, falha vira status unknown"
  },
  "states": {
    "online": { "color": "green", "icon": "check-circle", "label": "Operacional" },
    "offline": { "color": "red", "icon": "x-circle", "label": "Indisponível" },
    "degraded": { "color": "yellow", "icon": "alert-triangle", "label": "Degradado" },
    "unknown": { "color": "gray", "icon": "help-circle", "label": "Desconhecido" }
  }
}
```

## ServiceCard

Componente filho do StatusGrid que renderiza card individual para cada serviço.

```json
{
  "name": "ServiceCard",
  "path": "src/components/status/ServiceCard.astro",
  "props": {
    "name": { "type": "string", "required": true },
    "status": { "type": "online|offline|degraded|unknown", "required": true },
    "latency": { "type": "number|null", "description": "Latência em ms ou null se falhou" },
    "lastCheck": { "type": "Date", "description": "Timestamp da última verificação" },
    "critical": { "type": "boolean", "default": false }
  },
  "visual": {
    "layout": "Card com ícone de status, nome, latência e timestamp",
    "critical_badge": "Exibe badge 'Crítico' se critical=true e offline"
  }
}
```

## Banner

Componente de notificação global exibido no topo de todas as páginas para comunicar informações importantes.

```json
{
  "name": "Banner",
  "path": "src/components/content/Banner.astro",
  "props": {
    "type": {
      "type": "info|warning|error",
      "required": true,
      "description": "Tipo visual do banner"
    },
    "message": {
      "type": "string",
      "required": true,
      "description": "Mensagem a exibir"
    },
    "dismissible": {
      "type": "boolean",
      "default": true,
      "description": "Se usuário pode fechar o banner"
    },
    "id": {
      "type": "string",
      "description": "ID único para persistir dismiss em localStorage"
    }
  },
  "behavior": {
    "dismiss": "Salva em localStorage com TTL de 24h",
    "check": "Verifica localStorage antes de renderizar",
    "styling": "info=azul, warning=amarelo, error=vermelho"
  }
}
```

## YouTubeEmbed

Componente para embed responsivo de vídeos do YouTube com lazy loading.

```json
{
  "name": "YouTubeEmbed",
  "path": "src/components/content/YouTubeEmbed.astro",
  "props": {
    "videoId": {
      "type": "string",
      "required": true,
      "description": "ID do vídeo no YouTube (11 caracteres)"
    },
    "title": {
      "type": "string",
      "required": true,
      "description": "Título para acessibilidade"
    },
    "startTime": {
      "type": "number",
      "description": "Tempo inicial em segundos"
    }
  },
  "behavior": {
    "lazy": "Exibe thumbnail até click, carrega iframe depois",
    "aspect": "16:9 responsivo com container",
    "privacy": "Usa youtube-nocookie.com para embed"
  }
}
```

## SwaggerUI

Componente que renderiza documentação OpenAPI interativa usando Swagger UI.

```json
{
  "name": "SwaggerUI",
  "path": "src/components/content/SwaggerUI.astro",
  "props": {
    "specUrl": {
      "type": "string",
      "required": true,
      "description": "URL da spec OpenAPI JSON"
    },
    "defaultExpand": {
      "type": "none|list|full",
      "default": "list",
      "description": "Estado inicial de expansão"
    }
  },
  "behavior": {
    "ssr": "Fetch spec durante build/SSR, cache por 5 minutos",
    "auth": "Injeta header Authorization com token do usuário logado",
    "hydration": "client:visible para carregar apenas quando visível"
  }
}
```

## LoginButton

Componente de botão de login exibido no header para usuários não autenticados.

```json
{
  "name": "LoginButton",
  "path": "src/components/auth/LoginButton.astro",
  "props": {
    "returnUrl": {
      "type": "string",
      "description": "URL para retornar após login, default é página atual"
    }
  },
  "behavior": {
    "click": "Redirect para /auth/login com redirect param",
    "styling": "Botão primário consistente com @carf/ui"
  }
}
```

## UserMenu

Componente de menu dropdown exibido no header para usuários autenticados.

```json
{
  "name": "UserMenu",
  "path": "src/components/auth/UserMenu.astro",
  "props": {
    "user": {
      "type": "User",
      "required": true,
      "description": "Dados do usuário autenticado"
    }
  },
  "user_type": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "roles": { "type": "string[]" }
  },
  "behavior": {
    "display": "Avatar com iniciais ou foto, nome truncado",
    "dropdown": "Perfil, Configurações, Logout",
    "hydration": "client:idle para interatividade do dropdown"
  }
}
```

## ProtectedContent

Componente wrapper que oculta conteúdo baseado nas roles do usuário.

```json
{
  "name": "ProtectedContent",
  "path": "src/components/auth/ProtectedContent.astro",
  "props": {
    "requiredRoles": {
      "type": "string[]",
      "required": true,
      "description": "Roles necessárias para ver conteúdo"
    },
    "fallback": {
      "type": "string",
      "description": "Mensagem ou slot a exibir se sem permissão"
    }
  },
  "behavior": {
    "check": "Verifica Astro.locals.user.roles contra requiredRoles",
    "match": "Usuário precisa ter pelo menos uma das roles",
    "render": "Renderiza children se permitido, fallback caso contrário"
  }
}
```

## Integração com @carf/ui

Componentes React da biblioteca @carf/ui são usados via integração Astro React para elementos que requerem interatividade complexa como Toast, Dialog e DropdownMenu. A hidratação usa client:idle para maioria e client:visible para componentes pesados.

```json
{
  "carf_ui_components": {
    "Toast": {
      "usage": "Notificações de sucesso/erro",
      "hydration": "client:idle"
    },
    "Dialog": {
      "usage": "Modais de confirmação",
      "hydration": "client:idle"
    },
    "DropdownMenu": {
      "usage": "Menu do usuário no header",
      "hydration": "client:idle"
    }
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
