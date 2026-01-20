---
status: review
updated: 2026-01-17
---

# Frontmatter Schema

Schema Zod define campos obrigatórios e opcionais do frontmatter para todos documentos do WEBDOCS. Validação acontece em build time garantindo consistência.

Campos obrigatórios incluem title como string não vazia exibida no browser tab, sidebar e breadcrumbs, description como string de 50-160 caracteres para SEO e previews em buscas, e lastUpdated como data ISO indicando última modificação significativa.

Campos de categorização incluem section como enum (guia, sistema, manuais, api, dev, status, changelog) indicando seção do portal, audience como enum (user, dev) indicando público alvo e controlando acesso, e subsection como string opcional para sub-categorização em manuais (geoweb, reurbcad, admin).

Campos de navegação incluem sidebar como objeto opcional com label (texto alternativo no menu), order (posição numérica), e badge (indicador como "Novo" ou "Beta"). Campo tableOfContents como boolean ou objeto controla exibição e configuração do índice lateral.

Campos especiais incluem draft como boolean ocultando página do build e navegação quando true, template como string referenciando layout customizado, e hero como objeto para páginas com banner destacado contendo title, tagline, image, e actions.

Schema extensível permite campos adicionais para casos específicos sem modificar schema base. Campos desconhecidos são preservados no frontmatter mas não validados. Usar com moderação para não fragmentar estrutura.

Arquivo de definição em src/content/config.ts exporta schema usado por Astro Content Collections. Alterações no schema requerem atualização de documentos existentes para conformidade.
