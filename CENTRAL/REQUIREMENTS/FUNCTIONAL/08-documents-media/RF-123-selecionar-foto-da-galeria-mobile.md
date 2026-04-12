---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-123: Selecionar Foto da Galeria Mobile

## Descricao

Aplicativo mobile REURBCAD deve permitir selecao de fotos existentes da galeria do dispositivo ao inves de capturar novas com camera. Funcionalidade acessa biblioteca de fotos atraves de APIs nativas iOS e Android. Sistema solicita permissoes de acesso a galeria conforme politicas de privacidade. Interface de selecao utiliza picker nativo permitindo navegacao por albuns e pastas do dispositivo com visualizacao de thumbnails. Suporte a selecao multipla permite escolher varias fotos simultaneamente via checkboxes ou gestos apropriados, facilitando upload em lote de documentacao fotografica. Apos selecao, sistema processa upload em lote imediatamente se ha conectividade ou enfileira para sincronizacao posterior se offline, mostrando progresso individual e indicando sucessos ou falhas.

## Criterios de Aceitacao

1. Acesso a galeria via picker nativo
2. Solicitacao de permissoes conforme plataforma
3. Navegacao por albuns com thumbnails
4. Selecao multipla de fotos
5. Upload em lote com indicacao de progresso

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-108, RF-122
