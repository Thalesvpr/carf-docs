---
status: review
updated: 2026-01-17
---

# Astro Starlight

Astro é framework web focado em performance que gera sites estáticos por padrão com opção de renderização server-side quando necessário. Diferente de frameworks SPA tradicionais, Astro envia zero JavaScript ao cliente por padrão resultando em páginas extremamente rápidas com scores Lighthouse próximos a 100.

Starlight é theme oficial do Astro para documentação técnica adicionando sidebar navigation automática, table of contents, breadcrumbs, search integrado, dark mode, e design responsivo mobile-first com acessibilidade WCAG AA. Configuração em astro.config.mjs define título, logo, navegação customizada, e integrações.

Islands Architecture permite componentes interativos seletivos onde apenas partes da página que precisam de JavaScript (como busca ou toggles) são hidratadas no cliente enquanto resto permanece HTML estático. Diretiva client:load hidrata componente imediatamente, client:visible hidrata quando visível no viewport, e client:idle hidrata quando navegador está ocioso.

Hybrid Rendering combina SSG para páginas públicas geradas no build time com SSR para páginas dinâmicas como seção /dev/ protegida por auth. Configuração output: 'hybrid' no astro.config.mjs habilita modo híbrido, e export const prerender = false em páginas específicas marca para SSR.
