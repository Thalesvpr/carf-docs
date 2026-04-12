---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-209: Ficha Tecnica de Unidade PDF

## Descricao

Sistema deve gerar automaticamente Ficha Tecnica completa de unidade territorial em formato PDF com layout profissional consolidando todas as informacoes relevantes: dados descritivos (codigo, endereco, area, tipo de ocupacao), informacoes de titulares (documentos, percentuais de propriedade), historico de aprovacoes e alteracoes. Ficha incorpora fotos associadas organizadas em grid com legendas de data e autor. Mapa de situacao estatico mostra localizacao precisa com geometria destacada sobre basemap, escala grafica e coordenadas geograficas. Codigo QR unico direciona para URL publica ou restrita com informacoes atualizadas, integrando documentacao fisica e digital. Conforme WORKFLOW-MESTRE, permite leitura de QR Code para protocolos.

## Criterios de Aceitacao

1. Consolidacao de dados cadastrais completos
2. Galeria de fotos com legendas
3. Mapa de situacao com escala e coordenadas
4. Codigo QR para URL de verificacao
5. Layout profissional institucional

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-102
