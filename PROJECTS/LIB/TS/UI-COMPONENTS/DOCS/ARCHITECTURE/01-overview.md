# Overview da Arquitetura - @carf/ui

## Visão Geral

@carf/ui é uma biblioteca de componentes React construída em **Atomic Design**, **[shadcn/ui](https://ui.shadcn.com/)** e **[Tailwind CSS](https://tailwindcss.com/)**, fornecendo componentes reutilizáveis para GEOWEB e ADMIN com design consistente, acessibilidade WCAG 2.1 AA e performance otimizada seguindo padrões documentados em . A biblioteca exporta dois tipos de componentes: (1) **Componentes Genéricos** - customizações de shadcn/ui (Button, Input, Dialog, Table, Select) com tema CARF, e (2) **Componentes de Domínio** - específicos do REURB (UnitCard, HolderCard, MapView, CommunityList, LegitimationStatusBadge) que encapsulam lógica de apresentação de entidades do sistema, consumindo types de `@carf/tscore` e podendo integrar com `@carf/geoapi-client` para data fetching.

## Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────┐
│                    Aplicações Consumidoras                 │
│                                                            │
│        ┌──────────────┐           ┌──────────────┐        │
│        │   GEOWEB     │           │    ADMIN     │        │
│        │   (Next.js)  │           │   (Next.js)  │        │
│        └──────┬───────┘           └──────┬───────┘        │
│               │                          │                 │
└───────────────┼──────────────────────────┼─────────────────┘
                │                          │
                └──────────┬───────────────┘
                           │ import { Button, UnitCard } from '@carf/ui'
                ┌──────────▼──────────┐
                │     @carf/ui        │
                │  (Component Lib)    │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐ ┌──────▼──────┐ ┌─────────▼────────┐
│  shadcn/ui     │ │ Domain      │ │   @carf/tscore   │
│  (Primitives)  │ │ Components  │ │   (Types)        │
│  - Button      │ │ - UnitCard  │ │   - Unit         │
│  - Dialog      │ │ - HolderCard│ │   - Holder       │
│  - Input       │ │ - MapView   │ │   - Community    │
└────────────────┘ └─────────────┘ └──────────────────┘
        │                  │
        └──────────┬───────┘
                   │
        ┌──────────▼──────────┐
        │    Radix UI         │ Accessible primitives
        │    (Headless UI)    │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Tailwind CSS      │ Styling
        │   (Utility-first)   │
        └─────────────────────┘
```

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

### 2. Componentes de Domínio CARF

Componentes específicos do sistema REURB:

#### **UnitCard**

Exibe informações de uma Unidade (Unit):

```tsx
<UnitCard
  unit={unit}  // type Unit from @carf/tscore
  onEdit={() => navigate(`/units/${unit.id}/edit`)}
  onDelete={() => confirmDelete(unit.id)}
  onViewMap={() => showMapModal(unit.geometry)}
/>
```

**Renderiza:** Código, endereço, área, status badge, holder count, mapa thumbnail.

#### **HolderCard**

Exibe informações de um Posseiro (Holder):

```tsx
<HolderCard
  holder={holder}  // type Holder from @carf/tscore
  showUnits={true}
  onEdit={() => navigate(`/holders/${holder.id}/edit`)}
/>
```

**Renderiza:** Nome, CPF/CNPJ mascarado, contato, unidades associadas.

#### **MapView**

Componente de mapa geográfico com Leaflet:

```tsx
<MapView
  center={[-23.5505, -46.6333]}
  zoom={15}
  units={units}
  onUnitClick={(unit) => navigate(`/units/${unit.id}`)}
  editable={true}
/>
```

**Features:** Exibe polígonos de unidades, markers, clustering, draw tools.

#### **CommunityList**

Lista de comunidades com filtros:

```tsx
<CommunityList
  communities={communities}
  onSelect={(community) => setCurrent(community)}
  filter={{ status: 'ACTIVE' }}
  sortBy="name"
/>
```

#### **LegitimationStatusBadge**

Badge colorido para status de legitimação:

```tsx
<LegitimationStatusBadge status={LegitimationStatus.APPROVED} />
```

**Cores:** PENDING (yellow), IN_PROGRESS (blue), APPROVED (green), REJECTED (red).

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

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (10) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.
