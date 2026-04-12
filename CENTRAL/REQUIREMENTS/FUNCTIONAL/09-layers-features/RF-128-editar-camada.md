---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-128: Editar Camada

## Descricao

Sistema deve permitir edicao de configuracoes de camadas existentes para ajustar apresentacao e comportamento sem recriar camada e migrar dados. Interface de edicao permite modificar propriedades mantendo features associadas intactas. Atualizacoes possiveis incluem nome da camada, estilo visual (cores, espessuras, icones), e visibilidade padrao. Funcionalidade de reordenacao permite ajustar Z-index relativo entre camadas, afetando empilhamento no mapa. Alteracoes geram entradas no log de auditoria registrando usuario, timestamp e descricao das mudancas. Sistema valida que alteracoes nao quebrem integridade de features existentes, impedindo mudanca de tipo de geometria se ja existem features na camada.

## Criterios de Aceitacao

1. Edicao de nome, estilo e visibilidade
2. Reordenacao de Z-index entre camadas
3. Log de auditoria para alteracoes
4. Validacao de integridade de features
5. Features existentes preservadas

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-137
