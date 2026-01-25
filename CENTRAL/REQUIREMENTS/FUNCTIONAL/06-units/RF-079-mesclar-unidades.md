---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-079: Mesclar Unidades

## Descricao

Sistema deve permitir que usuarios ADMIN mesclem multiplas unidades em uma unica unidade resultante, util para corrigir cadastros duplicados ou representar unificacao fisica. Interface permite selecao de unidades no mapa com destaque visual. Geometria resultante calculada via ST_Union das geometrias originais. Titulares de todas as unidades originais vinculados automaticamente a unidade mesclada. Unidades originais inativadas via soft delete mantendo rastreabilidade historica e permitindo eventual reversao.

## Criterios de Aceitacao

1. Selecao de multiplas unidades no mapa
2. Uniao geometrica via ST_Union
3. Preservacao de titulares vinculados
4. Soft delete das unidades originais
5. Restrito a perfil ADMIN

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-066
