# Build and Run - ADMIN

## Build

Build usa `bun run build` gerando `dist/` otimizado com HTML + JS bundle via Vite, validar build localmente com `bun run preview` servindo production mode em `http://localhost:4173`, rodar linters com `bun run lint` e type check com `bun run type-check`, deploy para Vercel push to `main` branch acionando deploy automático ou manual com `vercel --prod`, configurar variáveis de ambiente secrets no Vercel dashboard antes do primeiro deploy (VITE_API_URL, VITE_KEYCLOAK_URL).

## Comandos

```bash
# Build
bun run build  # → dist/

# Preview
bun run preview  # → http://localhost:4173

# Lint
bun run lint

# Type check
bun run type-check

# Deploy
vercel --prod
```

## Referências

- [Vite Build](https://vitejs.dev/guide/build.html)
- [Vercel Deployment](https://vercel.com/docs)
