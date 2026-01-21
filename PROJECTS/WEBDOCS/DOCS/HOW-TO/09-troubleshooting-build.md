---
status: review
updated: 2026-01-21
---

# Troubleshooting - Build

Resolução de problemas de build e Decap CMS.

Arquivos relacionados:
- Problemas de auth: `09-troubleshooting-auth.md`
- Problemas de runtime: `09-troubleshooting-runtime.md`

## Build Falha com Erro de Frontmatter

**Sintoma:** Astro build falha com erro de validação.

```json
{
  "problem": "frontmatter_validation_error",
  "error_example": "ZodError: description must be at least 50 characters"
}
```

**Solução:**

```bash
# Identificar arquivo com problema
bun run astro check

# Verificar frontmatter do arquivo indicado
# Corrigir conforme SPECS/23-content-schema-overview.md
```

## Build Falha com Import Error

**Sintoma:** `Cannot find module` ou `Failed to resolve import`.

```json
{
  "problem": "import_error",
  "common_causes": {
    "missing_dependency": "bun install",
    "wrong_path": "Verificar caminho relativo vs absoluto",
    "alias_not_configured": "Verificar tsconfig.json paths"
  }
}
```

**tsconfig.json paths:**

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@lib/*": ["src/lib/*"]
    }
  }
}
```

## Out of Memory Durante Build

**Sintoma:** Build falha com `JavaScript heap out of memory`.

```json
{
  "problem": "oom_build",
  "solutions": [
    {
      "description": "Aumentar memória do Node",
      "command": "NODE_OPTIONS='--max-old-space-size=4096' bun run build"
    },
    {
      "description": "Verificar imports circulares",
      "tool": "madge --circular src/"
    },
    {
      "description": "Lazy load componentes pesados",
      "pattern": "const Heavy = lazy(() => import('./Heavy'))"
    }
  ]
}
```

## Problemas do Decap CMS

### CMS Não Carrega

**Sintoma:** Página /admin mostra tela branca ou erro.

```json
{
  "problem": "cms_blank_page",
  "debug_steps": [
    "1. Verificar console do browser por erros",
    "2. Verificar se /admin/config.yml existe",
    "3. Verificar YAML syntax válida",
    "4. Verificar backend configurado corretamente"
  ]
}
```

**config.yml mínimo funcional:**

```yaml
backend:
  name: github
  repo: owner/repo
  branch: main
  base_url: https://docs.carf.com.br
  auth_endpoint: /api/auth

media_folder: public/images
public_folder: /images

collections:
  - name: docs
    label: Documentos
    folder: src/content/docs
    create: true
    extension: mdx
    fields:
      - { name: title, label: Título, widget: string }
```

### CMS Auth Failed

**Sintoma:** Erro ao autenticar no GitHub via CMS.

```json
{
  "problem": "cms_auth_failed",
  "causes": {
    "github_oauth_not_configured": {
      "check": "GitHub > Settings > Developer settings > OAuth Apps",
      "ensure": "Authorization callback URL = https://docs.carf.com.br/api/auth/callback"
    },
    "env_vars_missing": {
      "check": "GITHUB_CLIENT_ID e GITHUB_CLIENT_SECRET configurados",
      "location": ".env.local ou Vercel Environment Variables"
    }
  }
}
```

### CMS Preview Não Funciona

**Sintoma:** Preview mostra conteúdo errado ou não atualiza.

```json
{
  "problem": "cms_preview_broken",
  "solutions": [
    "Verificar registerPreviewTemplate está chamado",
    "Verificar componente de preview importa estilos",
    "Hard refresh do CMS (Ctrl+Shift+R)"
  ]
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
