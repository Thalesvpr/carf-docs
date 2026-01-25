---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-167: Anexar Memorial Descritivo

## Descricao

Sistema deve permitir upload de documentos de memorial descritivo em formato PDF vinculados ao levantamento topografico, armazenando centralizadamente documentacao tecnica que descreve formalmente o perimetro levantado (coordenadas geodesicas, azimutes, distancias, vertices caracteristicos). Vinculacao entre memorial digital e levantamento georreferenciado estabelece rastreabilidade completa entre representacao grafica das features espaciais e descricao textual tecnico-juridica do imovel, atendendo requisitos para processos de regularizacao fundiaria e registro cartorario. Controle de versoes dos memoriais permite registrar atualizacoes e retificacoes com metadados (data, autor, justificativa) preservando historico completo. Download de arquivos PDF disponivel diretamente da interface.

## Criterios de Aceitacao

1. Upload de memorial descritivo em PDF
2. Vinculacao ao levantamento
3. Controle de versoes com metadados
4. Download direto da interface
5. Rastreabilidade tecnico-juridica

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-157, RF-102, RF-120
