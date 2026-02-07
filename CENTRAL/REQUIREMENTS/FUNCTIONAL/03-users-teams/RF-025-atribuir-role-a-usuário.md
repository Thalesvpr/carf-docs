---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-025: Atribuir Role a Usuario

## Descricao

Usuarios com role ADMIN podem atribuir ou alterar role de usuarios do tenant. Selecao de role ocorre via dropdown exibindo opcoes permitidas (MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR), excluindo SUPER_ADMIN que so pode ser atribuida por outro SUPER_ADMIN. Validacao de permissoes impede escalacao de privilegios alem do proprio nivel do ADMIN. Atualizacao imediata de permissoes onde role e sincronizada com Keycloak e proxima requisicao ja reflete novas permissoes.

## Criterios de Aceitacao

1. Dropdown com roles permitidas para ADMIN
2. SUPER_ADMIN so atribuida por SUPER_ADMIN
3. Validacao impede escalacao de privilegios
4. Sincronizacao imediata com Keycloak
5. Log de auditoria registra mudancas de role

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-006, RF-022
