---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-017: Criar Tenant

## Descricao

Usuarios com role SUPER_ADMIN devem poder criar novos tenants no sistema. Formulario de criacao inclui campos obrigatorios como nome do tenant, dominio unico identificador (slug), configuracoes iniciais de personalizacao (logo, cores, tema) e parametros tecnicos de infraestrutura. Sistema valida unicidade do dominio garantindo que slug seja unico em toda plataforma, retornando erro descritivo caso duplicado. Criacao provisiona automaticamente estruturas de banco de dados e recursos padrao.

## Criterios de Aceitacao

1. Formulario com campos obrigatorios nome e slug
2. Validacao de unicidade de dominio antes de salvar
3. Slug unico em toda plataforma com erro descritivo se duplicado
4. Provisionamento automatico de estruturas de banco de dados
5. Criacao de roles e configuracoes padrao do novo tenant

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-007
