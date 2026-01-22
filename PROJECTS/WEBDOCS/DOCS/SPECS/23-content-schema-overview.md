---
type: leaf
status: review
updated: 2026-01-21
---

# Content Schema - Visão Geral

Schema Zod para validação de frontmatter em Astro Content Collections.

Arquivos relacionados:
- Schema TypeScript: `23-content-schema-typescript.md`
- Exemplos: `23-content-schema-examples.md`

## Visão Geral

```json
{
  "file": "src/content/config.ts",
  "collections": {
    "docs": "Documentação principal (guia, manuais, api, status)",
    "dev": "Documentação técnica protegida",
    "banners": "Notificações e avisos"
  },
  "validation": "Zod schemas com types exportados",
  "integration": "Astro Content Collections API"
}
```

## Validações Customizadas

```json
{
  "validations": {
    "title": {
      "min": 3,
      "max": 100,
      "reason": "Balanceamento entre clareza e display em sidebar"
    },
    "description": {
      "min": 50,
      "max": 160,
      "reason": "SEO: meta description ideal entre 50-160 chars"
    },
    "source": {
      "pattern": "^CENTRAL\\/[\\w\\-\\/]+\\.md$",
      "example": "CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md",
      "reason": "Rastreabilidade para documento fonte"
    },
    "banner_id": {
      "pattern": "^[a-z0-9-]+$",
      "reason": "Usado em localStorage para dismiss state"
    }
  }
}
```

## Estrutura de Pastas

```json
{
  "content_structure": {
    "src/content/": {
      "docs/": {
        "guia/": "Páginas da seção /guia/",
        "manuais/": "Páginas da seção /manuais/",
        "api/": "Páginas da seção /api/",
        "status/": "Página de status"
      },
      "dev/": "Páginas protegidas da seção /dev/",
      "banners/": "Arquivos YAML de banners"
    }
  }
}
```

## Erros de Validação

```json
{
  "common_errors": {
    "description_too_short": {
      "error": "Descrição deve ter pelo menos 50 caracteres para SEO",
      "fix": "Expandir descrição com mais detalhes relevantes"
    },
    "invalid_source_path": {
      "error": "Source deve seguir padrão CENTRAL/PATH/file.md",
      "fix": "Verificar caminho exato no repositório CENTRAL"
    },
    "invalid_section": {
      "error": "Expected 'guia' | 'manuais' | 'api' | 'status' | 'dev'",
      "fix": "Usar uma das seções válidas"
    },
    "sidebar_order_negative": {
      "error": "Number must be greater than or equal to 0",
      "fix": "Usar número inteiro >= 0 para ordem"
    }
  }
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
