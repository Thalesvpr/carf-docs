---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-177: Gerar Termo de Legitimacao

## Descricao

Sistema deve oferecer geracao automatizada de documento formal de Termo de Legitimacao Fundiaria atraves de template predefinido estruturado conforme exigencias legais da legislacao de regularizacao fundiaria. Mecanismo de preenchimento automatico extrai dados cadastrais do processo, informacoes dos titulares, caracteristicas da unidade territorial incluindo area e localizacao, e fundamentacao legal aplicavel, populando campos do template sem digitacao manual. Documento gerado em formato PDF com formatacao profissional incluindo cabecalho institucional, numeracao sequencial controlada, campos para assinaturas e codigo de verificacao para autenticacao posterior. PDF automaticamente vinculado ao processo e armazenado em bucket S3/MinIO com versionamento.

## Criterios de Aceitacao

1. Template predefinido conforme legislacao
2. Preenchimento automatico de dados do processo
3. Geracao em PDF com formatacao profissional
4. Numeracao sequencial controlada
5. Armazenamento versionado em bucket

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-172, RF-176
