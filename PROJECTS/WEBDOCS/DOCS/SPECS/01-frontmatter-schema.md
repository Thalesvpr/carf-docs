# Frontmatter Schema

Schema Zod define campos obrigatórios e opcionais do frontmatter para todos documentos do WEBDOCS. Validação acontece em build time garantindo consistência e rastreabilidade com documentação fonte em CENTRAL e PROJECTS.

## Campos Obrigatórios

Campos obrigatórios incluem title como string não vazia exibida no browser tab, sidebar e breadcrumbs, description como string de 50-160 caracteres para SEO e previews em buscas, e source como caminho para arquivo fonte em CENTRAL ou PROJECTS garantindo rastreabilidade.

## Schema JSON Completo

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["title", "description", "source"],
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "description": "Título exibido no browser tab, sidebar e breadcrumbs"
    },
    "description": {
      "type": "string",
      "minLength": 50,
      "maxLength": 160,
      "description": "Descrição para SEO e previews em buscas"
    },
    "source": {
      "type": "string",
      "pattern": "^(CENTRAL|PROJECTS)/.*\\.md$",
      "description": "Caminho para arquivo fonte garantindo rastreabilidade",
      "examples": [
        "CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md",
        "PROJECTS/GEOWEB/DOCS/FEATURES/01-map-navigation.md"
      ]
    },
    "lastUpdated": {
      "type": "string",
      "format": "date",
      "description": "Data ISO da última modificação significativa"
    },
    "section": {
      "type": "string",
      "enum": ["guia", "sistema", "manuais", "api", "dev", "status", "changelog"],
      "description": "Seção do portal que determina acesso por role"
    },
    "audience": {
      "type": "string",
      "enum": ["user", "dev"],
      "description": "Público alvo principal da página"
    },
    "subsection": {
      "type": "string",
      "enum": ["geoweb", "reurbcad", "admin"],
      "description": "Sub-categorização para seção manuais"
    },
    "draft": {
      "type": "boolean",
      "default": false,
      "description": "Oculta página do build e navegação quando true"
    },
    "sidebar": {
      "type": "object",
      "properties": {
        "label": {
          "type": "string",
          "description": "Texto alternativo no menu lateral"
        },
        "order": {
          "type": "integer",
          "description": "Posição numérica na navegação"
        },
        "badge": {
          "type": "string",
          "description": "Indicador como Novo ou Beta"
        }
      }
    },
    "tableOfContents": {
      "type": ["boolean", "object"],
      "description": "Controla exibição do índice lateral"
    },
    "template": {
      "type": "string",
      "description": "Referência a layout customizado"
    },
    "hero": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "tagline": { "type": "string" },
        "image": { "type": "string" },
        "actions": { "type": "array" }
      },
      "description": "Configuração de banner para landing pages"
    }
  }
}
```

## Campo Source Obrigatório

O campo source é obrigatório e garante que toda página WEBDOCS tenha rastreabilidade para sua documentação fonte. O validador verifica se o arquivo referenciado existe no repositório e se o caminho é compatível com a seção da página conforme mapeamento em SPECS/16-source-alignment.md.

Exemplos válidos de source incluem caminhos para requisitos funcionais como CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/01-auth-security/RF-001-integracao-com-keycloak.md, workflows como CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md, e features de projetos como PROJECTS/GEOWEB/DOCS/FEATURES/01-map-navigation.md.

## Campos de Categorização

Campo section como enum indica seção do portal e determina quais roles podem acessar a página. Campo audience como enum indica público alvo principal. Campo subsection é opcional e usado apenas na seção manuais para categorizar por aplicação (geoweb, reurbcad, admin).

## Campos de Navegação

Campo sidebar como objeto opcional permite customizar aparência no menu com label (texto alternativo), order (posição numérica), e badge (indicador visual). Campo tableOfContents como boolean ou objeto controla exibição e configuração do índice lateral de headings.

## Campos Especiais

Campo draft como boolean oculta página do build e navegação quando true, útil para conteúdo em desenvolvimento. Campo template como string referencia layout customizado para páginas especiais. Campo hero como objeto configura banner destacado para landing pages contendo title, tagline, image, e actions.

Schema extensível permite campos adicionais para casos específicos sem modificar schema base. Campos desconhecidos são preservados no frontmatter mas não validados. Usar com moderação para não fragmentar estrutura.

Arquivo de definição em src/content/config.ts exporta schema usado por Astro Content Collections. Alterações no schema requerem atualização de documentos existentes para conformidade.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
