---
type: leaf
status: review
updated: 2026-02-07
---

# Progress

Componente indicador de progresso nativo com variantes linear e circular.

## Props

Prop value numero de 0 a 100 representando percentual de conclusao. Prop variant aceita linear ou circular definindo formato visual. Prop size aceita sm, default ou lg controlando dimensoes. Prop indeterminate boolean ativa animacao continua sem valor definido. Prop label texto opcional exibido proximo ao indicador.

## Variante Linear

Barra horizontal com fundo bg-secondary e preenchimento bg-primary. Largura do preenchimento anima proporcionalmente ao value. Tamanho sm usa h-1, default usa h-2, lg usa h-3 para altura da barra. Cantos arredondados com rounded-full para acabamento visual.

## Variante Circular

Circulo SVG com stroke-dasharray calculado a partir do value. Rotacao inicia no topo com transform rotate -90 graus. Tamanho sm usa 24px, default usa 40px, lg usa 56px de diametro. Stroke width proporcional ao tamanho para visual equilibrado.

## Modo Indeterminado

Linear indeterminado anima barra de preenchimento deslizando da esquerda para direita em loop. Circular indeterminado anima rotacao continua do arco parcial. Prop value ignorada quando indeterminate true. Util para operacoes sem progresso mensuravel.

## Acessibilidade

Prop accessibilityRole definido como progressbar automaticamente. AccessibilityValue inclui min 0, max 100 e now igual ao value atual. Label lido antes do valor para contexto completo. Modo indeterminado anuncia estado de carregamento generico.

## Estilizacao

Classes NativeWind aplicam estilos responsivos ao container. Cor primaria do preenchimento segue tema do sistema. Dark mode ajusta cores de fundo e preenchimento. ClassName prop permite customizacao do container externo.
