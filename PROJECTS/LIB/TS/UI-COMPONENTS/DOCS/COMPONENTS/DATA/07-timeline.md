---
type: leaf
status: review
updated: 2026-02-07
---

# Timeline

Componente de linha do tempo vertical para exibicao de historico de eventos.

## Props

Prop items array de objetos com date, title, description, icon opcional e variant opcional definindo cada evento. Prop orientation aceita vertical como direcao de exibicao da timeline.

## Variantes de Item

Variante default exibe indicador cinza para eventos neutros sem destaque. Variante success exibe indicador verde para eventos positivos como aprovacoes. Variante warning exibe indicador amarelo para eventos que requerem atencao. Variante error exibe indicador vermelho para eventos negativos como rejeicoes.

## Caso de Uso

Historico de legitimacao fundiaria mostrando cada etapa do processo com datas. Audit log de alteracoes em unidades e cadastros com usuario e acao. Historico de sincronizacao exibindo eventos de upload e download. Rastreamento de status de processos administrativos.

## Estrutura Visual

Linha vertical conecta indicadores circulares de cada evento. Indicador circular posicionado a esquerda com linha conectora abaixo. Titulo e data exibidos a direita do indicador na mesma linha. Descricao exibida abaixo do titulo com cor mutada para hierarquia visual.

## Icones

Prop icon opcional substitui indicador padrao por icone customizado. Icones de Lucide React para consistencia com design system. Icone dimensionado proporcionalmente ao indicador circular. Ausencia de icone renderiza circulo solido com cor da variante.

## Acessibilidade

Lista recebe role list para contexto semantico de sequencia. Cada item recebe role listitem com aria-label combinando data e titulo. Datas formatadas em formato legivel para leitores de tela. Variante comunicada via aria-label com descricao do tipo de evento.

## Estilizacao

Container vertical com relative para posicionamento da linha conectora. Indicadores usam w-3 h-3 rounded-full com cor da variante. Linha conectora usa w-px bg-border com posicao absoluta. Items usam pl-6 para espacamento apos indicador.
