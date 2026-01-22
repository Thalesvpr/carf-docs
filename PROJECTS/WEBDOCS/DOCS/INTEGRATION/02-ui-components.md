---
type: leaf
status: review
updated: 2026-01-21
---

# Integração com UI Components

WEBDOCS importa tema visual da biblioteca @carf/ui garantindo consistência de cores, tipografia e espaçamentos com demais aplicações do ecossistema CARF sem duplicação de definições.

Design tokens exportados por ui-components incluem cores (primary, secondary, neutral, semantic), tipografia (font families, sizes, weights, line heights), espaçamentos (scale de 4px), bordas (radius, widths), e sombras. Tokens disponíveis como CSS custom properties e objetos JavaScript/TypeScript.

Configuração do Starlight em astro.config.mjs importa customTheme de ui-components aplicando cores primárias ao header, links, e elementos interativos. Dark mode usa variantes escuras dos mesmos tokens mantendo contraste WCAG AA em ambos temas.

CSS global em src/styles/global.css importa @carf/ui/styles/tokens.css disponibilizando todas custom properties no escopo :root. Componentes customizados usam var(--carf-color-primary-500) referenciando tokens ao invés de valores hardcoded.

Atualizações de ui-components propagam automaticamente para WEBDOCS na próxima build. Mudanças breaking (remoção de tokens, alteração de nomes) são detectadas por TypeScript compilation errors garantindo que incompatibilidades sejam corrigidas antes de deploy.

## Uso dos Design Tokens

### CSS Custom Properties

```css
/* Disponíveis após importar @carf/ui/styles/tokens.css */

.meu-componente {
  /* Cores */
  color: var(--carf-color-text-primary);
  background: var(--carf-color-bg-surface);
  border-color: var(--carf-color-border-default);

  /* Cores semânticas */
  --success: var(--carf-color-success-500);
  --warning: var(--carf-color-warning-500);
  --error: var(--carf-color-error-500);

  /* Tipografia */
  font-family: var(--carf-font-sans);
  font-size: var(--carf-text-base);
  line-height: var(--carf-leading-normal);

  /* Espaçamentos (escala de 4px) */
  padding: var(--carf-space-4); /* 16px */
  margin-bottom: var(--carf-space-6); /* 24px */
  gap: var(--carf-space-2); /* 8px */

  /* Bordas */
  border-radius: var(--carf-radius-md);
  border-width: var(--carf-border-default);

  /* Sombras */
  box-shadow: var(--carf-shadow-sm);
}
```

### Tokens Disponíveis

| Categoria | Prefixo | Exemplo |
|-----------|---------|---------|
| Cores primárias | `--carf-color-primary-*` | `--carf-color-primary-500` |
| Cores neutras | `--carf-color-gray-*` | `--carf-color-gray-100` |
| Semânticas | `--carf-color-{success,warning,error}-*` | `--carf-color-error-500` |
| Texto | `--carf-color-text-*` | `--carf-color-text-muted` |
| Background | `--carf-color-bg-*` | `--carf-color-bg-surface` |
| Espaçamento | `--carf-space-{1-12}` | `--carf-space-4` (16px) |
| Tipografia | `--carf-text-*` | `--carf-text-lg` |
| Raio | `--carf-radius-*` | `--carf-radius-lg` |
| Sombras | `--carf-shadow-*` | `--carf-shadow-md` |

### Dark Mode

Tokens automaticamente ajustam valores para dark mode via media query:

```css
/* Não precisa fazer nada - tokens respondem ao prefers-color-scheme */
.card {
  background: var(--carf-color-bg-surface);
  /* Automaticamente #ffffff em light, #1a1a1a em dark */
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
