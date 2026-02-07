---
type: leaf
status: review
updated: 2026-01-21
---

# Content Schema - Exemplos

Exemplos de frontmatter válido e uso em componentes.

Arquivos relacionados:
- Visão geral: `23-content-schema-overview.md`
- Schema TypeScript: `23-content-schema-typescript.md`

## Exemplos de Frontmatter Válido

### Página de Guia

```yaml
---
title: "Cadastro de Unidades"
description: "Guia completo para cadastro de unidades habitacionais no sistema CARF, incluindo coleta de dados e geolocalização."
source: "CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md"
lastUpdated: 2026-01-20
section: "guia"
audience: "field-coordinator"
draft: false
sidebar:
  order: 2
  label: "Unidades"
  badge: "Atualizado"
---
```

### Página de Manual

```yaml
---
title: "Manual do Agente de Campo"
description: "Manual operacional completo para agentes de campo realizarem coleta de dados em comunidades REURB."
section: "manuais"
audience: "field-coordinator"
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3
sidebar:
  order: 1
prev: false
next:
  link: "/manuais/analista/"
  label: "Manual do Analista"
---
```

### Página de API

```yaml
---
title: "Unidades API"
description: "Documentação da API REST para gerenciamento de unidades habitacionais, incluindo CRUD e operações espaciais."
section: "api"
audience: "dev"
sidebar:
  order: 3
  badge:
    text: "v2"
    variant: "tip"
---
```

### Página Dev (Protegida)

```yaml
---
title: "Middleware de Autenticação"
description: "Documentação técnica do middleware Astro para autenticação via Keycloak e controle de acesso por roles."
section: "dev"
audience: "dev"
requiredRoles:
  - dev
  - super-admin
relatedSpecs:
  - "SPECS/14-auth-endpoints.md"
  - "SPECS/20-keycloak-client-config.md"
changelog:
  - date: 2026-01-20
    version: "1.2.0"
    changes:
      - "Adicionado suporte a refresh token automático"
      - "Corrigido bug de redirect loop"
---
```

### Banner

```yaml
# src/content/banners/manutencao-programada.yaml
id: "manutencao-2026-01"
content: "Manutenção programada dia 25/01 das 02:00 às 06:00. O sistema poderá ficar indisponível."
variant: "caution"
dismissible: true
startDate: 2026-01-20
endDate: 2026-01-26
sections:
  - guia
  - manuais
priority: 80
link:
  href: "https://status.carf.com.br"
  text: "Ver status"
```

## Uso em Componentes

```typescript
// Exemplo: listar docs de uma seção
import { getCollection } from 'astro:content';
import type { DocsSchema } from '../content/config';

// Filtrar por seção
const guiaDocs = await getCollection('docs', ({ data }) => {
  return data.section === 'guia' && !data.draft;
});

// Filtrar por audience
const fieldAgentDocs = await getCollection('docs', ({ data }) => {
  return data.audience === 'field-coordinator' || data.audience === 'field-cadastrator' || data.audience === 'all';
});

// Ordenar por sidebar.order
const sortedDocs = guiaDocs.sort((a, b) => {
  const orderA = a.data.sidebar?.order ?? 999;
  const orderB = b.data.sidebar?.order ?? 999;
  return orderA - orderB;
});
```

```typescript
// Exemplo: banners ativos
import { getCollection } from 'astro:content';

const now = new Date();

const activeBanners = await getCollection('banners', ({ data }) => {
  const afterStart = !data.startDate || data.startDate <= now;
  const beforeEnd = !data.endDate || data.endDate >= now;
  return afterStart && beforeEnd;
});

// Ordenar por prioridade
const sortedBanners = activeBanners.sort((a, b) =>
  b.data.priority - a.data.priority
);
```

## Script de Validação de Frontmatter

```typescript
// scripts/validate-frontmatter.ts
import { glob } from 'glob';
import matter from 'gray-matter';
import { z } from 'zod';

const docsSchema = z.object({
  title: z.string().min(3).max(100),
  description: z.string().min(50).max(160),
  // ... resto do schema
});

async function validateAll() {
  const files = await glob('src/content/docs/**/*.mdx');
  const errors: Array<{ file: string; issues: z.ZodIssue[] }> = [];

  for (const file of files) {
    const content = await Bun.file(file).text();
    const { data } = matter(content);

    const result = docsSchema.safeParse(data);
    if (!result.success) {
      errors.push({ file, issues: result.error.issues });
    }
  }

  if (errors.length > 0) {
    console.error('Frontmatter validation errors:');
    for (const { file, issues } of errors) {
      console.error(`\n${file}:`);
      for (const issue of issues) {
        console.error(`  - ${issue.path.join('.')}: ${issue.message}`);
      }
    }
    process.exit(1);
  }

  console.log('All frontmatter valid!');
}

validateAll();
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
