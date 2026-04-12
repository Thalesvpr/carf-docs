---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-133: Editar Feature

## Descricao

Sistema deve permitir edicao de geometria e atributos de features existentes para correcao e atualizacao de dados espaciais e descritivos, com modos separados para edicao geometrica e alfanumerica. Para edicao de geometria, modo de edicao de vertices permite selecionar feature e manipular pontos de controle apresentados como handles arrastaveis, podendo mover vertices existentes, adicionar novos no meio de segmentos ou remover via interacao apropriada. Para edicao de atributos, formulario populado com valores atuais permite modificacao de campos individuais conforme schema da camada com validacoes de tipo e obrigatoriedade. Alteracoes geram entradas no log de auditoria registrando usuario, timestamp, campos modificados e valores anteriores versus novos. Sistema valida geometria apos edicao antes de persistir.

## Criterios de Aceitacao

1. Modo de edicao de vertices
2. Formulario de atributos populado
3. Validacao de tipos e obrigatoriedade
4. Log de auditoria com diff de valores
5. Validacao de geometria apos edicao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-132, RF-136
