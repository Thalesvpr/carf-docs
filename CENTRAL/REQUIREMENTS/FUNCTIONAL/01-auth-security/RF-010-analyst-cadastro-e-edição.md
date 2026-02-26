---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - REURBWEB
---

# RF-010: ANALYST - Cadastro e Edicao

## Descricao

Usuarios com role ANALYST podem cadastrar e editar unidades, titulares e documentos. Podem criar unidades com campos obrigatorios, vincular titulares, anexar documentos e submeter para aprovacao. Nao podem aprovar workflows, garantindo separacao de responsabilidades onde ANALYST prepara dados e MANAGER aprova.

## Criterios de Aceitacao

1. ANALYST cria unidades com status inicial DRAFT
2. Pode editar dados cadastrais e geometrias
3. Vincula titulares e anexa documentos
4. Submete unidades para aprovacao de MANAGER
5. Nao possui permissao de aprovar ou rejeitar

## Rastreabilidade

- Modulos: GEOAPI, REURBWEB
- Requisitos dependentes: RF-006
