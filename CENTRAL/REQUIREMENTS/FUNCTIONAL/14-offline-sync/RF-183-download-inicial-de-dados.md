---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
  - GEOAPI
---

# RF-183: Download Inicial de Dados

## Descricao

Sistema deve permitir download unico e temporario do pacote de dados do tenant para dispositivo mobile antes de deslocamento a campo. Usuario seleciona tenant de interesse e baixa todos os dados associados incluindo ortofoto (online e/ou versao offline otimizada), poligonos georreferenciados, unidades territoriais cadastradas, titulares vinculados e configuracoes especificas. Conforme WORKFLOW-MESTRE, download so e habilitado apos Analista publicar trabalho do tenant no backend. Processo otimizado agrupa requisicoes em lotes e comprime dados transmitidos minimizando consumo de dados moveis. Barra de progresso exibe percentual concluido, registros transferidos e tempo estimado. Dados persistidos em SQLite ficam imediatamente disponiveis para acesso offline, permitindo inicio do trabalho de campo sem conectividade adicional.

## Criterios de Aceitacao

1. Download de pacote completo do tenant
2. Inclusao de ortofoto, poligonos e unidades
3. Condicionado a publicacao pelo Analista
4. Barra de progresso detalhada
5. Dados disponiveis imediatamente apos download

## Rastreabilidade

- Modulos: REURBCAD, GEOAPI
- Requisitos dependentes: RF-017, RF-182
