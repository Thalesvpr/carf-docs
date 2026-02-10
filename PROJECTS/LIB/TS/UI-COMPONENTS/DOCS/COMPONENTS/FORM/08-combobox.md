---
type: leaf
status: review
updated: 2026-02-07
---

# Combobox

Componente de autocomplete web com busca e selecao de opcoes em popover.

## Props

Prop items array de opcoes disponiveis para selecao com label e value. Prop value valor selecionado atualmente controlado externamente. Prop onValueChange callback invocado com novo valor ao selecionar opcao. Prop onSearch callback invocado com texto digitado para busca assincrona. Prop placeholder texto guia exibido quando nenhum valor selecionado. Prop loading boolean exibe spinner durante busca assincrona. Prop emptyMessage texto exibido quando busca nao retorna resultados. Prop renderItem funcao opcional para customizar renderizacao de cada opcao.

## Composicao Interna

Usa Popover de Radix UI como container flutuante para lista de opcoes. Command de cmdk renderiza lista filtravel com busca integrada. Input trigger abre popover ao focar e filtra opcoes conforme digitacao. Padrao shadcn de composicao Popover + Command para consistencia com design system.

## Caso de Uso

Busca de holder por CPF no cadastro de unidades com debounce de busca. Selecao de comunidade por nome com autocomplete em formularios. Selecao de municipio com lista extensa filtrada por digitacao. Qualquer campo que combine input livre com selecao de lista.

## Estados

Estado idle exibe input com placeholder e chevron indicando natureza expansivel. Estado open exibe popover com lista de opcoes filtradas. Estado loading exibe spinner dentro do popover durante busca assincrona. Estado empty exibe emptyMessage quando filtro nao encontra resultados.

## Acessibilidade

Prop role combobox definido no input trigger automaticamente. Aria-expanded comunica estado de abertura do popover. Aria-activedescendant aponta para opcao focada via teclado. Navegacao por setas percorre opcoes, Enter seleciona, Escape fecha. Anuncio de resultados encontrados para leitores de tela.

## Estilizacao

Input trigger segue estilos do componente Input do design system. Popover posiciona abaixo do input com largura igual. Opcao focada via teclado destaca com bg-accent. Opcao selecionada exibe check icon a esquerda.
