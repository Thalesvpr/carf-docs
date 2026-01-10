# Design Principles - @carf/ui

## Princípios de Design

### 1. Composition over Configuration

Preferir composição de subcomponentes ao invés de props booleanas excessivas. Exemplo: `<Card><CardHeader /><CardContent /></Card>` é melhor que `<Card hasHeader={true} hasFooter={false}>`. Isso permite flexibilidade máxima sem explosão de props.

### 2. Accessibility First

Todos os componentes têm ARIA completo implementado ANTES de serem adicionados à biblioteca. Acessibilidade não é uma feature opcional, é um requisito fundamental. Nenhum componente é merged sem passar em testes axe-core.

### 3. Mobile-First Responsive

Design para mobile primeiro, depois adapta para desktop com breakpoints Tailwind (sm: 640px, md: 768px, lg: 1024px, xl: 1280px). Garante experiência otimizada em todos os dispositivos.

### 4. Performance

- **Lazy loading** - Componentes pesados carregados on-demand
- **Code splitting** - Bundle separado por componente
- **React.memo** - Previne re-renders desnecessários em componentes pesados
- **Tree-shaking** - Importações individuais minimizam bundle size

### 5. Type Safety

- Uso de generics quando aplicável: `<DataTable<Unit>>` infere tipos da data
- Props 100% tipadas com TypeScript
- Erros de tipo em tempo de compilação
- Autocompletion completo em IDEs

### 6. Testability

- **Testing Library** - Testes focados em comportamento do usuário
- **Accessibility tests** - axe-core em todos os componentes
- **Snapshot tests** - Previne regressões visuais
- **Coverage mínimo** - 80% para merge

## Exemplo Prático

```tsx
// ❌ Configuration (evitar)
<Card
  hasHeader={true}
  hasFooter={true}
  headerSize="large"
  footerAlign="right"
>
  Content
</Card>

// ✅ Composition (preferir)
<Card>
  <CardHeader className="text-lg">
    Header
  </CardHeader>
  <CardContent>
    Content
  </CardContent>
  <CardFooter className="justify-end">
    <Button>Action</Button>
  </CardFooter>
</Card>
```

## Referências

- [Composition vs Configuration](https://www.joshwcomeau.com/react/demystifying-styled-components/)
- [Accessibility First Design](https://www.w3.org/WAI/fundamentals/accessibility-intro/)
- [Mobile-First Responsive Design](https://tailwindcss.com/docs/responsive-design)
