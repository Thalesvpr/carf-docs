---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
  - GEOAPI
---

# RF-011: FIELD_AGENT - Coleta de Dados

## Descricao

Usuarios com role FIELD_AGENT utilizam aplicativo mobile REURBCAD para cadastrar unidades em campo. Podem trabalhar offline com dados armazenados localmente, tirar fotos com geolocalizacao automatica e sincronizar quando conexao disponivel. Conforme WORKFLOW-MESTRE, FIELD_AGENT so acessa dados apos Analista publicar trabalho do tenant no backend.

## Criterios de Aceitacao

1. Cadastro de unidades funciona offline
2. Fotos capturadas incluem GPS e timestamp
3. Sincronizacao automatica ao retornar conexao
4. Acesso liberado somente apos publicacao pelo Analista
5. Download unico e temporario do pacote do tenant

## Rastreabilidade

- Modulos: REURBCAD, GEOAPI
- Requisitos dependentes: RF-006, RF-013
