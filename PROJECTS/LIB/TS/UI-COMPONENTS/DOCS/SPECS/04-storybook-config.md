---
title: "Storybook Config - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Storybook Config - @carf/ui

Configuracao do Storybook para documentacao interativa de componentes.

## Estrutura de Configuracao

```
.storybook/
├── main.ts           # Configuracao principal
├── preview.ts        # Configuracao de preview
├── manager.ts        # Configuracao do manager UI
└── theme.ts          # Tema customizado CARF
```

## main.ts

```typescript
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: [
    '../src/**/*.mdx',
    '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'
  ],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  viteFinal: async (config) => {
    // Customizacoes do Vite se necessario
    return config
  },
}

export default config
```

## preview.ts

```typescript
import type { Preview } from '@storybook/react'
import '../src/styles/globals.css'

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
        { name: 'carf-primary', value: '#2C5F2D' },
      ],
    },
    viewport: {
      viewports: {
        mobile: {
          name: 'Mobile',
          styles: { width: '375px', height: '667px' },
        },
        tablet: {
          name: 'Tablet',
          styles: { width: '768px', height: '1024px' },
        },
        desktop: {
          name: 'Desktop',
          styles: { width: '1280px', height: '800px' },
        },
      },
    },
  },
  decorators: [
    (Story, context) => {
      // Aplicar dark mode baseado no background selecionado
      const isDark = context.globals.backgrounds?.value === '#1a1a1a'

      return (
        <div className={isDark ? 'dark' : ''}>
          <div className="min-h-screen bg-background text-foreground p-4">
            <Story />
          </div>
        </div>
      )
    },
  ],
  globalTypes: {
    theme: {
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        title: 'Theme',
        icon: 'circlehollow',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
}

export default preview
```

## manager.ts

```typescript
import { addons } from '@storybook/manager-api'
import { carfTheme } from './theme'

addons.setConfig({
  theme: carfTheme,
  sidebar: {
    showRoots: true,
  },
  toolbar: {
    zoom: { hidden: false },
    eject: { hidden: true },
    copy: { hidden: false },
    fullscreen: { hidden: false },
  },
})
```

## theme.ts

```typescript
import { create } from '@storybook/theming/create'

export const carfTheme = create({
  base: 'light',

  // Branding
  brandTitle: '@carf/ui',
  brandUrl: 'https://github.com/carf/carf-ui',
  brandImage: '/carf-logo.svg',
  brandTarget: '_self',

  // Colors
  colorPrimary: '#2C5F2D',
  colorSecondary: '#97BC62',

  // UI
  appBg: '#f8fafc',
  appContentBg: '#ffffff',
  appBorderColor: '#e2e8f0',
  appBorderRadius: 8,

  // Text colors
  textColor: '#1e293b',
  textInverseColor: '#ffffff',
  textMutedColor: '#64748b',

  // Toolbar colors
  barTextColor: '#64748b',
  barSelectedColor: '#2C5F2D',
  barBg: '#ffffff',

  // Form colors
  inputBg: '#ffffff',
  inputBorder: '#e2e8f0',
  inputTextColor: '#1e293b',
  inputBorderRadius: 6,
})
```

## Estrutura de Stories

### Convencao de Nomes

```
src/
├── components/
│   └── ui/
│       ├── button.tsx
│       └── button.stories.tsx    # Story do componente
```

### Template de Story

```typescript
// button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './button'

const meta: Meta<typeof Button> = {
  title: 'UI/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link'],
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'icon'],
    },
  },
}

export default meta
type Story = StoryObj<typeof meta>

// Stories
export const Default: Story = {
  args: {
    children: 'Button',
    variant: 'default',
  },
}

export const Destructive: Story = {
  args: {
    children: 'Delete',
    variant: 'destructive',
  },
}

export const Outline: Story = {
  args: {
    children: 'Outline',
    variant: 'outline',
  },
}

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="default">Default</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
}

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
}

export const WithIcon: Story = {
  render: () => (
    <Button>
      <IconPlus className="mr-2 h-4 w-4" />
      Add Item
    </Button>
  ),
}

export const Loading: Story = {
  render: () => (
    <Button disabled>
      <IconLoader className="mr-2 h-4 w-4 animate-spin" />
      Loading...
    </Button>
  ),
}
```

### Story de Domain Component

```typescript
// unit-card.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { UnitCard } from './unit-card'

const meta: Meta<typeof UnitCard> = {
  title: 'Domain/UnitCard',
  component: UnitCard,
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof meta>

const mockUnit = {
  id: '123',
  code: 'UN-001',
  address: 'Rua das Flores, 123',
  area: 250,
  status: 'approved' as const,
  holderCount: 2,
}

export const Default: Story = {
  args: {
    unit: mockUnit,
  },
}

export const WithActions: Story = {
  args: {
    unit: mockUnit,
    onEdit: () => console.log('Edit'),
    onDelete: () => console.log('Delete'),
    onViewMap: () => console.log('View Map'),
  },
}

export const AllStatuses: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-4">
      <UnitCard unit={{ ...mockUnit, status: 'pending' }} />
      <UnitCard unit={{ ...mockUnit, status: 'in_progress' }} />
      <UnitCard unit={{ ...mockUnit, status: 'approved' }} />
      <UnitCard unit={{ ...mockUnit, status: 'rejected' }} />
    </div>
  ),
}
```

## Comandos

```bash
# Desenvolvimento
bun run storybook

# Build estatico
bun run build-storybook

# Testar acessibilidade
# (addon a11y mostra issues no painel)
```

## Deploy

O Storybook pode ser deployado no Vercel, Netlify ou GitHub Pages:

```bash
# Build
bun run build-storybook

# Output em storybook-static/
```
