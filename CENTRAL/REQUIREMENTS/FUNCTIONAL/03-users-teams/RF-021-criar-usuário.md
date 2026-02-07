---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-021: Criar Usuario

## Descricao

Usuarios com roles ADMIN e SUPER_ADMIN podem criar novos usuarios no tenant. Formulario de criacao inclui campos obrigatorios nome completo, email unico e role inicial (MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR). Validacao de email unico implementada verificando inexistencia em base do tenant, retornando erro descritivo caso duplicado. Sistema envia automaticamente email de boas-vindas com link para ativacao e definicao de senha inicial. Usuario criado recebe tenant_id do contexto do administrador.

## Criterios de Aceitacao

1. Formulario com campos obrigatorios nome, email e role
2. Validacao de email unico no tenant
3. Email de boas-vindas enviado apos criacao
4. Sincronizacao automatica com Keycloak
5. Atribuicao automatica de tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-001, RF-006
