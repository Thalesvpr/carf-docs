# Build and Run - WEBDOCS

## Build

Build usa `bun run build` gerando site estático em `dist/` com HTML, CSS, JS, images otimizados, preview production build localmente com `bun run preview` servindo `dist/` em `http://localhost:4321`, validar build com `bun run check` verificando links quebrados e acessibilidade, e deploy para Vercel push to `main` branch acionando deploy automático ou deploy manual com `vercel --prod` usando Vercel CLI, site fica disponível em `https://docs.carf.gov.br` após configurar custom domain no Vercel dashboard.

## Comandos

```bash
# Build
bun run build  # Gera dist/

# Preview local
bun run preview  # Serve dist/ em http://localhost:4321

# Validar
bun run check  # Check links, accessibility

# Deploy manual
vercel --prod
```

## Output Structure

```
dist/
├── index.html
├── domain-model/
│   └── index.html
├── _astro/
│   ├── [hash].css
│   └── [hash].js
└── pagefind/
    ├── pagefind.js
    └── index.json
```

## Referências

- [Astro Build](https://docs.astro.build/en/reference/cli-reference/#astro-build)
- [Vercel Deployment](https://vercel.com/docs/deployments/overview)

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
