---
type: leaf
status: approved
updated: 2026-01-24
---

# Elemento de Camada

Geometria individual dentro de uma camada vetorial. Representa ponto, linha ou poligono especifico com atributos descritivos.

Cada elemento e uma feature geografica unica. Poste de energia, trecho de tubulacao, area de risco delimitada. A camada agrupa elementos tematicamente relacionados.

## Geometria

Coordenadas que definem a forma espacial do elemento. Deve ser valida - poligono fechado sem auto-intersecao, linha com ao menos dois pontos.

## Propriedades

Atributos em formato chave-valor descrevem caracteristicas do elemento. Flexibilidade permite esquema livre onde cada camada define seus proprios campos.

## Rastreabilidade

Sistema registra quem criou e modificou cada elemento. Permite auditoria e responsabilizacao por alteracoes nos dados.

## Consultas Espaciais

Elementos podem ser buscados por proximidade ou contencao. Encontrar todos postes a menos de 100m de uma unidade. Verificar se unidade esta dentro de area de risco.
