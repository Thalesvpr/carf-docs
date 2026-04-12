---
type: leaf
status: review
updated: 2026-02-07
---

# Criar Diagrama

Guia para criar diagramas usando sintaxe Mermaid em documentos Markdown.

## Visao Geral

Mermaid permite criar diagramas a partir de texto renderizado como SVG no build. Preferir Mermaid quando possivel pois texto e pesquisavel, versionavel e facilmente atualizavel comparado a imagens. Plugin Astro processa durante build convertendo para SVG inline sem JavaScript client-side. Tema segue configuracao global em astro.config.mjs aplicando cores do design system CARF com dark mode automatico. Para prototipar diagramas antes de incluir no documento, usar Mermaid Live Editor em mermaid.live.

## Tipos de Diagrama

| Tipo | Declaracao Inicial | Uso Principal |
|---|---|---|
| Flowchart | graph TD ou graph LR | Fluxos de processo e decisao |
| Sequence Diagram | sequenceDiagram | Interacoes entre componentes |
| ER Diagram | erDiagram | Modelo de dados e relacionamentos |
| State Diagram | stateDiagram-v2 | Estados e transicoes de entidades |
| Gantt Chart | gantt | Cronogramas de projeto |

## Sintaxe de Flowchart

Para criar um fluxograma, iniciar com graph seguido da direcao. Nos sao definidos por identificador seguido de label entre colchetes para retangulo ou entre parenteses para arredondado. Conexoes entre nos usam setas com texto opcional entre pipes. Nos de decisao usam chaves para forma de losango.

| Sintaxe de Direcao | Significado |
|---|---|
| graph TD | Cima para baixo (top-down) |
| graph TB | Mesmo que TD |
| graph BT | Baixo para cima |
| graph LR | Esquerda para direita |
| graph RL | Direita para esquerda |

## Formas de Nos

| Sintaxe | Forma Resultante |
|---|---|
| A[texto] | Retangulo |
| B(texto) | Retangulo arredondado |
| C([texto]) | Estadio |
| D[[texto]] | Subrotina |
| E[(texto)] | Cilindro (banco de dados) |
| F((texto)) | Circulo |
| G>texto] | Flag |
| H{texto} | Losango (decisao) |
| I{{texto}} | Hexagono |

## Sequence Diagram

Para diagramas de sequencia, declarar participantes com participant seguido de alias. Mensagens entre participantes usam setas: seta com dois hifens e maior para sincrona, seta tracejada com dois hifens e maior para resposta. Util para documentar fluxos de autenticacao e comunicacao entre servicos.

## ER e State Diagram

Para diagramas ER, declarar entidades com atributos tipados e relacionamentos usando notacao de cardinalidade com pipes e chaves. Para diagramas de estado, declarar transicoes com setas entre estados e labels apos dois pontos descrevendo a acao que causa a transicao. Estado inicial representado por [*].
