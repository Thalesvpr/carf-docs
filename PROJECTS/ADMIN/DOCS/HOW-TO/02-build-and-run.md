---
type: leaf
status: review
updated: 2026-02-07
---

# Build and Run - ADMIN

## Build

O build utiliza bun para gerar o diretorio dist/ otimizado contendo HTML e JS bundle via Vite. Para validar o build localmente, executar o comando de preview via bun que serve o modo producao em localhost na porta 4173. Antes do build, executar o linter via bun para verificar padroes de codigo e o type-check via bun para validar tipagem TypeScript. O deploy para Vercel acontece automaticamente ao fazer push para a branch main, acionando o deploy automatico, ou pode ser feito manualmente via CLI da Vercel com flag de producao. As variaveis de ambiente secrets devem ser configuradas no Vercel dashboard antes do primeiro deploy, incluindo VITE_API_URL e VITE_KEYCLOAK_URL.

## Etapas do Build

| Etapa | Comando | Resultado |
|-------|---------|-----------|
| Build producao | bun run build | Gera dist/ otimizado |
| Preview local | bun run preview | Serve em localhost:4173 |
| Linter | bun run lint | Verifica padroes de codigo |
| Type check | bun run type-check | Valida tipagem TypeScript |
| Deploy producao | Push para main ou vercel --prod | Deploy na Vercel |

## Referencias

Documentacao do Vite sobre build em vitejs.dev/guide/build.html e documentacao da Vercel sobre deployment em vercel.com/docs contem informacoes detalhadas sobre configuracoes avancadas de build e deploy.
