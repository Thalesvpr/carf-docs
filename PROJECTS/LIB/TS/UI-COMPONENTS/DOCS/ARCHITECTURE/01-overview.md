---
status: approved
updated: 2026-01-20
---

# Overview da Arquitetura - @carf/ui

## Nomenclatura

**Nome oficial do pacote npm:** `@carf/ui`

A pasta no repositorio chama-se `UI-COMPONENTS` por convencao de organizacao, mas o pacote publicado e importado e `@carf/ui`.

## Visao Geral

@carf/ui e uma biblioteca de componentes React baseada em **[shadcn/ui](https://ui.shadcn.com/)** e **[Tailwind CSS](https://tailwindcss.com/)**, fornecendo componentes reutilizaveis para GEOWEB, ADMIN e outras aplicacoes web CARF com design consistente, acessibilidade WCAG 2.1 AA e performance otimizada. A biblioteca exporta dois tipos de componentes: (1) **Componentes Genericos** - customizacoes de shadcn/ui (Button, Input, Dialog, Table, Select) com tema CARF, e (2) **Componentes de Dominio** - especificos do REURB (UnitCard, HolderCard, CommunityCard, StatusBadge) que encapsulam logica de apresentacao de entidades.

## Modelo de Dependencias

```
@carf/ui
├── @radix-ui/* (peer dependency - primitivos acessiveis)
├── class-variance-authority (dependency - variants)
├── clsx + tailwind-merge (dependency - cn utility)
└── tailwindcss (peer dependency - estilos)

@carf/tscore (OPCIONAL - nao e dependencia direta)
└── Types compativeis podem ser passados para domain components
```

**Importante:** @carf/ui **NAO depende** de @carf/geoapi-client. Domain components (UnitCard, HolderCard, etc) sao "dumb components" que recebem dados via props. A aplicacao consumidora e responsavel por buscar dados usando geoapi-client ou outra fonte e passar para os componentes.

## Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────┐
│                    Aplicacoes Consumidoras                 │
│                                                            │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│   │ GEOWEB   │  │  ADMIN   │  │ Keycloak │  │ WebDocs  │  │
│   │(Next.js) │  │(Next.js) │  │ (Theme)  │  │ (Astro)  │  │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
└────────┼─────────────┼─────────────┼─────────────┼────────┘
         │             │             │             │
         └─────────────┴──────┬──────┴─────────────┘
                              │
               import { Button, UnitCard } from '@carf/ui'
                              │
                   ┌──────────▼──────────┐
                   │      @carf/ui       │
                   │   (Component Lib)   │
                   └──────────┬──────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
┌────────▼─────────┐ ┌────────▼────────┐ ┌────────▼─────────┐
│   shadcn/ui      │ │ Domain          │ │ Utils/Hooks      │
│   (Generics)     │ │ Components      │ │                  │
│   - Button       │ │ - UnitCard      │ │ - cn()           │
│   - Dialog       │ │ - HolderCard    │ │ - carfColors     │
│   - Table        │ │ - CommunityCard │ │ - useTheme       │
│   - Input        │ │ - StatusBadge   │ │ - useMediaQuery  │
└────────┬─────────┘ └─────────────────┘ └──────────────────┘
         │
┌────────▼─────────┐
│    Radix UI      │  Accessible headless primitives
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Tailwind CSS    │  Utility-first styling
└──────────────────┘
```

**Nota:** @carf/tscore types sao compatíveis com domain components mas NAO sao dependencia obrigatoria. Domain components definem seus proprios types internamente.

## Componentes Principais

### 1. Componentes shadcn/ui Customizados

Componentes genéricos reutilizáveis com tema CARF aplicado:

- **Button** - Botão com variantes `default`, `destructive`, `outline`, `ghost`, `link`
- **Input** - Campo de texto com suporte a máscaras (CPF, CNPJ, phone)
- **Dialog** - Modal acessível com overlay e animações
- **Table** - Tabela responsiva com sorting, pagination, filtering
- **Select** - Dropdown acessível com keyboard navigation
- **Card** - Container para conteúdo agrupado
- **Badge** - Label colorido para status
- **Tooltip** - Hint contextual ao hover
- **Accordion** - Conteúdo expansível
- **Tabs** - Navegação em abas

### 2. Componentes de Dominio CARF

Componentes especificos do sistema REURB, implementados como "dumb components" que recebem dados via props:

#### **UnitCard**

Exibe informacoes de uma Unidade Habitacional:

```tsx
<UnitCard
  unit={{ id: '1', code: 'UN-001', address: 'Rua das Flores', status: 'approved' }}
  onEdit={() => navigate(`/units/${unit.id}/edit`)}
  onDelete={() => confirmDelete(unit.id)}
  onViewMap={() => showMapModal(unit)}
/>
```

**Renderiza:** Codigo, endereco, area, status badge, holder count.

#### **HolderCard**

Exibe informacoes de um Posseiro:

```tsx
<HolderCard
  holder={{ id: '1', name: 'Maria Silva', cpf: '12345678901' }}
  onEdit={() => navigate(`/holders/${holder.id}/edit`)}
/>
```

**Renderiza:** Nome, CPF/CNPJ mascarado, contato, unidades count.

#### **CommunityCard**

Exibe informacoes de uma Comunidade:

```tsx
<CommunityCard
  community={{ id: '1', name: 'Vila das Flores', status: 'active' }}
  onEdit={() => navigate(`/communities/${community.id}/edit`)}
  onSelect={() => setCurrentCommunity(community)}
/>
```

#### **StatusBadge**

Badge colorido para status de processos REURB:

```tsx
<StatusBadge status="pending" />    // Amarelo - Pendente
<StatusBadge status="in_progress"/> // Azul - Em Andamento
<StatusBadge status="approved" />   // Verde - Aprovado
<StatusBadge status="rejected" />   // Vermelho - Rejeitado
```

**Outros status:** active, inactive, draft, archived.

## Padrões de Composição

### Compound Components

Componentes complexos seguem padrão de composição:

```tsx
<Card>
  <CardHeader>
    <CardTitle>Unidade UN-001</CardTitle>
    <CardDescription>Rua das Flores, 123</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Área: 250m²</p>
  </CardContent>
  <CardFooter>
    <Button>Editar</Button>
  </CardFooter>
</Card>
```

### Render Props

Para flexibilidade máxima:

```tsx
<DataTable
  data={units}
  columns={columns}
  renderRow={(unit) => <CustomUnitRow unit={unit} />}
/>
```

### Custom Hooks

Lógica reutilizável via hooks:

```tsx
function UnitForm() {
  const { control, errors } = useUnitForm()
  const { validate } = useUnitValidation()

  return <form>...</form>
}
```

## Princípios de Design

1. **Acessibilidade (WCAG 2.1 AA):** Todos os componentes têm ARIA labels, keyboard navigation, focus management.
2. **Responsividade:** Mobile-first design, breakpoints Tailwind (sm, md, lg, xl).
3. **Performance:** React.memo, lazy loading, code splitting por componente.
4. **Type Safety:** 100% TypeScript, props tipadas, generics quando aplicável.
5. **Testabilidade:** Testing Library, snapshots, acessibilidade tests (axe).
6. **Documentação:** Storybook com todos os estados e variantes.

## Stack Tecnológico

| Tecnologia | Versão | Justificativa |
|------------|--------|---------------|
| React | 18.2 | Server Components ready |
| TypeScript | 5.3 | Type safety |
| Tailwind CSS | 3.4 | Utility-first styling |
| shadcn/ui | latest | Customizable components |
| Radix UI | latest | Accessible primitives |
| Leaflet | 1.9 | Maps (MapView) |
| React Hook Form | 7.49 | Forms com performance |
| Zod | 3.22 | Validação runtime |

## Decisões Técnicas

### Por que shadcn/ui ao invés de Material-UI?

- **Customização total:** shadcn/ui copia componentes para nosso código, permitindo edição completa.
- **Bundle size menor:** Importa apenas o necessário.
- **Tailwind integration:** CSS utility-first é mais produtivo que CSS-in-JS.
- **Server Components:** Compatível com Next.js 13+ App Router.

### Por que Radix UI como base?

[Radix UI](https://www.radix-ui.com/) fornece primitivos acessíveis que servem como base para shadcn/ui, garantindo **Acessibilidade** WAI-ARIA compliant out of the box, arquitetura **Headless** com separação entre lógica e apresentação, e **Composabilidade** que permite criar variantes facilmente sem sacrificar usabilidade ou performance.
