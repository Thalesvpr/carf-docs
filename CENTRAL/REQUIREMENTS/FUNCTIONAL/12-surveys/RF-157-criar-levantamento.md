---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
  - REURBCAD
---

# RF-157: Criar Levantamento

## Descricao

Sistema deve permitir criacao de registros de levantamento topografico documentando trabalhos de campo e medicoes realizadas. Formulario de criacao com campos para data de realizacao, responsavel tecnico (para rastreabilidade), e equipamento utilizado (estacao total, GPS RTK, drone) documentando metodologia e precisao. Vinculacao a comunidade ou unidade territorial estabelece escopo geografico e contexto administrativo. Suporte a upload de arquivo bruto (.raw, .txt, .csv ou formatos proprietarios) armazenado em object storage vinculado ao registro. Metadados e arquivo validados durante criacao e persistidos no banco conforme segregacao por tenant do WORKFLOW-MESTRE.

## Criterios de Aceitacao

1. Formulario com data, responsavel e equipamento
2. Vinculacao a comunidade ou unidade
3. Upload de arquivo bruto de dados
4. Armazenamento em object storage
5. Validacao de metadados

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI, REURBCAD
- Requisitos dependentes: RF-017, RF-102
