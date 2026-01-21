---
status: rejected
description: "Mistura spec com implementacao. Codigo CSS/Tailwind vai para PROJECTS/LIB/TS/UI-COMPONENTS. Aqui so spec abstrata. Contem blocos de codigo."
updated: 2026-01-20
---

# Colors

Paleta de cores oficial do projeto CARF composta por três cores primárias institucionais, cores de suporte e escala de cinzas, garantindo identidade visual consistente e acessibilidade WCAG 2.1 AA.

## Cores Primárias

Tríade vibrante representando a identidade visual do CARF:

| Cor | Hex | RGB | Uso |
|:----|:----|:----|:----|
| Amarelo | `#FFCD07` | 255, 205, 7 | Energia, atenção, elementos decorativos |
| Verde | `#15981C` | 21, 152, 28 | Natureza, sucesso, aprovação |
| Azul | `#3872C6` | 56, 114, 198 | Confiança, tecnologia, links |

### Amarelo `#FFCD07`

- Elementos decorativos destacados
- Banners informativos
- Badges de status pendente
- Indicadores visuais de atenção
- Call-to-action secundários

### Verde `#15981C`

- Indicadores de sucesso
- Status de aprovação/ativo
- Validação correta
- Confirmação de ações completadas

### Azul `#3872C6`

- Links interativos
- Elementos clicáveis
- Informações contextuais
- Navegação secundária
- Fundo de painéis informativos

## Cores Institucionais

Verde institucional para branding governamental:

| Cor | Hex | RGB | Uso |
|:----|:----|:----|:----|
| Verde Institucional | `#2C5F2D` | 44, 95, 45 | Backgrounds, botões primários |
| Verde Escuro | `#1A3D1B` | 26, 61, 27 | Hover states, gradients |

### Verde Institucional `#2C5F2D`

- Background principal em painéis de branding
- Headers de login
- Sidebars institucionais
- Botões primários de ação
- Representa identidade governamental municipal

### Verde Escuro `#1A3D1B`

- Hover states de botões primários
- Gradients para profundidade visual
- Borders de destaque

## Cor de Destaque

| Cor | Hex | RGB | Uso |
|:----|:----|:----|:----|
| Vermelho Accent | `#E63946` | 230, 57, 70 | Linhas decorativas, separadores |

Usado exclusivamente para elementos decorativos de destaque, não para indicar erro.

## Escala de Cinzas

Baseada no Tailwind CSS para consistência com shadcn/ui:

| Token | Hex | Uso |
|:------|:----|:----|
| `gray-100` | `#F7F7F7` | Backgrounds sutis, cards |
| `gray-300` | `#D1D5DB` | Borders, inputs, separadores |
| `gray-500` | `#6B7280` | Placeholders, texto secundário |
| `gray-700` | `#374151` | Labels, corpo secundário, ícones |
| `gray-900` | `#111827` | Títulos, headings, texto principal |
| `white` | `#FFFFFF` | Backgrounds principais, cards, forms |

## CSS Variables

```css
:root {
  /* Primárias */
  --color-yellow: #FFCD07;
  --color-green: #15981C;
  --color-blue: #3872C6;

  /* Institucionais */
  --color-primary: #2C5F2D;
  --color-primary-dark: #1A3D1B;

  /* Accent */
  --color-accent: #E63946;

  /* Cinzas */
  --color-gray-100: #F7F7F7;
  --color-gray-300: #D1D5DB;
  --color-gray-500: #6B7280;
  --color-gray-700: #374151;
  --color-gray-900: #111827;
}
```

## Tailwind Classes

```javascript
// tailwind.config.js
colors: {
  carf: {
    yellow: '#FFCD07',
    green: '#15981C',
    blue: '#3872C6',
    primary: '#2C5F2D',
    'primary-dark': '#1A3D1B',
    accent: '#E63946',
  }
}
```

Uso: `bg-carf-yellow`, `text-carf-green`, `border-carf-blue`, `bg-carf-primary`

## Acessibilidade

Conformidade WCAG 2.1 AA (contrast ratio minimo 4.5:1 para texto normal, 3:1 para texto grande):

| Combinacao | Ratio | Status |
|:-----------|:------|:-------|
| Verde Institucional `#2C5F2D` sobre branco | 7.2:1 | Excelente |
| Azul `#3872C6` sobre branco | 4.8:1 | Adequado |
| Amarelo `#FFCD07` sobre branco | 1.4:1 | Somente decorativo |

**Regras:**
- Amarelo nunca usado para texto (baixo contraste)
- Cores nao transmitem informacao sozinhas
- Sempre acompanhadas de texto ou icone (daltonismo-friendly)

## Referências

- [ADR-023](../ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md) - Decisão arquitetural
- [WCAG 2.1 Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum)
