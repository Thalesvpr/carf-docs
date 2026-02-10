---
type: leaf
status: review
updated: 2026-02-07
---

# Content Schema - Visao Geral

Schema Zod para validacao de frontmatter em Astro Content Collections. Arquivos relacionados: 23-content-schema-typescript.md e 23-content-schema-examples.md.

## Visao Geral

Arquivo de definicao em src/content/config.ts. Tres collections definidas: docs para documentacao principal (guia, manuais, api, status), dev para documentacao tecnica protegida, e banners para notificacoes e avisos. Validacao usa Zod schemas com types exportados, integrado com Astro Content Collections API.

## Validacoes Customizadas

| Campo | Min | Max | Motivo |
|-------|-----|-----|--------|
| title | 3 | 100 | Balanceamento entre clareza e display em sidebar |
| description | 50 | 160 | SEO: meta description ideal entre 50-160 caracteres |
| source | - | - | Pattern CENTRAL/path/file.md para rastreabilidade |
| banner id | - | - | Pattern lowercase com hifens para localStorage dismiss state |

## Estrutura de Pastas

| Pasta | Conteudo |
|-------|----------|
| src/content/docs/guia/ | Paginas da secao /guia/ |
| src/content/docs/manuais/ | Paginas da secao /manuais/ |
| src/content/docs/api/ | Paginas da secao /api/ |
| src/content/docs/status/ | Pagina de status |
| src/content/dev/ | Paginas protegidas da secao /dev/ |
| src/content/banners/ | Arquivos YAML de banners |

## Erros Comuns de Validacao

| Erro | Mensagem | Correcao |
|------|----------|----------|
| description_too_short | Descricao deve ter pelo menos 50 caracteres para SEO | Expandir descricao com mais detalhes relevantes |
| invalid_source_path | Source deve seguir padrao CENTRAL/PATH/file.md | Verificar caminho exato no repositorio CENTRAL |
| invalid_section | Expected guia, manuais, api, status ou dev | Usar uma das secoes validas |
| sidebar_order_negative | Number must be greater than or equal to 0 | Usar numero inteiro >= 0 para ordem |
