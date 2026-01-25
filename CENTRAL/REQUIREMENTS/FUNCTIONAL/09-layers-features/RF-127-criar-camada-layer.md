---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-127: Criar Camada (Layer)

## Descricao

Sistema deve permitir criacao de camadas GIS personalizadas para organizar e visualizar conjuntos de dados geoespaciais, onde cada camada representa colecao logica de features geograficas do mesmo tipo compartilhando schema de atributos e estilo visual. Formulario de criacao permite definir nome descritivo e tipo de geometria (Point, LineString, Polygon) que features desta camada terao. Configuracao de estilo visual padrao inclui cor de preenchimento, cor de borda, espessura de linha, opacidade e icone para camadas de pontos. Campo de visibilidade padrao configura se camada deve estar visivel ou oculta ao carregar mapa inicialmente. Camadas criadas sao especificas do tenant e opcionalmente de comunidade especifica, conforme segregacao do WORKFLOW-MESTRE.

## Criterios de Aceitacao

1. Formulario com nome e tipo de geometria
2. Configuracao de estilo visual padrao
3. Campo de visibilidade inicial
4. Segregacao por tenant e comunidade
5. Validacao de tipo de geometria

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-017, RF-131
