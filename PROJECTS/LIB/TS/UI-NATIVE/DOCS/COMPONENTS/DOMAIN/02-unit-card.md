---
type: leaf
status: review
updated: 2026-01-24
---

# UnitCard

Componente que exibe resumo de unidade habitacional com dados formatados.

## Props

Prop unit recebe objeto Unit de @carf/tscore/types. Prop onPress callback executado ao tocar no card. Prop variant aceita default ou compact controlando densidade. Prop showStatus boolean controla exibicao de StatusBadge.

## Dados Exibidos

Codigo da unidade exibido como titulo principal em negrito. Endereco formatado com rua, numero e bairro. Status renderizado via StatusBadge no canto superior. Area exibida em metros quadrados quando disponivel.

## Formatacao

Endereco concatena campos com separadores apropriados. Campos nulos omitidos graciosamente. Area formatada com duas casas decimais e unidade m2. Data de atualizacao em formato relativo como ha 2 dias.

## Variantes

Variante default exibe informacoes completas com espacamento generoso. Variante compact reduz padding e oculta dados secundarios. Compact ideal para listas longas. Default para selecao e detalhes.

## Interacao

Pressable wrapper permite navegacao ao tocar. Visual feedback via opacity ou scale ao pressionar. OnPress tipicamente navega para tela de detalhes. Long press opcional para menu contextual.

## Acessibilidade

AccessibilityLabel concatena informacoes principais. AccessibilityRole button quando onPress fornecido. AccessibilityHint descreve acao de toque. Status anunciado como parte do label.
