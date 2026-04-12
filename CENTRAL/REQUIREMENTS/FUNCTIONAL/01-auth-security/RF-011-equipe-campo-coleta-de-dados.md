---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
  - GEOAPI
---

# RF-011: Equipe de Campo - Coleta de Dados

## Descricao

Usuarios com roles FIELD_COORDINATOR e FIELD_CADASTRATOR utilizam aplicativo mobile REURBCAD para cadastrar unidades em campo. FIELD_COORDINATOR supervisiona a equipe de campo e tem acesso ao menu completo do aplicativo mobile. FIELD_CADASTRATOR tem acesso restrito apenas ao mapa e formularios, sem menu de navegacao. Ambos podem trabalhar offline com dados armazenados localmente, tirar fotos com geolocalizacao automatica e sincronizar quando conexao disponivel. Conforme WORKFLOW-MESTRE, equipe de campo so acessa dados apos Analista publicar trabalho do tenant no backend.

## Criterios de Aceitacao

1. Cadastro de unidades funciona offline
2. Fotos capturadas incluem GPS e timestamp
3. Sincronizacao automatica ao retornar conexao
4. Acesso liberado somente apos publicacao pelo Analista
5. Download unico e temporario do pacote do tenant

## Rastreabilidade

- Modulos: REURBCAD, GEOAPI
- Requisitos dependentes: RF-006, RF-013
