---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-122: Tirar Foto com Camera Mobile

## Descricao

Aplicativo mobile REURBCAD deve permitir captura de fotos diretamente atraves da camera nativa do dispositivo durante trabalho de campo. Funcionalidade acessa hardware de camera via APIs nativas iOS e Android. Sistema solicita permissoes de camera conforme politicas de privacidade de cada plataforma, mantendo autorizacao para usos futuros. Interface de captura utiliza componente nativo com controles familiares: foco automatico, flash, ajuste de exposicao e preview em tempo real. Apos captura, sistema oferece upload imediato se conectividade disponivel ou armazenamento offline local para sincronizacao posterior quando conexao restabelecida. App preserva metadados EXIF incluindo coordenadas GPS para geotagging automatico conforme WORKFLOW-MESTRE onde equipe de campo (Coordenador e Cadastrador) captura fotos geolocalizadas em campo.

## Criterios de Aceitacao

1. Captura via camera nativa do dispositivo
2. Solicitacao de permissoes conforme plataforma
3. Preview em tempo real com controles nativos
4. Upload imediato ou armazenamento offline
5. Preservacao de metadados EXIF e GPS

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-108, RF-110
