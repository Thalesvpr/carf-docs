---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-168: Validar Fechamento de Poligonal

## Descricao

Sistema deve implementar algoritmos para calculo de erro de fechamento de poligonais topograficas, verificando precisao do levantamento atraves de analise da discrepancia entre coordenadas inicial e final quando percorridos todos os vertices da figura fechada. Calculo abrange erro linear (distancia euclidiana entre ponto de partida teorico e ponto de chegada efetivo) e erro angular (diferenca entre soma dos angulos internos medidos e valor teorico esperado para o poligono). Sistema gera relatorio detalhado de precisao com valores absolutos e relativos de erro, comparacao com tolerancias da NBR 13133 e classificacao de qualidade do levantamento. Essencial para garantir confiabilidade dos limites territoriais cadastrados e conformidade com requisitos tecnicos de cartorios para georreferenciamento.

## Criterios de Aceitacao

1. Calculo de erro linear
2. Calculo de erro angular
3. Relatorio de precisao detalhado
4. Comparacao com tolerancias NBR 13133
5. Classificacao de qualidade

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-160, RF-157
