---
status: review
updated: 2026-01-17
---

# Build e Deploy

Pipeline de CI/CD usa GitHub Actions para validação e Vercel para hosting com deploy automático em push para main e preview deployments em pull requests.

Build local executa bun run build que processa Content Collections validando schemas Zod, compila arquivos MDX para HTML, aplica syntax highlighting via Shiki, gera sidebar e table of contents via Starlight, bundla assets via Vite, e indexa conteúdo para busca via Pagefind. Output em dist/ pronto para deploy.

GitHub Actions workflow em .github/workflows/ci.yml executa em push e PRs. Jobs paralelos rodam lint (ESLint, Prettier), type check (tsc, astro check), build, testes e2e (Playwright com axe-core), e Lighthouse CI. Falha em qualquer job bloqueia merge.

Vercel conectado ao repositório GitHub detecta pushes e dispara builds automaticamente. Configuração em vercel.json define framework Astro, build command, output directory, e variáveis de ambiente de produção. Funções serverless configuradas para páginas SSR.

Preview deployments são criados automaticamente para cada PR permitindo review de mudanças antes de merge. URL única por PR no formato webdocs-git-branch-carf.vercel.app. Comments automáticos no PR linkam para preview.

Production deploy acontece em merge para main após checks passarem. Vercel executa build de produção e deploya para edge network global. Rollback automático se health check falhar após deploy. DNS configurado para domínio customizado.

Variáveis de ambiente sensíveis (URLs Keycloak, secrets) configuradas no dashboard Vercel, não commitadas no repositório. Preview deployments usam variáveis de ambiente de preview que podem diferir de produção.
