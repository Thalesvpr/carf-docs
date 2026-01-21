---
status: review
updated: 2026-01-21
---

# Visão Geral da Arquitetura

WEBDOCS é portal de documentação construído com Astro 4 e Starlight theme usando hybrid rendering que combina páginas estáticas geradas em build time (SSG) para conteúdo público com páginas renderizadas no servidor (SSR) para seção protegida /dev/ que requer autenticação Keycloak.

Stack tecnológico inclui Astro 4 como framework web com Islands Architecture para hidratação seletiva, Starlight como theme de documentação com sidebar navigation e search integrado, TypeScript para type safety em componentes e configuração, Bun como runtime e bundler com performance superior a Node, Content Collections para gerenciamento de conteúdo Markdown com validação Zod, Pagefind para busca full-text client-side indexada em build time, e Vercel como plataforma de hosting com edge network global.

Fluxo de requisição para páginas públicas serve HTML estático do CDN Vercel com latência mínima. Páginas em /dev/ passam por função serverless que valida token JWT do Keycloak e verifica role dev antes de renderizar conteúdo. Swagger embutido executa fetch da especificação OpenAPI da GEOAPI durante SSR.

Conteúdo é editável via Decap CMS (Git-based) permitindo contribuidores não-técnicos editarem documentação via interface visual no navegador com commits automáticos para GitHub. CMS autentica via Keycloak garantindo que apenas usuários autorizados podem editar.

Tema visual importa tokens de @carf/ui garantindo consistência de cores, tipografia e espaçamentos com demais aplicações do ecossistema CARF. Dark mode usa variantes escuras dos mesmos tokens.
