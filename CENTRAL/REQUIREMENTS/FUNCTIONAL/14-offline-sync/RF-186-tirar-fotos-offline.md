---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-186: Tirar Fotos Offline

## Descricao

Aplicativo mobile deve permitir captura de fotos atraves da camera do dispositivo sem conectividade, funcionalidade essencial para documentacao fotografica de unidades territoriais durante levantamentos em areas sem cobertura de rede. Camera funciona completamente offline utilizando recursos nativos, capturando imagens em resolucao configuravel que equilibra qualidade visual com tamanho de arquivo para otimizar armazenamento local e posterior transmissao. Imagens armazenadas localmente no sistema de arquivos com nomenclatura estruturada incluindo UUID da unidade associada e timestamp de captura. Metadados como coordenadas GPS, orientacao da camera e identificacao do usuario registrados no SQLite local estabelecendo vinculo com registro cadastral. Upload automatico durante sincronizacao quando conectividade restabelecida.

## Criterios de Aceitacao

1. Captura de fotos completamente offline
2. Resolucao configuravel
3. Metadados GPS e timestamp
4. Vinculacao automatica a unidade
5. Upload automatico na sincronizacao

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-102, RF-184
