---
type: leaf
status: review
updated: 2026-02-07
---

# Troubleshooting - Build

Resolucao de problemas de build e Decap CMS. Arquivos relacionados: 09-troubleshooting-auth.md para problemas de autenticacao e 09-troubleshooting-runtime.md para problemas de runtime.

## Build Falha com Erro de Frontmatter

Sintoma: Astro build falha com erro de validacao como ZodError indicando campo com restricao nao atendida. Para identificar arquivo com problema, executar bun run astro check. Corrigir frontmatter conforme schema definido em SPECS/23-content-schema-overview.md.

## Build Falha com Import Error

Sintoma: erro "Cannot find module" ou "Failed to resolve import".

| Causa | Solucao |
|---|---|
| Dependencia ausente | Executar bun install |
| Caminho incorreto | Verificar caminho relativo vs absoluto |
| Alias nao configurado | Verificar tsconfig.json paths com baseUrl e mapeamentos para @/ (src/), @components/ (src/components/) e @lib/ (src/lib/) |

## Out of Memory Durante Build

Sintoma: build falha com "JavaScript heap out of memory".

| Solucao | Detalhes |
|---|---|
| Aumentar memoria | Executar build com NODE_OPTIONS --max-old-space-size=4096 |
| Verificar imports circulares | Usar ferramenta madge com flag --circular em src/ |
| Lazy load componentes pesados | Usar pattern de import dinamico com lazy |

## CMS Nao Carrega

Sintoma: pagina /admin mostra tela branca ou erro. Verificar console do browser por erros, confirmar que /admin/config.yml existe, validar YAML syntax, e verificar backend configurado corretamente. Configuracao minima funcional requer backend com name github, repo, branch main, base_url e auth_endpoint; media_folder apontando para public/images; e ao menos uma collection com name, label, folder, create true e fields definidos.

## CMS Auth Failed

Sintoma: erro ao autenticar no GitHub via CMS.

| Causa | Verificacao |
|---|---|
| GitHub OAuth nao configurado | GitHub, Settings, Developer settings, OAuth Apps; confirmar Authorization callback URL correta |
| Variaveis de ambiente ausentes | Confirmar GITHUB_CLIENT_ID e GITHUB_CLIENT_SECRET configurados em .env.local ou Vercel |

## CMS Preview Nao Funciona

Sintoma: preview mostra conteudo errado ou nao atualiza. Verificar que registerPreviewTemplate esta sendo chamado, que componente de preview importa estilos corretamente, e fazer hard refresh do CMS com Ctrl+Shift+R.
