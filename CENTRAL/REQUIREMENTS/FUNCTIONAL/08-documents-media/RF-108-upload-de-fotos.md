---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - REURBCAD
  - GEOAPI
---

# RF-108: Upload de Fotos

## Descricao

Sistema deve permitir upload de fotos em formatos JPG, PNG e HEIC garantindo compatibilidade com diferentes dispositivos e cameras. Tamanho maximo 20MB por arquivo validado em frontend e backend. Apos upload, sistema gera automaticamente miniatura para otimizar exibicao em galerias. Validacao inclui integridade do arquivo e verificacao de tipo MIME real. Feedback visual de progresso para uploads maiores. Conforme WORKFLOW-MESTRE, Agente de Campo captura fotos via REURBCAD em campo.

## Criterios de Aceitacao

1. Formatos: JPG, PNG, HEIC
2. Limite de 20MB por arquivo
3. Geracao automatica de miniatura
4. Validacao de tipo MIME real
5. Feedback de progresso de upload

## Rastreabilidade

- Modulos: GEOWEB, REURBCAD, GEOAPI
- Requisitos dependentes: RF-109, RF-110, RF-115, RF-116
