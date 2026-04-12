---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao com UI Components

WEBDOCS importa tema visual da biblioteca @carf/ui garantindo consistencia de cores, tipografia e espacamentos com demais aplicacoes do ecossistema CARF sem duplicacao de definicoes.

Design tokens exportados por ui-components incluem cores (primary, secondary, neutral, semantic), tipografia (font families, sizes, weights, line heights), espacamentos (scale de 4px), bordas (radius, widths), e sombras. Tokens disponiveis como CSS custom properties e objetos JavaScript/TypeScript.

Configuracao do Starlight em astro.config.mjs importa customTheme de ui-components aplicando cores primarias ao header, links, e elementos interativos. Dark mode usa variantes escuras dos mesmos tokens mantendo contraste WCAG AA em ambos temas.

CSS global em src/styles/global.css importa @carf/ui/styles/tokens.css disponibilizando todas custom properties no escopo :root. Componentes customizados usam var(--carf-color-primary-500) referenciando tokens ao inves de valores hardcoded.

Atualizacoes de ui-components propagam automaticamente para WEBDOCS na proxima build. Mudancas breaking (remocao de tokens, alteracao de nomes) sao detectadas por TypeScript compilation errors garantindo que incompatibilidades sejam corrigidas antes de deploy.

## Tokens Disponiveis

| Categoria | Prefixo | Exemplo |
|-----------|---------|---------|
| Cores primarias | --carf-color-primary-* | --carf-color-primary-500 |
| Cores neutras | --carf-color-gray-* | --carf-color-gray-100 |
| Semanticas | --carf-color-{success,warning,error}-* | --carf-color-error-500 |
| Texto | --carf-color-text-* | --carf-color-text-muted |
| Background | --carf-color-bg-* | --carf-color-bg-surface |
| Espacamento | --carf-space-{1-12} | --carf-space-4 (16px) |
| Tipografia | --carf-text-* | --carf-text-lg |
| Raio | --carf-radius-* | --carf-radius-lg |
| Sombras | --carf-shadow-* | --carf-shadow-md |

## Uso em Componentes

Componentes customizados referenciam tokens via var() para cores (--carf-color-text-primary, --carf-color-bg-surface, --carf-color-border-default), cores semanticas (--carf-color-success-500, --carf-color-warning-500, --carf-color-error-500), tipografia (--carf-font-sans, --carf-text-base, --carf-leading-normal), espacamentos na escala de 4px (--carf-space-4 para 16px, --carf-space-6 para 24px, --carf-space-2 para 8px), bordas (--carf-radius-md, --carf-border-default), e sombras (--carf-shadow-sm).

## Dark Mode

Tokens automaticamente ajustam valores para dark mode via media query prefers-color-scheme. Nenhuma configuracao adicional necessaria nos componentes. Exemplo: --carf-color-bg-surface resolve para #ffffff em light e #1a1a1a em dark automaticamente.
