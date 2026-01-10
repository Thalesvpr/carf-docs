# Troubleshooting - WEBDOCS

## Problemas Comuns

**(1) Markdown not rendering** - validar frontmatter YAML está correto, verificar que arquivo está em `src/content/docs/` e não em pasta incorreta, **(2) Components not working** - garantir que componente React tem `client:load` directive se precisa interatividade, **(3) Search not working** - rodar `bun run build` para gerar índice Pagefind antes de testar search, **(4) Styles not applying** - verificar que Tailwind config inclui Astro files no `content` array, **(5) Build failing** - checar logs de erro, comum ser path inválido em link ou image reference, **(6) Links quebrados após deploy** - confirmar que base URL está correto em `astro.config.mjs`.

## Soluções

### Frontmatter Inválido

```yaml
# ❌ ERRADO
---
title: Docs  # Falta quotes
description  # Falta ':'
---

# ✅ CORRETO
---
title: 'Docs'
description: 'Documentation site'
---
```

### Component Não Hidrata

```astro
<!-- ❌ ERRADO - sem client directive -->
<SearchBox />

<!-- ✅ CORRETO - com directive -->
<SearchBox client:load />
```

### Build Fail - Link Quebrado

```bash
# Erro: [ERROR] Link to /invalid-path not found

# Solução: Corrigir link para path válido relativo
# Use paths relativos como ./overview.md ao invés de absolutos
```

