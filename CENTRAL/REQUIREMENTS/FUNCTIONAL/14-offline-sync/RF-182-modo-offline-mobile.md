---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-182: Modo Offline Mobile

## Descricao

Aplicativo mobile REURBCAD deve funcionar completamente offline permitindo coleta e gestao de dados cadastrais em campo sem conectividade com internet, requisito essencial para trabalho em comunidades remotas. Implementacao utiliza SQLite como banco de dados local atraves da biblioteca WatermelonDB que fornece camada de abstracao reativa e performatica, possibilitando armazenamento de milhares de registros de unidades, titulares, fotos e documentos diretamente no dispositivo. Todas as funcionalidades principais permanecem disponiveis offline incluindo criacao e edicao de unidades, cadastro de titulares, captura de fotos georreferenciadas, desenho de geometrias no mapa e preenchimento de formularios. Sistema exibe indicador visual permanente de status de conectividade (online/offline) na interface informando contexto atual de operacao. Conforme WORKFLOW-MESTRE, acesso aos dados so e liberado apos Analista publicar trabalho do tenant.

## Criterios de Aceitacao

1. Banco SQLite local via WatermelonDB
2. Todas funcionalidades principais offline
3. Indicador visual de status online/offline
4. Armazenamento de unidades, titulares, fotos
5. Acesso condicionado a publicacao pelo Analista

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-044, RF-102
