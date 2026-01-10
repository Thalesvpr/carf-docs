# Deployment - WEBDOCS

## Deploy para Vercel

Deployment usa Vercel com GitHub integration fazendo preview deploy automático em cada PR e production deploy em merge para `main`, build command é `bun run build` gerando `dist/` com HTML estático, variáveis de ambiente incluem `PUBLIC_SITE_URL` para canonical URLs e `ENABLE_SEARCH` para ativar Pagefind indexing, Vercel configura caching headers automático para assets (images, CSS, JS) com max-age 1 year e HTML com stale-while-revalidate, redirects e rewrites definidos em `vercel.json` ou `astro.config.mjs`, custom domain configurado em Vercel dashboard apontando DNS para `cname.vercel-dns.com`, e CI/CD via GitHub Actions roda lint checks e link validation antes de permitir deploy.

## Vercel Configuration

```json
// vercel.json
{
  "buildCommand": "bun run build",
  "outputDirectory": "dist",
  "framework": "astro",
  "headers": [
    {
      "source": "/_astro/:path*",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/:path*",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ]
}
```

## Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1

      - run: bun install
      - run: bun run build
      - run: bun run check-links

      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: ${{ github.ref == 'refs/heads/main' && '--prod' || '' }}
```

## Custom Domain

```bash
# 1. Adicionar domínio no Vercel
vercel domains add docs.carf.gov.br

# 2. Configurar DNS
# Tipo: CNAME
# Nome: docs
# Valor: cname.vercel-dns.com

# 3. Verificar
dig docs.carf.gov.br
# → deve retornar cname.vercel-dns.com
```

