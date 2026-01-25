---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-169: Integracao com Estacao Total

## Descricao

Sistema deve importar dados de estacoes totais atraves de parsers especializados que interpretam formatos proprietarios dos principais fabricantes (Leica, Topcon, Trimble, South), reconhecendo estruturas especificas de codificacao de medicoes angulares e lineares. Processo de importacao extrai automaticamente coordenadas tridimensionais calculadas pelo software embarcado, alem de atributos complementares (codigos de ponto, descricoes de features, timestamps de coleta), transformando dados brutos em informacoes estruturadas compativeis com o modelo de dados geoespacial. Apos extracao e validacao, sistema cria features geograficas classificando-as automaticamente conforme codigos padronizados e estabelecendo relacionamentos topologicos entre vertices de poligonais e elementos cadastrais. Elimina necessidade de conversoes manuais ou software intermediario.

## Criterios de Aceitacao

1. Parsers para Leica, Topcon, Trimble, South
2. Extracao de coordenadas e metadados
3. Classificacao automatica por codigos
4. Criacao de features georreferenciadas
5. Rastreabilidade desde medicao original

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-160, RF-157
