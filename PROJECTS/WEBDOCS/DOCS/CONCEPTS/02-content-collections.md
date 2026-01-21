---
status: review
updated: 2026-01-21
---

# Content Collections

Content Collections são sistema nativo do Astro para gerenciar conteúdo estruturado com validação de schema. Arquivos Markdown ou MDX em src/content/ são automaticamente parseados, validados contra schema Zod, e disponibilizados via API type-safe.

Configuração em src/content/config.ts define collections com schema Zod especificando campos obrigatórios e opcionais do frontmatter. Schema garante que todos documentos tenham metadados consistentes como title, description, lastUpdated, e campos customizados como section ou audience.

Starlight estende Content Collections adicionando collection docs com schema próprio incluindo campos como sidebar com label e order, tableOfContents com minHeadingLevel e maxHeadingLevel, e hero para páginas com banner destacado. Schema é extensível via extend() permitindo adicionar campos customizados.

Queries usam funções getCollection() e getEntry() retornando objetos tipados com data (frontmatter validado), body (conteúdo Markdown), e slug (identificador único). Erros de validação são reportados no build time prevenindo documentos malformados de serem publicados.

Frontmatter schema do WEBDOCS inclui campos title (obrigatório), description (obrigatório para SEO), lastUpdated (data automática), audience (user ou dev), e section (guia, sistema, manuais, api, dev).
