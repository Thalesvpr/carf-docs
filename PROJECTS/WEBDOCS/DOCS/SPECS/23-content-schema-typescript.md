---
type: leaf
status: review
updated: 2026-02-07
---

# Content Schema - TypeScript

Schema Zod completo para src/content/config.ts. Relacionado com 23-content-schema-overview.md e 23-content-schema-examples.md.

## Enums

Tres enums definidos: sectionEnum com valores guia, manuais, api, status e dev. AudienceEnum com user, field-cadastrator, field-coordinator, analyst, admin, super-admin, dev e all. BadgeVariantEnum com note, tip, caution, danger, success e default.

## Schema Docs

Campos obrigatorios: title (string 3-100 chars) e description (string 50-160 chars para SEO). Campos opcionais: source com pattern CENTRAL/path/file.md, lastUpdated como date, section default guia, audience default all, draft default false, sidebar com order/label/badge/hidden, tableOfContents, template (doc ou splash), hero com title/tagline/image/actions, banner com content, prev/next e head para tags extras.

## Schema DevDocs

Estende docsSchema. Section fixo em dev. RequiredRoles array de admin/super-admin/dev default dev. RelatedSpecs array de strings. Changelog array com date, version e changes.

## Schema Banners

Id obrigatorio com pattern lowercase-hifens. Content 10-200 chars. Variant default note. Dismissible default true. StartDate e endDate opcionais. Sections array opcional. Link com href e text. Priority 0-100 default 50.

## Collections

Tres collections exportadas: docs com type content usando docsSchema, dev com type content usando devDocsSchema, banners com type data usando bannersSchema. Types exportados: DocsSchema, DevDocsSchema, BannerSchema, Section, Audience.
