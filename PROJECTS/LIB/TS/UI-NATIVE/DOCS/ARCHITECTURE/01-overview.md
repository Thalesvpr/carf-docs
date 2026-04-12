---
type: leaf
status: review
updated: 2026-01-24
---

# Overview da Arquitetura

Visao geral da arquitetura da biblioteca @carf/ui-native baseada em react-native-reusables com NativeWind.

## Pilares Tecnologicos

Tres tecnologias fundamentam a biblioteca. React-native-reusables segue filosofia shadcn de componentes copiados ao inves de instalados como dependencia. NativeWind compila classes Tailwind para StyleSheet nativo de React Native. Rn-primitives fornece primitivos acessiveis equivalentes ao Radix UI para web.

## Organizacao de Componentes

Componentes dividem-se em duas categorias. Primitivos sao elementos genericos como Button, Input, Checkbox e Dialog usados em qualquer contexto. Componentes de dominio sao especificos do CARF como StatusBadge, UnitCard e HolderCard recebendo dados tipados do tscore.

## Sistema de Temas

NativeWind suporta dark mode via classe dark: em classes Tailwind. Arquivo tailwind.config.js define tema com cores primarias, backgrounds e bordas. Componentes usam variaveis CSS customizadas para cores permitindo customizacao por tenant.

## Acessibilidade

Rn-primitives implementa gerenciamento de foco, navegacao por teclado e anuncios para leitores de tela. Componentes incluem props accessibilityLabel e accessibilityRole. Contrastes seguem WCAG 2.1 AA com ratio minimo 4.5:1 para texto.

## Tipagem

Componentes exportam interfaces de props estendendo tipos base de React Native. Componentes de dominio importam tipos do @carf/tscore garantindo consistencia com backend. Props obrigatorias e opcionais documentadas via TypeScript.
