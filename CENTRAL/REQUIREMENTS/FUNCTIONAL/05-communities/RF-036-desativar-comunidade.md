---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-036: Desativar Comunidade

## Descricao

Usuarios com role ADMIN podem desativar comunidade utilizando soft delete onde comunidade e marcada como inativa atraves de flag is_active=false sem exclusao fisica de dados. Unidades vinculadas a comunidade desativada sao preservadas integralmente mantendo referencia para comunidade. Comunidade inativa nao aparece em listagens padrao sendo filtrada automaticamente, mas permanece visivel em contextos administrativos ou quando filtro de inativos ativado.

## Criterios de Aceitacao

1. Soft delete com flag is_active=false
2. Unidades vinculadas preservadas com referencia
3. Comunidade inativa filtrada de listagens padrao
4. Visivel para ADMIN com filtro de inativos
5. Log de auditoria registra motivo da desativacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-008
