# Deployment - ADMIN

## Deploy

Deploy para Vercel como static SPA: build command `bun run build` gera `dist/` com HTML + JS bundle via Vite, Vercel serve arquivos estáticos via CDN com caching headers (max-age 1 year para assets, stale-while-revalidate para HTML), routing client-side via React Router com fallback para `index.html` configurado em `vercel.json` `rewrites: [{ source: "/(.*)", destination: "/index.html" }]`, variáveis de ambiente `VITE_API_URL` e `VITE_KEYCLOAK_URL` configuradas em Vercel dashboard, preview deployments em cada PR permitem testar mudanças antes de produção, production deployment em merge para `main` com healthcheck validando que `/` retorna 200 antes de finalizar deploy.

## Vercel Configuration

```json
// vercel.json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

## Build

```bash
# Build SPA
bun run build  # → dist/

# Preview locally
bun run preview  # → http://localhost:4173
```

