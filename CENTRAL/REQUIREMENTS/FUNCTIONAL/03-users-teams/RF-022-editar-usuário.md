---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-022: Editar Usuario

## Descricao

Usuarios com role ADMIN podem editar dados de usuarios pertencentes ao mesmo tenant. Atualizacao inclui modificacao de nome completo, email, role atribuida, status ativo/inativo e vinculacao a equipes. Validacao de permissoes garante que ADMIN so edite usuarios do proprio tenant e que alteracoes de role respeitem hierarquia. Log detalhado de alteracoes registra timestamp, usuario responsavel, campos alterados, valores anteriores e novos valores para auditoria completa.

## Criterios de Aceitacao

1. ADMIN edita apenas usuarios do proprio tenant
2. Alteracoes de role respeitam hierarquia
3. Log de auditoria registra todas modificacoes
4. Sincronizacao com Keycloak para email e role
5. Formulario pre-preenchido com valores atuais

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-021, RF-008
