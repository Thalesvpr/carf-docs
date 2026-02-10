---
type: leaf
status: review
updated: 2026-02-08
---

# Permissions Matrix

Value object conceitual definindo sistema de permissoes granulares baseado em recursos e acoes, permitindo controle de acesso fino alem de roles basicos (SUPER_ADMIN, ADMIN, MANAGER, ANALYST, FIELD_COORDINATOR, FIELD_CADASTRATOR).

## Estrutura de Permissao

Cada permissao e composta de tres partes formando uma permission string: recurso.acao.escopo.

| Componente | Valores | Descricao |
|------------|---------|-----------|
| Recurso | UNIT, HOLDER, COMMUNITY, PROCESS, DOCUMENT, TEAM, TENANT, REPORT | Entidade ou funcionalidade alvo. |
| Acao | CREATE, READ, UPDATE, DELETE, APPROVE, REJECT, EXPORT, IMPORT | Operacao a ser executada. |
| Escopo | OWN_ONLY, TEAM_ONLY, COMMUNITY_ONLY, TENANT_ONLY, ALL | Abrangencia dos registros acessiveis. |

## Permissoes por Role

| Role | Permissoes Padrao |
|------|-------------------|
| SUPER_ADMIN | *.*.all (wildcard irrestrito cross-tenant). |
| ADMIN | *.*.tenant_only (gestao completa do proprio tenant). |
| MANAGER | units.approve.community_only, processes.approve.community_only, teams.read.tenant_only. |
| ANALYST | units.*.community_only, holders.*.community_only, documents.*.community_only. |
| FIELD_COORDINATOR | units.create.team_only, units.read.team_only, documents.create.team_only. |
| FIELD_CADASTRATOR | units.create.own_only, units.read.own_only, documents.create.own_only. |

## Resolucao de Permissao

Permissoes explicitas do Account sobrescrevem permissoes do Team que sobrescrevem permissoes padrao do Role. Deny permissions (ex: units.delete.deny) tem precedencia sobre allow, implementando principio de privilegio minimo. Cache distribuido de 5 minutos com invalidacao ao alterar permissoes.

## Verificacao em Camadas

| Camada | Descricao |
|--------|-----------|
| Middleware | Verifica permission antes de executar acao consultando cache. |
| Domain Service | Double-check em logica critica como approval. |
| Repository | Aplica filtros automaticos baseado em scope (WHERE clause transparente). |
| Frontend | Desabilita botoes e oculta menus sem permission (nao e camada de seguranca confiavel). |
