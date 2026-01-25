---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-078: Clonar Unidade

## Descricao

Sistema deve permitir clonagem de unidades habitacionais criando copia com todos os campos alfanumericos e relacionamentos exceto codigo identificador. Geometria clonada deslocada automaticamente 5 metros em direcao nordeste evitando sobreposicao exata. Funcionalidade gera novo codigo unico automaticamente seguindo padrao do tenant. Clone herda tipo, comunidade, quadra, lote e campos customizados, mas campos de auditoria refletem criacao como novo registro. Otimiza cadastramento de edificacoes similares ou geminadas.

## Criterios de Aceitacao

1. Copia de todos campos exceto codigo
2. Deslocamento automatico da geometria
3. Geracao de codigo unico
4. Heranca de relacionamentos
5. Novos campos de auditoria

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-076
