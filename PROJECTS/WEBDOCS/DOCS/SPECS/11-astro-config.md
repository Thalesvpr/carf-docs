# Configuração Astro

Especificação completa do arquivo astro.config.mjs que define comportamento do framework Astro com integração Starlight para o portal de documentação WEBDOCS.

A configuração base define site como URL de produção do portal, output como hybrid para combinar páginas estáticas com rotas dinâmicas (autenticação e status), e adapter usando @astrojs/vercel/serverless para deploy na plataforma Vercel com suporte a Server-Side Rendering quando necessário.

## Configuração Base

```json
{
  "site": "https://docs.carf.com.br",
  "output": "hybrid",
  "adapter": "@astrojs/vercel/serverless",
  "trailingSlash": "ignore"
}
```

## Integração Starlight

Starlight fornece estrutura de documentação com navegação, busca e tema. A configuração define title como nome exibido no header, logo com caminho para arquivo SVG em src/assets/, social com links para repositórios GitHub, e locales configurando português brasileiro como idioma padrão.

```json
{
  "starlight": {
    "title": "CARF Docs",
    "logo": {
      "src": "./src/assets/logo.svg",
      "alt": "CARF - Sistema de Regularização Fundiária"
    },
    "social": {
      "github": "https://github.com/carf"
    },
    "locales": {
      "root": {
        "label": "Português",
        "lang": "pt-BR"
      }
    },
    "sidebar": "definido em SPECS/09-sidebar-navegacao.md",
    "customCss": ["./src/styles/custom.css"],
    "components": {
      "Header": "./src/components/overrides/Header.astro",
      "SiteTitle": "./src/components/overrides/SiteTitle.astro"
    },
    "head": [
      {
        "tag": "meta",
        "attrs": {
          "name": "robots",
          "content": "noindex"
        },
        "condition": "draft pages only"
      }
    ],
    "pagination": true,
    "tableOfContents": {
      "minHeadingLevel": 2,
      "maxHeadingLevel": 3
    },
    "editLink": {
      "baseUrl": "https://github.com/carf/carf-webdocs/edit/main/"
    }
  }
}
```

## Integrações Adicionais

Além do Starlight, o projeto utiliza integrações para funcionalidades específicas. A integração @astrojs/react permite uso de componentes React da biblioteca @carf/ui com hidratação client-side. A integração @astrojs/mdx habilita uso de componentes em arquivos de conteúdo. A integração @astrojs/sitemap gera sitemap.xml automaticamente para SEO.

```json
{
  "integrations": [
    "@astrojs/starlight",
    "@astrojs/react",
    "@astrojs/mdx",
    "@astrojs/sitemap"
  ]
}
```

## Configuração Vite

Build tool Vite requer configuração específica para SSR com bibliotecas compartilhadas CARF. A opção ssr.noExternal lista pacotes que devem ser bundled ao invés de tratados como external, necessário para bibliotecas que usam imports específicos de Node.js.

```json
{
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
```

## Configuração de Build

Opções de build controlam output do processo de compilação. O campo outDir define diretório de saída como dist/, compressFiles habilita gzip dos assets, e inlineStylesheets configura threshold para inline de CSS pequeno.

```json
{
  "build": {
    "format": "directory",
    "assets": "_astro",
    "inlineStylesheets": "auto"
  }
}
```

## Markdown e MDX

Configuração de processamento Markdown define plugins remark e rehype para transformações do conteúdo. O plugin remark-gfm habilita GitHub Flavored Markdown com tabelas e checkboxes, rehype-slug adiciona IDs aos headings para deep linking, e rehype-autolink-headings cria links automáticos.

```json
{
  "markdown": {
    "remarkPlugins": ["remark-gfm"],
    "rehypePlugins": [
      "rehype-slug",
      ["rehype-autolink-headings", { "behavior": "wrap" }]
    ],
    "shikiConfig": {
      "theme": "github-dark",
      "wrap": true
    }
  }
}
```

## Variáveis de Ambiente

Astro distingue variáveis públicas (prefixo PUBLIC_) expostas ao cliente de variáveis privadas disponíveis apenas server-side. A configuração não define variáveis diretamente, mas documenta prefixos esperados conforme SPECS/12-env-vars.md.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
