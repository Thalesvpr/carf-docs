---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-069: Validar Sobreposicao de Unidades

## Descricao

Sistema deve detectar automaticamente sobreposicoes geometricas entre unidades ao salvar cadastro ou editar geometria. Validacao espacial utiliza operadores PostGIS (ST_Intersects, ST_Overlaps) com indices geometricos. Quando sobreposicao detectada, sistema apresenta alerta visual listando unidades conflitantes. Validacao nao bloqueia salvamento mas registra warning no log de auditoria, permitindo casos validos como edificacoes verticalizadas. Interface oferece visualizacao das unidades sobrepostas no mapa com area de intersecao destacada.

## Criterios de Aceitacao

1. Deteccao automatica via PostGIS
2. Alerta visual com unidades conflitantes
3. Validacao nao bloqueante com registro de warning
4. Visualizacao de intersecao no mapa
5. Suporte a sobreposicoes legitimas

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-066, RF-068
