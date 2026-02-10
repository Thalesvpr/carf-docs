---
type: leaf
status: review
updated: 2026-02-07
---

# Content Schema - Exemplos

Exemplos de frontmatter valido e uso em componentes. Relacionado com 23-content-schema-overview.md e 23-content-schema-typescript.md.

## Pagina de Guia

Title "Cadastro de Unidades", description 50-160 chars sobre cadastro de unidades habitacionais. Source CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md. Section guia, audience field-coordinator, draft false, sidebar order 2 label Unidades badge Atualizado.

## Pagina de Manual

Title "Manual do Agente de Campo", description sobre manual operacional. Section manuais, audience field-coordinator. TableOfContents min 2 max 3, sidebar order 1. Prev false, next com link /manuais/analista/ label Manual do Analista.

## Pagina de API

Title "Unidades API", description sobre API REST. Section api, audience dev, sidebar order 3 com badge text v2 variant tip.

## Pagina Dev Protegida

Title "Middleware de Autenticacao", section dev, audience dev. RequiredRoles dev e super-admin. RelatedSpecs referenciando SPECS/14a e SPECS/20. Changelog com data, versao e lista de mudancas.

## Banner

ID manutencao-2026-01, content sobre manutencao, variant caution, dismissible, startDate/endDate definidos, sections guia e manuais, priority 80, link para status.carf.com.br.

## Uso em Componentes

Listar docs: getCollection filtrar por section e nao draft, ordenar por sidebar.order. Banners ativos: filtrar por startDate/endDate, ordenar por prioridade. Script validate-frontmatter.ts usa glob, gray-matter e Zod para validar todos mdx com exit 1 em erros.
