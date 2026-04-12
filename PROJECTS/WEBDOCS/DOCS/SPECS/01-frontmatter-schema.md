---
type: leaf
status: review
updated: 2026-02-07
---

# Frontmatter Schema

Schema Zod define campos obrigatorios e opcionais do frontmatter WEBDOCS. Validacao em build time garante consistencia e rastreabilidade com documentacao fonte.

## Campos Obrigatorios

| Campo | Tipo | Restricao | Descricao |
|-------|------|-----------|-----------|
| title | string | minLength 1 | Titulo no browser tab, sidebar e breadcrumbs |
| description | string | 50-160 chars | Descricao para SEO e previews |
| source | string | CENTRAL/ ou PROJECTS/ .md | Caminho para arquivo fonte |

## Categorizacao

| Campo | Tipo | Valores |
|-------|------|---------|
| section | enum | guia, sistema, manuais, api, dev, status, changelog |
| audience | enum | user, dev |
| subsection | enum | reurbweb, reurbcad, admin |
| lastUpdated | date | formato ISO |

## Navegacao

| Campo | Tipo | Descricao |
|-------|------|-----------|
| sidebar.label | string | Texto alternativo no menu |
| sidebar.order | integer | Posicao na navegacao |
| sidebar.badge | string | Indicador Novo ou Beta |
| tableOfContents | boolean/object | Indice lateral de headings |

## Especiais

| Campo | Tipo | Descricao |
|-------|------|-----------|
| draft | boolean | Oculta do build quando true, default false |
| template | string | Layout customizado |
| hero | object | Banner com title, tagline, image, actions |

## Rastreabilidade

Source obrigatorio garante rastreabilidade para documentacao fonte. Validador verifica existencia do arquivo e compatibilidade com secao conforme SPECS/16-source-alignment.md. Schema extensivel permite campos adicionais. Definicao em src/content/config.ts exporta schema para Astro Content Collections.
