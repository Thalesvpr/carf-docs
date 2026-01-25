---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
  - GEOAPI
---

# RF-049: Criar Unidade

## Descricao

Usuarios autorizados (ANALYST, FIELD_AGENT, MANAGER) podem criar novas unidades cadastrais. Formulario inclui todos campos obrigatorios definidos em RF-054 como codigo identificador unico, endereco completo, tipo de unidade, area construida e terreno. Desenho de geometria no mapa atraves de ferramentas interativas de digitalizacao com snap para vertices de unidades adjacentes e validacoes topologicas. Unidade criada com status inicial DRAFT permitindo edicoes antes de submeter para aprovacao.

## Criterios de Aceitacao

1. Formulario com campos obrigatorios conforme RF-054
2. Desenho de poligono no mapa com ferramentas interativas
3. Validacao de unicidade de codigo identificador
4. Status inicial DRAFT para novas unidades
5. Calculo automatico de area apos desenho

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-054, RF-066
