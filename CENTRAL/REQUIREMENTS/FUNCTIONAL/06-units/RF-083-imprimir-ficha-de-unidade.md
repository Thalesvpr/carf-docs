---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-083: Imprimir Ficha de Unidade

## Descricao

Sistema deve gerar documento PDF com ficha tecnica completa de unidade habitacional. Layout profissional apresenta dados cadastrais organizados em secoes: identificacao, localizacao, caracteristicas, titulares, anexos. Ficha inclui codigo, endereco, tipo, area, comunidade, quadra, lote e lista de titulares com documento e tipo de relacionamento. Galeria de fotos renderizada com miniaturas por tipo. Mapa de localizacao mostra posicao geografica. QR code no rodape contem URL para visualizacao web, conforme WORKFLOW-MESTRE para leitura de QR Code em campo.

## Criterios de Aceitacao

1. Geracao de PDF formatado
2. Secoes organizadas de dados cadastrais
3. Galeria de fotos em miniaturas
4. Mapa de localizacao da unidade
5. QR code com URL da unidade

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-049, RF-063
