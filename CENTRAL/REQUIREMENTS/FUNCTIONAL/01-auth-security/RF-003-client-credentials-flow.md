---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOGIS
  - GEOAPI
---

# RF-003: Autenticacao Plugin QGIS

## Descricao

O plugin QGIS (GEOGIS) deve implementar autenticacao em duas etapas conforme WORKFLOW-MESTRE. Primeira etapa: login via Keycloak OAuth2 com interface de autenticacao integrada ao plugin. Segunda etapa: usuario informa AUTHENTICATION KEY (chave adicional) que vincula sessao do plugin ao backend e habilita acesso as ortofotos do tenant designado. A chave e validada pelo backend GEOAPI antes de liberar acesso aos recursos geoespaciais.

## Criterios de Aceitacao

1. Plugin exibe tela de login Keycloak integrada
2. Apos login OAuth2, solicita AUTHENTICATION KEY
3. Backend valida combinacao token + chave antes de liberar acesso
4. Credenciais armazenadas de forma segura no keychain do SO
5. Renovacao automatica de token antes da expiracao

## Rastreabilidade

- Modulos: GEOGIS, GEOAPI
- Requisitos dependentes: RF-001, RF-013
