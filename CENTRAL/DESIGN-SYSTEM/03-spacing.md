# Spacing

Sistema de espaçamento do CARF baseado em unidade de 8px, definindo escala para paddings, margins, gaps e dimensões consistentes em todos os componentes.

## Base

Unidade base: **8px**

Múltiplos de 8 garantem alinhamento consistente em grids e facilita cálculos mentais.

## Escala

| Token | Valor | Pixels | Uso |
|:------|:------|:-------|:----|
| `0` | 0 | 0px | Reset |
| `0.5` | 0.125rem | 2px | Micro ajustes |
| `1` | 0.25rem | 4px | Gaps mínimos, padding de ícones |
| `2` | 0.5rem | 8px | Padding interno pequeno |
| `3` | 0.75rem | 12px | Gaps de elementos inline |
| `4` | 1rem | 16px | Padding padrão, gaps de lista |
| `5` | 1.25rem | 20px | Espaçamento médio |
| `6` | 1.5rem | 24px | Padding de cards, gaps de seção |
| `8` | 2rem | 32px | Margens entre seções |
| `10` | 2.5rem | 40px | Espaçamento grande |
| `12` | 3rem | 48px | Padding de containers |
| `16` | 4rem | 64px | Margens de página |
| `20` | 5rem | 80px | Hero sections |
| `24` | 6rem | 96px | Espaçamento extra grande |

## CSS Variables

```css
:root {
  --space-unit: 8px;

  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
}
```

## Aplicação

### Componentes

| Componente | Padding | Gap |
|:-----------|:--------|:----|
| Button | 8px 16px | - |
| Input | 8px 12px | - |
| Card | 16px / 24px | - |
| Form fields | - | 16px |
| List items | - | 8px |
| Sections | - | 32px |

### Layout

| Elemento | Valor |
|:---------|:------|
| Container max-width | 1280px |
| Container padding | 16px (mobile), 24px (tablet), 32px (desktop) |
| Grid gap | 16px / 24px |
| Stack gap | 8px / 16px |

### Exemplos

```css
/* Card */
.card {
  padding: var(--space-6); /* 24px */
}

/* Form */
.form-group {
  margin-bottom: var(--space-4); /* 16px */
}

/* Button */
.button {
  padding: var(--space-2) var(--space-4); /* 8px 16px */
}

/* Section */
.section {
  margin-bottom: var(--space-8); /* 32px */
}
```

## Responsividade

Espaçamentos podem ser reduzidos em mobile:

| Contexto | Desktop | Mobile |
|:---------|:--------|:-------|
| Container padding | 32px | 16px |
| Section margin | 48px | 32px |
| Card padding | 24px | 16px |

## Boas Práticas

1. **Usar tokens** - Evitar valores arbitrários como 13px ou 27px
2. **Consistência vertical** - Manter ritmo vertical com line-height + margin
3. **Espaço em branco** - Não ter medo de espaço vazio; melhora legibilidade
4. **Mobile-first** - Começar com espaçamentos menores e aumentar

---

**Status do arquivo:** Draft
**Última atualização:** 2026-01-19
