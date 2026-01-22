---
type: leaf
status: review
updated: 2026-01-22
---

# Component Showcase

Especificação da seção de showcase de componentes no WEBDOCS, inspirada no Material Design Components Gallery, que exibe todos os componentes disponíveis na biblioteca @carf/ui com exemplos interativos e documentação de uso.

## Visão Geral

A seção /dev/components/ funciona como uma galeria de componentes similar ao material.io/components, permitindo desenvolvedores explorarem todos os componentes disponíveis em @carf/ui com exemplos vivos, variantes, props e código de uso.

```json
{
  "purpose": "Documentar e demonstrar todos componentes @carf/ui",
  "audience": "Desenvolvedores (role dev)",
  "location": "/dev/components/",
  "inspiration": [
    "material.io/components",
    "ui.shadcn.com",
    "storybook"
  ],
  "features": [
    "Exemplos interativos",
    "Variantes visuais",
    "Props documentadas",
    "Código copiável",
    "Playground opcional"
  ]
}
```

## Estrutura de Navegação

```json
{
  "sidebar": {
    "label": "Componentes",
    "parent": "Desenvolvedores",
    "items": [
      {
        "label": "Visão Geral",
        "slug": "dev/components"
      },
      {
        "label": "Ações",
        "collapsed": true,
        "items": [
          { "label": "Button", "slug": "dev/components/button" },
          { "label": "IconButton", "slug": "dev/components/icon-button" },
          { "label": "FAB", "slug": "dev/components/fab" }
        ]
      },
      {
        "label": "Inputs",
        "collapsed": true,
        "items": [
          { "label": "Input", "slug": "dev/components/input" },
          { "label": "Textarea", "slug": "dev/components/textarea" },
          { "label": "Select", "slug": "dev/components/select" },
          { "label": "Checkbox", "slug": "dev/components/checkbox" },
          { "label": "Radio", "slug": "dev/components/radio" },
          { "label": "Switch", "slug": "dev/components/switch" },
          { "label": "Slider", "slug": "dev/components/slider" }
        ]
      },
      {
        "label": "Navegação",
        "collapsed": true,
        "items": [
          { "label": "Tabs", "slug": "dev/components/tabs" },
          { "label": "Breadcrumb", "slug": "dev/components/breadcrumb" },
          { "label": "Pagination", "slug": "dev/components/pagination" },
          { "label": "DropdownMenu", "slug": "dev/components/dropdown-menu" }
        ]
      },
      {
        "label": "Feedback",
        "collapsed": true,
        "items": [
          { "label": "Toast", "slug": "dev/components/toast" },
          { "label": "Alert", "slug": "dev/components/alert" },
          { "label": "Progress", "slug": "dev/components/progress" },
          { "label": "Skeleton", "slug": "dev/components/skeleton" },
          { "label": "Spinner", "slug": "dev/components/spinner" }
        ]
      },
      {
        "label": "Overlays",
        "collapsed": true,
        "items": [
          { "label": "Dialog", "slug": "dev/components/dialog" },
          { "label": "Sheet", "slug": "dev/components/sheet" },
          { "label": "Popover", "slug": "dev/components/popover" },
          { "label": "Tooltip", "slug": "dev/components/tooltip" }
        ]
      },
      {
        "label": "Layout",
        "collapsed": true,
        "items": [
          { "label": "Card", "slug": "dev/components/card" },
          { "label": "Separator", "slug": "dev/components/separator" },
          { "label": "Accordion", "slug": "dev/components/accordion" },
          { "label": "Collapsible", "slug": "dev/components/collapsible" }
        ]
      },
      {
        "label": "Data Display",
        "collapsed": true,
        "items": [
          { "label": "Table", "slug": "dev/components/table" },
          { "label": "Badge", "slug": "dev/components/badge" },
          { "label": "Avatar", "slug": "dev/components/avatar" }
        ]
      }
    ]
  }
}
```

## Estrutura de Página de Componente

Cada página de componente segue estrutura consistente.

```json
{
  "page_structure": {
    "header": {
      "title": "Nome do componente",
      "description": "Descrição curta do propósito",
      "source_link": "Link para código fonte no GitHub"
    },
    "demo": {
      "position": "Logo após header",
      "content": "Exemplo interativo do componente",
      "variants": "Toggle para diferentes variantes"
    },
    "installation": {
      "import_statement": "import { Button } from '@carf/ui'",
      "dependencies": "Dependências se houver"
    },
    "usage": {
      "basic_example": "Código mínimo para usar",
      "with_astro": "Como usar com hidratação Astro"
    },
    "variants": {
      "visual_examples": "Grid com todas variantes visuais",
      "code_for_each": "Código para cada variante"
    },
    "props": {
      "table": "Tabela com todas props",
      "columns": ["Nome", "Tipo", "Default", "Descrição"]
    },
    "accessibility": {
      "aria": "Atributos ARIA suportados",
      "keyboard": "Navegação por teclado"
    },
    "examples": {
      "real_world": "Exemplos de uso no sistema CARF",
      "patterns": "Padrões comuns de uso"
    }
  }
}
```

## Componente ComponentDemo

Componente Astro para renderizar demos interativas.

```json
{
  "ComponentDemo": {
    "path": "src/components/docs/ComponentDemo.astro",
    "props": {
      "component": "Nome do componente a demonstrar",
      "variants": "Array de variantes para mostrar",
      "defaultProps": "Props padrão para o exemplo"
    },
    "features": {
      "live_preview": "Componente renderizado e interativo",
      "code_display": "Código com syntax highlighting",
      "copy_button": "Copiar código para clipboard",
      "variant_switcher": "Toggle entre variantes",
      "props_editor": "Opcional - editar props ao vivo"
    }
  }
}
```

## Componente PropsTable

Componente para exibir tabela de props.

```json
{
  "PropsTable": {
    "path": "src/components/docs/PropsTable.astro",
    "props": {
      "props": "Array de definições de props"
    },
    "prop_definition": {
      "name": "Nome da prop",
      "type": "Tipo TypeScript",
      "default": "Valor padrão se houver",
      "required": "Se é obrigatória",
      "description": "Descrição do que faz"
    }
  }
}
```

## Geração Automática

Props e tipos podem ser extraídos automaticamente do código fonte da @carf/ui.

```json
{
  "auto_generation": {
    "source": "@carf/ui package",
    "extract": [
      "Interface de Props de cada componente",
      "JSDoc comments",
      "Default values"
    ],
    "output": "JSON usado pelos componentes de documentação",
    "trigger": "Build do WEBDOCS ou script manual"
  }
}
```

## Tokens de Design

Página especial documentando design tokens da @carf/ui.

```json
{
  "design_tokens": {
    "path": "/dev/components/tokens",
    "sections": {
      "colors": {
        "primary": "Paleta principal",
        "semantic": "Cores semânticas (success, error, etc)",
        "neutral": "Escalas de cinza"
      },
      "typography": {
        "font_family": "Fontes usadas",
        "font_sizes": "Escala de tamanhos",
        "line_heights": "Alturas de linha",
        "font_weights": "Pesos de fonte"
      },
      "spacing": {
        "scale": "Escala de espaçamento (4, 8, 12, 16, etc)",
        "usage": "Quando usar cada valor"
      },
      "borders": {
        "radius": "Border radius disponíveis",
        "widths": "Larguras de borda"
      },
      "shadows": {
        "elevations": "Níveis de elevação/sombra"
      },
      "breakpoints": {
        "values": "Breakpoints responsivos",
        "usage": "Media queries"
      }
    }
  }
}
```

## Integração com Storybook

Opcionalmente, as demos podem ser powered by Storybook embeddado.

```json
{
  "storybook_integration": {
    "option": "Embed Storybook stories nas páginas",
    "benefits": [
      "Stories já existentes na @carf/ui",
      "Addons de acessibilidade",
      "Canvas interativo"
    ],
    "implementation": {
      "build": "Storybook build estático",
      "embed": "iframe ou fetch stories JSON"
    },
    "alternative": "Componentes Astro nativos com hidratação React"
  }
}
```

## Source Alignment

Páginas de componentes referenciam código fonte como source.

```json
{
  "source_mapping": {
    "pattern": "PROJECTS/LIB/TS/UI/src/components/{component}/index.tsx",
    "example": {
      "page": "/dev/components/button",
      "source": "PROJECTS/LIB/TS/UI/src/components/Button/index.tsx"
    }
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
