---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-120: Versionamento de Documentos

## Descricao

Sistema deve manter historico completo de versoes de documentos onde re-upload cria nova versao ao inves de sobrescrever. Versoes antigas preservadas conforme politica de retencao, armazenadas como objetos separados no S3/MinIO com referencias no banco. Cada versao com metadados proprios: numero sequencial, timestamp, usuario e comentario opcional. Funcionalidade de restauracao permite reverter para versao anterior selecionada. Interface exibe lista de versoes ordenada com opcoes de visualizar, baixar ou restaurar.

## Criterios de Aceitacao

1. Nova versao ao re-upload (nao sobrescreve)
2. Versoes antigas preservadas
3. Metadados por versao (numero, timestamp, usuario)
4. Funcionalidade de restauracao
5. Lista de versoes com acoes

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-102, RF-116
