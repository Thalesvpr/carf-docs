---
type: leaf
status: review
updated: 2026-02-07
---

# Troubleshooting - Runtime

Resolucao de problemas de runtime, performance e desenvolvimento local. Arquivos relacionados: 09-troubleshooting-auth.md para problemas de autenticacao e 09-troubleshooting-build.md para problemas de build.

## Health Check Sempre Failing

Sintoma: servico mostra como offline na status page mesmo estando online.

| Passo | Acao | Verificacao |
|---|---|---|
| 1 | Testar endpoint diretamente via browser ou ferramenta HTTP | Resposta retorna status esperado |
| 2 | Verificar timeout | Timeout configurado pode ser muito curto para servico |
| 3 | Verificar CORS | Health endpoint deve permitir origem do WEBDOCS |
| 4 | Verificar SSL | Certificado valido e nao expirado |

## Status Page Mostra Dados Antigos

Sintoma: status nao atualiza mesmo com refresh. Causa tipica e SSR com cache ou CDN cache. Verificar que response inclui Cache-Control no-cache, adicionar parametro timestamp na URL se necessario, e confirmar que vercel.json nao esta cacheando rota /status.

## Pagina Carrega Lentamente

Sintoma: Lighthouse mostra score baixo de performance nas metricas LCP, FCP, TTI e CLS.

| Problema | Solucao |
|---|---|
| Imagens nao otimizadas | Usar astro:assets para otimizacao automatica |
| JS bloqueando render | Adicionar defer ou async em scripts |
| CSS nao utilizado | Aplicar PurgeCSS ou revisar imports |
| Assets sem cache headers | Configurar Cache-Control conforme SPECS/24 |

## Bun/Node Version Mismatch

Sintoma: erros estranhos ou comportamento inconsistente. Verificar versao do Bun (esperado 1.0.0 ou superior) e Node (esperado 20.0.0 ou superior). Atualizar Bun reinstalando via script oficial e Node via nvm.

## Hot Reload Nao Funciona

Sintoma: mudancas no codigo nao refletem no browser. Verificar se dev server esta rodando, reiniciar com Ctrl+C e bun dev, limpar cache do Astro removendo pasta .astro, e confirmar que arquivo esta sendo watched pelo servidor.

## Erro de Permissao em Windows

Sintoma: EPERM operation not permitted. Fechar VS Code e outros editores que podem estar lockando arquivos. Executar terminal como administrador. Desabilitar antivirus temporariamente. Considerar usar WSL2 para desenvolvimento.

## Logs e Debugging

Para habilitar logs detalhados em desenvolvimento, executar bun dev com variavel DEBUG. Usar DEBUG=astro:* para logs do Astro, DEBUG=auth:* para apenas autenticacao, ou DEBUG=* para todos logs. Em producao no Vercel, acessar logs via CLI com vercel logs seguido da URL do site com flag --follow, ou via dashboard em Deployments, Functions, Logs.

## Checklist de Diagnostico

| Verificacao |
|---|
| Console do browser sem erros |
| Network tab mostra requests com status 200 |
| Cookies sendo salvos corretamente |
| Variaveis de ambiente configuradas |
| Build local passa sem erros |
| Keycloak acessivel |
| GeoAPI health check retornando OK |
| DNS resolvendo corretamente |
| SSL/TLS valido |
