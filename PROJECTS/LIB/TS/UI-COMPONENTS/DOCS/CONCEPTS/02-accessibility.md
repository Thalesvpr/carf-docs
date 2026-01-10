# Accessibility - @carf/ui

## Padrões de Acessibilidade

Todos os componentes seguem WCAG 2.1 AA implementando ARIA labels (`aria-label`, `aria-describedby`), keyboard navigation (Tab, Enter, Escape, Arrow keys), focus management com `FocusTrap`, live regions (`aria-live`) para notificações dinâmicas, e color contrast ratios mínimos de 4.5:1 para texto normal via CSS variables testadas com axe-core em todos os componentes no Storybook, garantindo que UnitCard, Dialog, Select e outros sejam utilizáveis por usuários de screen readers (NVDA, JAWS) e teclado-only.

## Exemplos de Implementação

### ARIA Labels

```tsx
<Button aria-label="Deletar unidade UN-001">
  <TrashIcon />
</Button>
```

### Keyboard Navigation

```tsx
<Select onKeyDown={(e) => {
  if (e.key === 'Enter') openMenu()
  if (e.key === 'Escape') closeMenu()
  if (e.key === 'ArrowDown') selectNext()
  if (e.key === 'ArrowUp') selectPrevious()
}} />
```

### Focus Management

```tsx
<Dialog open={isOpen}>
  <FocusTrap>
    <DialogContent>
      <input ref={firstFocusableElement} />
    </DialogContent>
  </FocusTrap>
</Dialog>
```

## Testes de Acessibilidade

Todos os componentes são testados com:
- **axe-core** - Varredura automática de violações WCAG
- **jest-axe** - Testes unitários de acessibilidade
- **Screen reader testing** - Validação manual com NVDA/JAWS
- **Keyboard-only testing** - Navegação sem mouse

## Referências

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Radix UI Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility)
- [axe-core](https://github.com/dequelabs/axe-core)
