# Design System

Especificações visuais do ecossistema CARF definindo cores, tipografia, espaçamento e componentes para garantir consistência visual entre todas as aplicações do sistema.

## Fundamentos

| Especificação | Descrição |
|:--------------|:----------|
| [01-colors](01-colors.md) | Paleta de cores institucional e semântica |
| [02-typography](02-typography.md) | Família tipográfica e escala de tamanhos |
| [03-spacing](03-spacing.md) | Sistema de espaçamento baseado em 8px |

## Princípios

1. **Consistência** - Mesma linguagem visual em todas as aplicações
2. **Acessibilidade** - Conformidade WCAG 2.1 AA em contrastes e interações
3. **Escalabilidade** - Tokens reutilizáveis via CSS Variables
4. **Identidade** - Cores institucionais representando confiança governamental

## Implementação

### CSS Variables

Todas as aplicações frontend devem importar as variáveis CSS padrão:

```css
:root {
  /* Cores primárias */
  --color-yellow: #FFCD07;
  --color-green: #15981C;
  --color-blue: #3872C6;

  /* Cores institucionais */
  --color-primary: #2C5F2D;
  --color-primary-dark: #1A3D1B;

  /* Tipografia */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  /* Espaçamento */
  --space-unit: 8px;
}
```

### Tailwind CSS

Configuração do `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        carf: {
          yellow: 'var(--color-yellow)',
          green: 'var(--color-green)',
          blue: 'var(--color-blue)',
          primary: 'var(--color-primary)',
        }
      }
    }
  }
}
```

## Aplicações

O Design System é aplicado em:

- **GeoWeb** - Portal web de analistas
- **Painel Admin** - Console de administração
- **WebDocs** - Portal de documentação
- **Keycloak Theme** - Telas de autenticação
- **REURBCAD Mobile** - Aplicativo de campo

## Referências

- [ADR-023](../ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md) - Decisão arquitetural da paleta de cores
- [Ecosystem](../ECOSYSTEM/README.md) - Catálogo de aplicações

---

**Status do arquivo:** Draft
**Última atualização:** 2026-01-19
