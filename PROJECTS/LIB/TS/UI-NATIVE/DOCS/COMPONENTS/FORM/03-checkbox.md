---
type: leaf
status: review
updated: 2026-01-24
---

# Checkbox

Componente de selecao booleana com visual customizado e acessibilidade.

## Props

Prop checked controla estado em modo controlado. Prop onCheckedChange recebe callback com novo valor booleano. Prop disabled impede interacao. Prop label exibe texto descritivo ao lado do checkbox.

## Estados

Estado unchecked exibe caixa vazia com borda. Estado checked exibe caixa preenchida com icone de check. Estado indeterminate exibe caixa com traco horizontal. Estado disabled reduz opacidade em qualquer estado.

## Acessibilidade

Usa rn-primitives Checkbox para semantica correta. AccessibilityRole definido como checkbox automaticamente. AccessibilityState comunica checked e disabled. Label associado via accessibilityLabelledBy.

## Integracao com Formularios

Em react-hook-form usar Controller para gerenciar estado. Value boolean mapeia diretamente para checked prop. Erros de validacao exibidos via mensagem associada. Submit inclui valor no objeto de dados.

## Estilizacao

Caixa base usa borda rounded com tamanho configuravel. Estado checked usa bg-primary com icone branco. Animacao suave transiciona entre estados. Dark mode ajusta cores mantendo contraste.

## Grupo de Checkboxes

Para multipla selecao, renderizar array de Checkbox. Cada item com value unico e checked individual. Handler consolida valores selecionados em array. Label de grupo usa accessibilityRole radiogroup.
