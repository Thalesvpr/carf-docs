---
status: review
updated: 2026-01-17
---

# Renderização

WEBDOCS usa hybrid rendering do Astro combinando Static Site Generation (SSG) para maioria das páginas com Server-Side Rendering (SSR) para páginas que requerem dados dinâmicos ou autenticação.

Páginas SSG são geradas em build time resultando em HTML estático servido diretamente do CDN com latência mínima. Inclui todas seções públicas: guia, sistema, manuais, api, changelog. Conteúdo não muda entre requests então caching agressivo é seguro.

Páginas SSR são renderizadas no servidor em cada request permitindo verificação de autenticação, fetch de dados dinâmicos, e personalização por usuário. Inclui seção /dev/ que verifica role, /status/ que faz health checks, e /admin/ para CMS.

Configuração em astro.config.mjs define output hybrid habilitando ambos modos. Páginas são SSG por padrão. Adicionar export const prerender = false no arquivo marca página para SSR.

Adapter @astrojs/vercel configura deploy para Vercel Functions. Páginas SSR são deployadas como funções serverless executando em edge locations próximas aos usuários. Cold start minimizado com funções pequenas e dependências otimizadas.

Islands Architecture permite componentes interativos em páginas SSG. Diretiva client:load hidrata componente imediatamente no cliente. Usado para busca, toggles, e outros elementos que requerem JavaScript. Resto da página permanece HTML estático.

Build output gera dist/ com HTML estático para páginas SSG e funções serverless para páginas SSR. Vercel detecta automaticamente tipos de output e configura routing apropriado.
