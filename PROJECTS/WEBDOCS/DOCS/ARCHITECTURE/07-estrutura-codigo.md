---
id: ""
type: ARCH
modules: []
epic: ""
status: review
created: 2026-01-21
updated: 2026-01-21
---

# Estrutura de Código

Especificação da estrutura de diretórios e arquivos do código fonte do WEBDOCS, definindo onde cada tipo de arquivo deve ser criado.

## Visão Geral

O projeto segue convenções do Astro com customizações para integração Starlight e bibliotecas CARF.

```json
{
  "root": "SRC-CODE/carf-webdocs/",
  "package_manager": "bun",
  "framework": "Astro 4.x",
  "template": "Starlight"
}
```

## Estrutura de Diretórios

```json
{
  "structure": {
    "src/": {
      "description": "Código fonte da aplicação",
      "content/": {
        "description": "Content Collections do Astro",
        "docs/": {
          "description": "Páginas de documentação MDX",
          "guia/": "Páginas de guia do usuário",
          "sistema/": "Páginas sobre o sistema CARF",
          "manuais/": {
            "geoweb/": "Manual GeoWeb",
            "reurbcad/": "Manual REURBCAD",
            "admin/": "Manual Admin"
          },
          "api/": "Documentação de API",
          "dev/": "Documentação para desenvolvedores",
          "status/": "Página de status (single page)",
          "changelog/": "Histórico de versões"
        },
        "incidents/": "Incidentes para status page",
        "config.ts": "Schema Zod para frontmatter"
      },
      "pages/": {
        "description": "Rotas Astro (SSR e API)",
        "auth/": {
          "login.astro": "Inicia fluxo OAuth PKCE",
          "callback.astro": "Recebe código e troca por tokens",
          "logout.ts": "Endpoint de logout",
          "cms.astro": "OAuth proxy para Decap CMS"
        },
        "api/": {
          "health.ts": "Health check da aplicação",
          "refresh.ts": "Refresh de token",
          "status.ts": "Status dos serviços para polling"
        },
        "[...slug].astro": "Catch-all para rotas Starlight"
      },
      "components/": {
        "description": "Componentes Astro reutilizáveis",
        "auth/": {
          "LoginButton.astro": "Botão de login",
          "UserMenu.astro": "Menu do usuário logado",
          "ProtectedContent.astro": "Wrapper para conteúdo protegido"
        },
        "status/": {
          "StatusGrid.astro": "Grid de status dos serviços",
          "ServiceCard.astro": "Card individual de serviço"
        },
        "content/": {
          "Banner.astro": "Banner de notificações",
          "YouTubeEmbed.astro": "Embed de vídeo",
          "SwaggerUI.astro": "Swagger embutido"
        },
        "overrides/": {
          "Header.astro": "Override do header Starlight",
          "SiteTitle.astro": "Override do título"
        }
      },
      "layouts/": {
        "BaseLayout.astro": "Layout base com auth check"
      },
      "lib/": {
        "description": "Código TypeScript utilitário",
        "auth/": {
          "pkce.ts": "Funções PKCE (generate, verify)",
          "tokens.ts": "Gerenciamento de tokens JWT",
          "middleware.ts": "Lógica do middleware de auth"
        },
        "services/": {
          "health.ts": "Client para health checks",
          "swagger.ts": "Client para Swagger spec"
        },
        "config/": {
          "env.ts": "Validação de variáveis de ambiente",
          "services.ts": "Configuração de serviços monitorados"
        }
      },
      "styles/": {
        "custom.css": "Customizações do tema Starlight"
      },
      "assets/": {
        "logo.svg": "Logo CARF",
        "favicon.svg": "Favicon"
      },
      "middleware.ts": "Entry point do middleware Astro"
    },
    "public/": {
      "description": "Arquivos estáticos servidos diretamente",
      "admin/": {
        "index.html": "Entry point Decap CMS",
        "config.yml": "Configuração Decap CMS"
      },
      "images/": "Imagens estáticas",
      "robots.txt": "Configuração de crawlers",
      "favicon.ico": "Fallback favicon"
    },
    "tests/": {
      "description": "Testes automatizados",
      "e2e/": "Testes Playwright end-to-end",
      "unit/": "Testes unitários Vitest"
    }
  }
}
```

## Arquivos de Configuração na Raiz

```json
{
  "config_files": {
    "astro.config.mjs": "Configuração principal Astro",
    "package.json": "Dependências e scripts",
    "tsconfig.json": "Configuração TypeScript",
    ".env.example": "Template de variáveis de ambiente",
    ".gitignore": "Arquivos ignorados pelo Git",
    "biome.json": "Configuração do linter Biome",
    "playwright.config.ts": "Configuração Playwright",
    "vitest.config.ts": "Configuração Vitest"
  }
}
```

## Convenções de Nomenclatura

```json
{
  "naming": {
    "components": {
      "pattern": "PascalCase.astro",
      "examples": ["StatusGrid.astro", "UserMenu.astro"]
    },
    "pages": {
      "pattern": "kebab-case.astro ou [param].astro",
      "examples": ["login.astro", "[...slug].astro"]
    },
    "api_routes": {
      "pattern": "kebab-case.ts",
      "examples": ["health.ts", "refresh.ts"]
    },
    "lib_modules": {
      "pattern": "kebab-case.ts",
      "examples": ["pkce.ts", "tokens.ts"]
    },
    "content": {
      "pattern": "kebab-case.mdx",
      "examples": ["primeiros-passos.mdx", "cadastro-unidade.mdx"]
    },
    "styles": {
      "pattern": "kebab-case.css",
      "examples": ["custom.css"]
    }
  }
}
```

## Onde Criar Cada Tipo de Arquivo

```json
{
  "file_placement": {
    "nova_pagina_docs": "src/content/docs/{secao}/",
    "novo_componente_ui": "src/components/{categoria}/",
    "nova_rota_api": "src/pages/api/",
    "nova_funcao_util": "src/lib/{dominio}/",
    "novo_estilo": "src/styles/",
    "nova_imagem": "public/images/",
    "novo_teste_e2e": "tests/e2e/",
    "novo_teste_unit": "tests/unit/"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
