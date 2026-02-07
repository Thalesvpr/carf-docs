---
type: leaf
status: review
updated: 2026-01-21
---

# Content Schema - TypeScript

Schema Zod completo para `src/content/config.ts`.

Arquivos relacionados:
- Visão geral: `23-content-schema-overview.md`
- Exemplos: `23-content-schema-examples.md`

## Schema Completo

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

// Enums reutilizáveis
const sectionEnum = z.enum([
  'guia',
  'manuais',
  'api',
  'status',
  'dev'
]);

const audienceEnum = z.enum([
  'user',
  'field-cadastrator',
  'field-coordinator',
  'analyst',
  'admin',
  'super-admin',
  'dev',
  'all'
]);

const badgeVariantEnum = z.enum([
  'note',
  'tip',
  'caution',
  'danger',
  'success',
  'default'
]);

// Schema de sidebar (opcional)
const sidebarSchema = z.object({
  order: z.number().int().min(0).optional(),
  label: z.string().max(50).optional(),
  badge: z.union([
    z.string(),
    z.object({
      text: z.string(),
      variant: badgeVariantEnum.optional()
    })
  ]).optional(),
  hidden: z.boolean().optional()
}).optional();

// Schema principal para docs
const docsSchema = z.object({
  // Campos obrigatórios
  title: z.string()
    .min(3, 'Título deve ter pelo menos 3 caracteres')
    .max(100, 'Título deve ter no máximo 100 caracteres'),

  description: z.string()
    .min(50, 'Descrição deve ter pelo menos 50 caracteres para SEO')
    .max(160, 'Descrição deve ter no máximo 160 caracteres para SEO'),

  // Campos opcionais com defaults
  source: z.string()
    .regex(
      /^CENTRAL\/[\w\-\/]+\.md$/,
      'Source deve seguir padrão CENTRAL/PATH/file.md'
    )
    .optional(),

  lastUpdated: z.coerce.date().optional(),

  section: sectionEnum.default('guia'),

  audience: audienceEnum.default('all'),

  draft: z.boolean().default(false),

  // Sidebar configuration
  sidebar: sidebarSchema,

  // Starlight específicos
  tableOfContents: z.union([
    z.boolean(),
    z.object({
      minHeadingLevel: z.number().min(1).max(6).optional(),
      maxHeadingLevel: z.number().min(1).max(6).optional()
    })
  ]).optional(),

  template: z.enum(['doc', 'splash']).optional(),

  hero: z.object({
    title: z.string().optional(),
    tagline: z.string().optional(),
    image: z.object({
      file: z.string(),
      alt: z.string()
    }).optional(),
    actions: z.array(z.object({
      text: z.string(),
      link: z.string(),
      icon: z.string().optional(),
      variant: z.enum(['primary', 'secondary', 'minimal']).optional()
    })).optional()
  }).optional(),

  // Banner de página específica
  banner: z.object({
    content: z.string()
  }).optional(),

  // Paginação
  prev: z.union([
    z.boolean(),
    z.string(),
    z.object({
      link: z.string(),
      label: z.string()
    })
  ]).optional(),

  next: z.union([
    z.boolean(),
    z.string(),
    z.object({
      link: z.string(),
      label: z.string()
    })
  ]).optional(),

  // SEO
  head: z.array(z.object({
    tag: z.string(),
    attrs: z.record(z.string()).optional(),
    content: z.string().optional()
  })).optional()
});

// Schema para seção dev (campos adicionais)
const devDocsSchema = docsSchema.extend({
  section: z.literal('dev').default('dev'),

  // Campos específicos de dev
  requiredRoles: z.array(z.enum([
    'admin',
    'super-admin',
    'dev'
  ])).default(['dev']),

  // Referência para specs
  relatedSpecs: z.array(z.string()).optional(),

  // Changelog
  changelog: z.array(z.object({
    date: z.coerce.date(),
    version: z.string().optional(),
    changes: z.array(z.string())
  })).optional()
});

// Schema para banners
const bannersSchema = z.object({
  id: z.string()
    .regex(/^[a-z0-9-]+$/, 'ID deve ser lowercase com hífens'),

  content: z.string()
    .min(10, 'Conteúdo do banner deve ter pelo menos 10 caracteres')
    .max(200, 'Conteúdo do banner deve ter no máximo 200 caracteres'),

  variant: z.enum([
    'note',
    'tip',
    'caution',
    'danger',
    'success'
  ]).default('note'),

  dismissible: z.boolean().default(true),

  // Controle de exibição
  startDate: z.coerce.date().optional(),
  endDate: z.coerce.date().optional(),

  // Seções onde exibir (vazio = todas)
  sections: z.array(sectionEnum).optional(),

  // Link opcional
  link: z.object({
    href: z.string().url(),
    text: z.string()
  }).optional(),

  // Prioridade (maior = mais importante)
  priority: z.number().int().min(0).max(100).default(50)
});

// Definição das collections
export const collections = {
  docs: defineCollection({
    type: 'content',
    schema: docsSchema
  }),

  dev: defineCollection({
    type: 'content',
    schema: devDocsSchema
  }),

  banners: defineCollection({
    type: 'data',
    schema: bannersSchema
  })
};

// Types exportados para uso em componentes
export type DocsSchema = z.infer<typeof docsSchema>;
export type DevDocsSchema = z.infer<typeof devDocsSchema>;
export type BannerSchema = z.infer<typeof bannersSchema>;
export type Section = z.infer<typeof sectionEnum>;
export type Audience = z.infer<typeof audienceEnum>;
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
