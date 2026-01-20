---
status: review
updated: 2026-01-17
---

# Integração com UI Components

WEBDOCS importa tema visual da biblioteca @carf/ui-components garantindo consistência de cores, tipografia e espaçamentos com demais aplicações do ecossistema CARF sem duplicação de definições.

Design tokens exportados por ui-components incluem cores (primary, secondary, neutral, semantic), tipografia (font families, sizes, weights, line heights), espaçamentos (scale de 4px), bordas (radius, widths), e sombras. Tokens disponíveis como CSS custom properties e objetos JavaScript/TypeScript.

Configuração do Starlight em astro.config.mjs importa customTheme de ui-components aplicando cores primárias ao header, links, e elementos interativos. Dark mode usa variantes escuras dos mesmos tokens mantendo contraste WCAG AA em ambos temas.

CSS global em src/styles/global.css importa @carf/ui-components/styles/tokens.css disponibilizando todas custom properties no escopo :root. Componentes customizados usam var(--carf-color-primary-500) referenciando tokens ao invés de valores hardcoded.

Atualizações de ui-components propagam automaticamente para WEBDOCS na próxima build. Mudanças breaking (remoção de tokens, alteração de nomes) são detectadas por TypeScript compilation errors garantindo que incompatibilidades sejam corrigidas antes de deploy.
