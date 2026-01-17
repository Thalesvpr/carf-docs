# GEOWEB Dockerfile

Multi-stage Dockerfile para build e deploy do frontend React/Next.js.

## Dockerfile

```dockerfile
# Dockerfile.geoweb

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Install dependencies based on lockfile
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS build
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build arguments for environment
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_KEYCLOAK_URL
ARG NEXT_PUBLIC_MAP_TILE_URL

ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_KEYCLOAK_URL=$NEXT_PUBLIC_KEYCLOAK_URL
ENV NEXT_PUBLIC_MAP_TILE_URL=$NEXT_PUBLIC_MAP_TILE_URL

RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine AS runtime
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built app
COPY --from=build /app/public ./public
COPY --from=build --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=build --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

## Otimizações

- **Output standalone**: Next.js gera servidor Node mínimo
- **Imagem Alpine**: ~150MB vs ~1GB com node:20
- **Static export**: Assets estáticos servidos separadamente via CDN
- **Non-root user**: Segurança em runtime

## Build

```bash
# Build com variáveis de ambiente
docker build -f Dockerfile.geoweb \
  --build-arg NEXT_PUBLIC_API_URL=https://api.carf.com.br \
  --build-arg NEXT_PUBLIC_KEYCLOAK_URL=https://keycloak.carf.com.br \
  -t carf/geoweb:latest .

# Build para staging
docker build -f Dockerfile.geoweb \
  --build-arg NEXT_PUBLIC_API_URL=https://api-staging.carf.com.br \
  -t carf/geoweb:staging .
```

## Notas

- Variáveis NEXT_PUBLIC_* são injetadas em build time
- Runtime não requer variáveis de ambiente (baked in)
- Para configuração dinâmica, usar runtime config

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
