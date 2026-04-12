---
type: leaf
status: review
updated: 2026-01-24
---

# Acessibilidade

Praticas de acessibilidade mobile implementadas na biblioteca @carf/ui-native.

## Leitores de Tela

Todos componentes incluem prop accessibilityLabel com descricao textual. Prop accessibilityRole define semantica como button, checkbox ou heading. VoiceOver em iOS e TalkBack em Android anunciam corretamente. Componentes interativos indicam estado via accessibilityState.

## Gerenciamento de Foco

Dialog move foco para primeiro elemento interativo ao abrir. Foco retorna para elemento trigger ao fechar. Trap de foco impede navegacao para fora de modais. Tab order segue ordem visual dos elementos.

## Contraste de Cores

Cores seguem WCAG 2.1 AA com ratio minimo 4.5:1 para texto normal. Texto grande pode ter ratio 3:1. Dark mode mantem mesmos ratios com cores invertidas. Ferramenta de verificacao valida contraste em design system.

## Touch Targets

Areas tocaveis tem minimo 44x44 pontos conforme guidelines iOS e Android. Espacamento entre elementos interativos previne toques acidentais. Estados de press fornecem feedback visual imediato.

## Reducao de Movimento

Usuarios com prefers-reduced-motion ativo recebem animacoes simplificadas. Transicoes mantém feedback funcional sem movimento excessivo. Animacoes decorativas sao desabilitadas completamente.

## Testes

Testar com VoiceOver em iOS e TalkBack em Android regularmente. Navegar apenas com gestos de acessibilidade. Validar que todas acoes sao possíveis sem visao. Verificar anuncios de estado em componentes dinamicos.
