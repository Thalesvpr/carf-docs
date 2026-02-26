---
type: leaf
status: review
updated: 2026-02-07
---

# Decap CMS - Collections

Collections do Decap CMS para WEBDOCS. Relacionado com 15-decap-cms-overview.md e 15-decap-cms-arquivos.md.

## Campos Base de Conteudo

Compartilhados entre guia e manuais:

| Campo | Widget | Obrigatorio | Validacao |
|-------|--------|-------------|-----------|
| title | string | sim | 3-100 chars |
| description | string | sim | 50-160 chars |
| source | string | sim | CENTRAL/ ou PROJECTS/ .md |
| sidebar.order | number | nao | - |
| sidebar.label | string | nao | - |
| draft | boolean | nao | default false |
| body | markdown | sim | - |

## Collections de Conteudo

Collection guia em src/content/docs/guia, extensao mdx. Filtro de rascunhos, sortavel por title e sidebar.order. Tres collections de manuais com mesma estrutura: manuais-reurbweb, manuais-reurbcad e manuais-admin em respectivas subpastas de src/content/docs/manuais/.

## Incidentes

Collection incidents em src/content/incidents, extensao md, slug ano-mes-dia-slug. Campos: title, date (datetime), status (investigating/identified/monitoring/resolved), services (select multiplo geoapi/keycloak/minio/postgres), severity (minor/major/critical), body.

## Banners

Collection banners em src/content/banners, extensao e formato yaml. Campos: id (lowercase-hifens), content (10-200 chars), variant (note/tip/caution/danger/success default note), dismissible (default true), startDate, endDate, priority (0-100 default 50).
