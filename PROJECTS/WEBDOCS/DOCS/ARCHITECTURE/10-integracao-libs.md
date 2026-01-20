# Integração com Bibliotecas

Especificação da integração do WEBDOCS com as bibliotecas TypeScript compartilhadas do ecossistema CARF: @carf/tscore, @carf/geoapi-client e @carf/ui.

## Dependências

```json
{
  "dependencies": {
    "@carf/tscore": {
      "version": "workspace:*",
      "usage": "Value Objects, validações, types compartilhados",
      "examples": ["CPF", "Email", "GeoPoint"],
      "hydration": "Não requer (TypeScript puro)",
      "bundle_impact": "~5kb (tree-shakeable)"
    },
    "@carf/geoapi-client": {
      "version": "workspace:*",
      "usage": "Chamadas HTTP para GeoAPI",
      "examples": ["client.units.list()", "client.auth.refresh()"],
      "hydration": "Não requer (usado em server-side)",
      "bundle_impact": "~15kb (não incluído no client bundle)"
    },
    "@carf/ui": {
      "version": "workspace:*",
      "usage": "Componentes React para UI interativa",
      "examples": ["Button", "Dialog", "Toast", "DropdownMenu"],
      "hydration": "Requer client:idle ou client:visible",
      "bundle_impact": "~40kb de React + componentes usados"
    }
  }
}
```

## Configuração Astro para React

Para usar componentes React da @carf/ui, o projeto requer integração React.

```json
{
  "astro_config": {
    "integrations": ["@astrojs/react"],
    "vite": {
      "ssr": {
        "noExternal": [
          "@carf/ui",
          "@carf/tscore",
          "@carf/geoapi-client"
        ]
      },
      "optimizeDeps": {
        "include": ["react", "react-dom"]
      }
    }
  }
}
```

A opção ssr.noExternal garante que os pacotes CARF sejam bundled durante SSR ao invés de tratados como external, necessário porque usam imports específicos que não funcionam como external em Node.js.

## Uso de @carf/tscore

Biblioteca base com Value Objects e validações. Usada principalmente em TypeScript server-side.

```json
{
  "tscore_usage": {
    "value_objects": {
      "import": "import { CPF, Email, GeoPoint } from '@carf/tscore'",
      "usage": [
        "Validação de dados de formulário",
        "Tipagem de dados da API",
        "Formatação para exibição"
      ]
    },
    "validators": {
      "import": "import { validateCPF, validateEmail } from '@carf/tscore'",
      "usage": "Validação client-side antes de submit"
    },
    "types": {
      "import": "import type { Unit, Holder, Community } from '@carf/tscore'",
      "usage": "Tipagem de responses da GeoAPI"
    }
  }
}
```

## Uso de @carf/geoapi-client

SDK HTTP para comunicação com GeoAPI. Usado apenas server-side ou em API routes.

```json
{
  "geoapi_client_usage": {
    "initialization": {
      "location": "src/lib/services/geoapi.ts",
      "config": {
        "baseUrl": "${GEOAPI_URL}",
        "timeout": 10000,
        "retry": { "count": 2, "delay": 1000 }
      }
    },
    "usage_contexts": {
      "ssr_pages": "Fetch dados durante renderização",
      "api_routes": "Proxy requests do cliente para GeoAPI",
      "health_checks": "Verificar disponibilidade da API"
    },
    "auth_injection": {
      "method": "Interceptor adiciona header Authorization",
      "token_source": "Cookie access_token do request"
    }
  }
}
```

## Uso de @carf/ui

Componentes React para interatividade. Requerem hidratação client-side.

```json
{
  "ui_usage": {
    "recommended_components": {
      "interactive_required": {
        "Toast": {
          "usage": "Notificações de sucesso/erro",
          "hydration": "client:idle",
          "wrapper": "Criar ToastProvider.astro"
        },
        "Dialog": {
          "usage": "Modais de confirmação",
          "hydration": "client:idle"
        },
        "DropdownMenu": {
          "usage": "Menu do usuário no header",
          "hydration": "client:idle"
        }
      },
      "optional": {
        "Button": {
          "note": "Pode usar Astro nativo, @carf/ui garante consistência visual",
          "when": "Botões com handlers complexos"
        },
        "Input": {
          "note": "Para formulários de busca avançada",
          "when": "Validação em tempo real necessária"
        }
      },
      "avoid": {
        "Table": "Starlight já tem tabelas markdown otimizadas",
        "Card": "Usar componentes Astro nativos para cards estáticos"
      }
    }
  }
}
```

## Padrão de Wrapper Astro para React

Para usar componentes React em páginas Astro, criar wrapper components.

```json
{
  "wrapper_pattern": {
    "purpose": "Encapsular componente React com hidratação apropriada",
    "structure": {
      "1": "Componente Astro que importa React component",
      "2": "Define props no frontmatter",
      "3": "Renderiza React component com diretiva de hidratação"
    },
    "example": {
      "file": "src/components/auth/UserMenuWrapper.astro",
      "imports": "@carf/ui DropdownMenu components",
      "props": "user: User",
      "render": "<DropdownMenu client:idle>...</DropdownMenu>"
    }
  }
}
```

## Tree Shaking

Bibliotecas CARF são tree-shakeable. Importar apenas o necessário.

```json
{
  "tree_shaking": {
    "do": "import { Button, Dialog } from '@carf/ui'",
    "dont": "import * as UI from '@carf/ui'",
    "reason": "Import seletivo permite bundler remover código não usado"
  }
}
```

## Versioning

Bibliotecas CARF usam workspace protocol para garantir versões consistentes no monorepo.

```json
{
  "versioning": {
    "protocol": "workspace:*",
    "meaning": "Sempre usa versão local do workspace",
    "publish": "Resolve para versão específica ao publicar"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
