---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-023: Desativar Usuario

## Descricao

Usuarios com role ADMIN podem desativar usuario utilizando soft delete onde usuario e marcado como inativo atraves de flag is_active=false sem exclusao fisica de registro. Login imediatamente bloqueado para usuario desativado, retornando mensagem especifica de usuario inativo. Dados historicos preservados integralmente incluindo unidades cadastradas, documentos anexados e logs de auditoria, permitindo reativacao futura sem perda de contexto. Sincronizacao com Keycloak desabilita conta no Identity Provider.

## Criterios de Aceitacao

1. Soft delete com flag is_active=false
2. Login bloqueado imediatamente apos desativacao
3. Mensagem especifica informando usuario inativo
4. Dados historicos preservados para auditoria
5. Sincronizacao com Keycloak para bloqueio efetivo

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-021, RF-008
