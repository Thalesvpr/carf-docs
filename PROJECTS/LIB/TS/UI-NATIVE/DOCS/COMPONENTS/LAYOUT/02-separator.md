---
type: leaf
status: review
updated: 2026-02-07
---

# Separator

Componente de separacao visual nativo entre elementos de conteudo.

## Props

Prop orientation aceita horizontal ou vertical definindo direcao da linha separadora. Prop className permite extensao de estilos via NativeWind.

## Orientacao

Orientacao horizontal renderiza View com bg-border e h-px ocupando largura total do container pai. Orientacao vertical renderiza View com bg-border e w-px ocupando altura total do container pai. Padrao e horizontal quando orientation nao especificado.

## Uso

Separator horizontal divide secoes de conteudo empilhadas verticalmente. Separator vertical divide elementos lado a lado em layouts horizontais. Componente minimal sem logica complexa serve como utilitario visual puro.

## Acessibilidade

Role separator definido automaticamente para leitores de tela. Orientacao comunicada via accessibilityValue para contexto direcional. Componente decorativo nao recebe foco na navegacao.

## Estilizacao

Cor padrao bg-border segue tema do sistema para consistencia visual. ClassName prop permite customizacao de cor, margem e espessura. Dark mode ajusta cor automaticamente via dark:bg-border. Margem vertical my-2 ou horizontal mx-2 adicionada conforme contexto de uso.
