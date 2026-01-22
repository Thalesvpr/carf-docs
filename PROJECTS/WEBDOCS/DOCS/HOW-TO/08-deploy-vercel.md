---
type: leaf
status: review
updated: 2026-01-21
---

# Deploy para Vercel

Guia para configurar e executar deploy do WEBDOCS na plataforma Vercel.

Conectar repositório GitHub ao Vercel via dashboard. Criar novo projeto selecionando repositório do WEBDOCS. Vercel detecta automaticamente framework Astro e configura build settings padrão.

Configurar settings de build em project settings ou vercel.json. Framework preset Astro, build command bun run build, output directory dist, e install command bun install. Root directory apontando para SRC-CODE/carf-webdocs se repositório é monorepo.

Configurar variáveis de ambiente no dashboard Vercel em Settings > Environment Variables. Adicionar todas variáveis de .env.example com valores de produção. Marcar variáveis sensíveis como sensitive para ocultar valores em logs.

Configurar domínio customizado em Settings > Domains. Adicionar domínio e configurar DNS conforme instruções do Vercel. Certificado SSL provisionado automaticamente via Let's Encrypt.

Deploy automático acontece em push para branch main. Vercel detecta push via webhook, executa build, e deploya para produção se bem-sucedido. Rollback automático se health check falhar após deploy.

Preview deployments criados automaticamente para pull requests. URL única por PR permite review de mudanças. Comments automáticos no PR linkam para preview. Útil para validar mudanças de conteúdo e código antes de merge.

Monitorar deploys no dashboard Vercel em Deployments. Logs de build disponíveis para debug de falhas. Analytics mostram métricas de performance e uso. Alertas configuráveis para falhas de deploy ou degradação de performance.

## vercel.json Completo

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "astro",
  "buildCommand": "bun run build",
  "installCommand": "bun install",
  "outputDirectory": "dist",
  "regions": ["gru1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store, must-revalidate" }
      ]
    },
    {
      "source": "/_astro/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/health", "destination": "/api/health" }
  ],
  "redirects": [
    { "source": "/docs", "destination": "/guia/", "permanent": true },
    { "source": "/swagger", "destination": "/dev/api/swagger/", "permanent": true }
  ],
  "functions": {
    "src/pages/api/**/*.ts": {
      "maxDuration": 30
    },
    "src/pages/status.astro": {
      "maxDuration": 60
    }
  },
  "crons": []
}
```

## Variáveis de Ambiente no Vercel

```json
{
  "environment_variables": {
    "production": {
      "PUBLIC_APP_URL": "https://docs.carf.com.br",
      "KEYCLOAK_URL": "https://auth.carf.com.br",
      "KEYCLOAK_REALM": "carf",
      "KEYCLOAK_CLIENT_ID": "webdocs",
      "GEOAPI_URL": "https://api.carf.com.br",
      "GEOAPI_SWAGGER_URL": "https://api.carf.com.br/swagger/v1/swagger.json"
    },
    "preview": {
      "PUBLIC_APP_URL": "https://preview-webdocs.vercel.app",
      "KEYCLOAK_URL": "https://auth-staging.carf.com.br",
      "KEYCLOAK_REALM": "carf-staging",
      "KEYCLOAK_CLIENT_ID": "webdocs-preview",
      "GEOAPI_URL": "https://api-staging.carf.com.br",
      "GEOAPI_SWAGGER_URL": "https://api-staging.carf.com.br/swagger/v1/swagger.json"
    }
  }
}
```

## Configurar no Dashboard Vercel

1. Acesse **Settings > Environment Variables**
2. Para cada variável, defina valores para:
   - **Production**: ambiente de produção (branch main)
   - **Preview**: ambientes de PR e branches
   - **Development**: não usado (dev local usa .env)

## Rollback Manual

```bash
# Via Vercel CLI
vercel rollback <deployment-url>

# Exemplo
vercel rollback webdocs-abc123.vercel.app
```

Ou via Dashboard:
1. Acesse **Deployments**
2. Encontre deploy anterior funcionando
3. Clique nos três pontos **...**
4. Selecione **Promote to Production**

## Preview Deployments

Cada PR recebe URL única no formato:
```
https://webdocs-git-<branch-name>-carf.vercel.app
```

Configurar proteção de preview (opcional):
```json
{
  "vercel.json": {
    "passwordProtection": {
      "deploymentType": "preview"
    }
  }
}
```

## Health Check Endpoint

```typescript
// src/pages/api/health.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  return new Response(JSON.stringify({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: import.meta.env.VERCEL_GIT_COMMIT_SHA || 'local'
  }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

## Checklist de Deploy

```json
{
  "checklist": [
    "[ ] Repositório conectado ao Vercel",
    "[ ] vercel.json na raiz do projeto",
    "[ ] Variáveis de ambiente configuradas (prod e preview)",
    "[ ] Domínio customizado configurado",
    "[ ] DNS apontando para Vercel",
    "[ ] SSL certificado ativo",
    "[ ] Health check funcionando",
    "[ ] Preview deployment testado"
  ]
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
