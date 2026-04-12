---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-035: Editar Comunidade

## Descricao

Usuarios com role ADMIN podem editar dados de comunidades existentes. Atualizacao inclui modificacao de nome, tipo, area, populacao estimada e outros atributos alfanumericos com validacoes garantindo integridade de dados obrigatorios. Edicao de geometria no mapa implementada atraves de ferramentas interativas permitindo adicionar/remover vertices, mover ou redesenhar boundary. Log automatico de alteracoes registra timestamp, usuario responsavel, campos modificados e snapshot de geometria anterior.

## Criterios de Aceitacao

1. Edicao de atributos alfanumericos com validacao
2. Edicao de geometria com ferramentas interativas
3. Validacao topologica em tempo real
4. Log de auditoria com snapshot de geometria anterior
5. Formulario pre-preenchido com valores atuais

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-008
