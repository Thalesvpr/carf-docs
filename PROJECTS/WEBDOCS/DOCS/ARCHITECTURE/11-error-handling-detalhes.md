---
type: leaf
status: review
updated: 2026-02-07
---

# Tratamento de Erros - Detalhes

Detalhes de erros de conteudo, paginas customizadas, logging e error boundaries. Documento complementar a 11-error-handling.md.

## Erros de Conteudo

| Erro | Deteccao | Acao | Severidade |
|------|----------|------|------------|
| Pagina nao encontrada | Slug inexistente em content collection | 404 customizada com home, busca, paginas populares | Erro |
| Source ausente | Campo source aponta para arquivo inexistente | Log warning no build, banner discreto na pagina | Warning |
| Frontmatter invalido | Zod validation falha no build | Build falha com erro detalhado | Bloqueante |

## Paginas de Erro Customizadas

| Pagina | Path | Titulo | Acoes |
|--------|------|--------|-------|
| 404 | src/pages/404.astro | Pagina nao encontrada | Ir para home, buscar no site, paginas populares |
| 403 | src/pages/403.astro | Acesso negado | Voltar, home, logout. Exibe roles necessarias e contato admin |
| 500 | src/pages/500.astro | Erro interno | Tentar novamente, home. Contato suporte@carf.com.br |

## Logging

Logging client-side usa console.error com opcional reporting service, incluindo mensagem, stack trace, e acao do usuario.

Logging server-side usa structured logging via pino incluindo timestamp, request_id, error_type, message, stack_trace, user_id (se autenticado), endpoint e method. Exclui tokens, passwords e PII.

## Error Boundaries

Error boundaries React capturam erros em componentes hidratados usando React ErrorBoundary wrapper com fallback UI contendo retry button e logging para monitoramento.
