---
type: readme
status: rejected
description: "Mistura spec com implementacao. Codigo CSS/Tailwind vai para PROJECTS/LIB/TS/UI-COMPONENTS. Aqui so spec abstrata. Contem blocos de codigo."
updated: 2026-01-20
---

# Design System

Especificações visuais do ecossistema CARF definindo cores, tipografia, espaçamento e componentes para garantir consistência visual entre todas as aplicações do sistema.

## Fundamentos

| Especificação | Descrição |
|:--------------|:----------|
| [01-colors](01-colors.md) | Paleta de cores institucional e semântica |
| [02-typography](02-typography.md) | Família tipográfica e escala de tamanhos |
| [03-spacing](03-spacing.md) | Sistema de espaçamento baseado em 8px |
| [04-borders](04-borders.md) | Border-radius scale para componentes |
| [05-shadows](05-shadows.md) | Sistema de elevação e sombras |
| [06-breakpoints](06-breakpoints.md) | Breakpoints responsivos |
| [07-states](07-states.md) | Estados interativos (focus, disabled, error) |
| [08-z-index](08-z-index.md) | Escala de z-index para camadas |
| [09-transitions](09-transitions.md) | Durações e easings de animação |

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

  /* Border Radius */
  --radius-sm: 4px;
  --radius: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.15);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.2);

  /* Z-Index */
  --z-dropdown: 10;
  --z-sticky: 20;
  --z-modal: 30;
  --z-popover: 40;
  --z-toast: 50;

  /* Transitions */
  --duration-fast: 150ms;
  --duration-default: 200ms;
  --duration-slow: 300ms;
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

## Implementação React

A biblioteca **[@carf/ui](../../PROJECTS/LIB/TS/UI-COMPONENTS/README.md)** implementa este Design System em componentes React reutilizáveis baseados em shadcn/ui.

### Instalação

```bash
npm install @carf/ui
```

### Uso

```tsx
import { Button, Card, Input, Badge } from '@carf/ui'
import '@carf/ui/styles'  // CSS variables do Design System

function MyComponent() {
  return (
    <Card>
      <Input placeholder="Digite seu nome" />
      <Button variant="default">Enviar</Button>
      <Badge variant="success">Aprovado</Badge>
    </Card>
  )
}
```

### Componentes Disponíveis

| Categoria | Componentes |
|:----------|:------------|
| Form | Button, Input, Label, Checkbox, Switch, Select, Textarea |
| Layout | Card, Separator, Tabs, Accordion |
| Feedback | Alert, Toast, Dialog, AlertDialog, Progress |
| Data Display | Avatar, Badge, Tooltip, Popover, Table |
| Navigation | DropdownMenu |
| CARF-Specific | UnitCard, HolderCard, CommunityCard, StatusBadge |

## Aplicações

O Design System é aplicado em:

- **@carf/ui** - Biblioteca de componentes React
- **GeoWeb** - Portal web de analistas
- **Painel Admin** - Console de administração
- **WebDocs** - Portal de documentação
- **Keycloak Theme** - Telas de autenticação (FreeMarker e Keycloakify)
- **REURBCAD Mobile** - Aplicativo de campo

## Referências

- [ADR-023](../ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md) - Decisão arquitetural da paleta de cores
- [Ecosystem](../ECOSYSTEM/README.md) - Catálogo de aplicações

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/DESIGN-SYSTEM/01-colors.md|Colors]]
- ○ [[CENTRAL/DESIGN-SYSTEM/02-typography.md|Typography]]
- ○ [[CENTRAL/DESIGN-SYSTEM/03-spacing.md|Spacing]]
- ○ [[CENTRAL/DESIGN-SYSTEM/04-borders.md|Borders]]
- ○ [[CENTRAL/DESIGN-SYSTEM/05-shadows.md|Shadows]]
- ○ [[CENTRAL/DESIGN-SYSTEM/06-breakpoints.md|Breakpoints]]
- ○ [[CENTRAL/DESIGN-SYSTEM/07-states.md|Interactive States]]
- ○ [[CENTRAL/DESIGN-SYSTEM/08-z-index.md|Z-Index Scale]]
- ○ [[CENTRAL/DESIGN-SYSTEM/09-transitions.md|Transitions]]
- ○ [[CENTRAL/DESIGN-SYSTEM/color-palette.md|Color Palette]]

<!-- CARF-INDEX-END -->
