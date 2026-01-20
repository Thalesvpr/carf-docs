---
id: ""
type: ARCH
modules: []
epic: ""
status: review
created: 2026-01-20
updated: 2026-01-20
---

# Pipeline de CI

GitHub Actions executa validações automáticas em pull requests e deploys garantindo qualidade antes de merge e publicação.

Workflow .github/workflows/ci.yml dispara em push para main e pull requests. Jobs paralelos executam lint, type check, build, testes, e validações de qualidade. Falha em qualquer job bloqueia merge do PR.

Job de lint executa ESLint para código TypeScript e Astro, Prettier para formatação, e markdownlint para arquivos Markdown. Configuração em arquivos respectivos na raiz do projeto. Erros de lint falham CI com lista de problemas.

Job de type check executa tsc e astro check validando tipos TypeScript e sintaxe Astro. Erros de tipo indicam problemas que podem causar falhas em runtime. Build não prossegue com erros de tipo.

Job de build executa npm run build gerando site estático. Inclui validação de Content Collections (schema Zod), validação de links internos, e geração de índice Pagefind. Falha de build bloqueia deploy.

Job de testes executa Playwright para testes e2e incluindo axe-core para acessibilidade. Testes rodam contra preview deploy gerado pelo Vercel. Screenshots de falhas armazenados como artifacts para debug.

Job de Lighthouse CI executa após deploy de preview medindo performance e gerando relatório. Thresholds definidos em lighthouserc.js. Falha em métricas críticas adiciona comment no PR com detalhes.

Deploy para produção acontece automaticamente após merge em main quando todos checks passam. Vercel detecta push e inicia deploy. Rollback automático se health check falhar após deploy.

---
