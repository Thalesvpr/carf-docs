# Terminology - @carf/ui

## Glossário de Termos

### Atomic Design

- **Atom** - Componente indivisível (Button, Input, Badge). Menor unidade de UI.
- **Molecule** - Combinação de atoms (FormField = Label + Input + ErrorMessage). Grupo funcional simples.
- **Organism** - Grupo de molecules (LoginForm, UnitCard). Seção completa de interface.

### Componentes React

- **Compound Component** - Componente com subcomponentes relacionados (Dialog.Header, Card.Footer). Permite composição flexível.
- **Controlled Component** - State gerenciado externamente via props (`value` e `onChange`).
- **Uncontrolled Component** - State interno com ref access (`defaultValue` e `ref`).
- **Render Prop** - Função como children para customização (`renderRow={(item) => <Custom />}`).

### Design Tokens

- **Design Token** - CSS variable que define tema (`--primary`, `--radius`, `--font-sans`).
- **Theme** - Conjunto de design tokens definindo visual da aplicação.
- **CSS Variable** - Valor reutilizável em CSS (`var(--primary)`).

### shadcn/ui

- **Primitive** - Componente base do Radix UI sem estilos.
- **Variant** - Versão alternativa de componente (Button: `default`, `outline`, `ghost`).
- **Slot** - Placeholder para children em compound components.

## Termos do Domínio CARF

- **UnitCard** - Componente que exibe informações de uma Unidade (código, endereço, área).
- **HolderCard** - Componente que exibe informações de um Posseiro (nome, CPF, contato).
- **MapView** - Componente de mapa geográfico com Leaflet.
- **LegitimationStatusBadge** - Badge colorido para status de legitimação (PENDING, APPROVED, REJECTED).

## Referências

- [Atomic Design - Brad Frost](https://bradfrost.com/blog/post/atomic-web-design/)
- [React Glossary](https://react.dev/learn/glossary)
- [shadcn/ui Docs](https://ui.shadcn.com/docs)
