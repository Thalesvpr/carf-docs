---
type: leaf
status: review
updated: 2026-02-07
---

# Error Pages

Paginas de erro customizadas substituindo defaults do Astro/Starlight.

## Paginas

| Pagina | Arquivo | Trigger |
|--------|---------|---------|
| 404 | src/pages/404.astro | Pagina nao encontrada |
| 403 | src/pages/403.astro | Acesso negado por role |
| 500 | src/pages/500.astro | Erro interno |

## 404 - Nao Encontrada

Heading "404", subheading "Ops! Esta pagina nao existe", mensagem sobre pagina movida. Acoes: Voltar para Home e Buscar documentacao. Sugestoes com links para Guia, Manuais e Status.

## 403 - Acesso Negado

Heading "403", mensagem indicando roles necessarias usando locals.allowedRoles com labels traduzidas (field-cadastrator para Cadastrador de Campo, analyst para Analista etc). Exibe email e roles do usuario autenticado. Acoes: Voltar para Home e Fazer logout. Mensagem de contato com administrador.

Middleware seta locals.allowedRoles e requestedSection, usa Astro.rewrite para redirecionar.

## 500 - Erro Interno

Heading "500", subheading "Algo deu errado". Botao Tentar novamente com reload, link Voltar para Home. Em modo DEV exibe error.message e stack em details. Mensagem de contato com suporte.

## CSS

Estilos em src/styles/error-pages.css importado via customCss. Pagina centralizada com min-height 60vh em flexbox. Codigo 6rem com cor accent. Botoes com padding 0.75rem, primario com background accent, secundario com gray-6. Role badges com border-radius 1rem. Debug info com background gray-7.
