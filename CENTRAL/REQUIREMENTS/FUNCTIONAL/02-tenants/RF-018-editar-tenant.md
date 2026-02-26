---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-018: Editar Tenant

## Descricao

Usuarios com role SUPER_ADMIN e ADMIN do proprio tenant podem editar configuracoes do tenant. Atualizacao inclui modificacao de nome oficial, logo institucional, cores de tema, personalizacao de interface e parametros operacionais especificos como limites de usuarios e quotas de storage. Campos criticos como nome e dominio nao podem ser deixados vazios. Modificacoes em identificador unico (slug) sao bloqueadas devido a impacto em URLs e referencias existentes. Log de alteracoes registra historico completo de modificacoes.

## Criterios de Aceitacao

1. SUPER_ADMIN e ADMIN podem editar configuracoes do tenant
2. Campos criticos validados como obrigatorios
3. Slug imutavel apos criacao do tenant
4. Log de auditoria registra todas modificacoes
5. Formulario pre-preenchido com valores atuais

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-017, RF-007, RF-008
