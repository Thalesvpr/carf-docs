---
type: leaf
status: draft
updated: 2026-02-08
---

# Hierarquia de Roles

Sistema CARF implementa sete realm roles em hierarquia de arvore (nao linear) com composite roles no Keycloak. Seis roles operacionais em dois ramos (campo e escritorio) unificam-se a partir de manager. Role dev e transversal e combinavel com qualquer role operacional.

## Tabela de Heranca

| Role | Herda de | Permissoes Principais |
|:-----|:---------|:----------------------|
| field-cadastrator | Nenhuma (base) | REURBCAD mapa e formularios, cria/edita unidades proprias, upload fotos |
| field-coordinator | field-cadastrator | Menu mobile completo, dados da equipe, reurbcad:manage-team |
| analyst | Nenhuma (ramo separado) | GEOWEB aprovacoes/rejeicoes, edicao qualquer unidade, relatorios CSV/PDF |
| manager | analyst E field-coordinator | Juncao campo e escritorio, gerencia equipes, visao completa do tenant |
| admin | manager | Gestao usuarios, config tenant (nome, CNPJ), audit logs, admin:manage-users |
| super-admin | admin | Criar/deletar tenants, switcher sem validacao, Admin API, admin:manage-tenants |
| dev | Nenhuma (transversal) | Secao /dev/ WEBDOCS: Swagger, docs tecnica, metricas debug |

## Ramo de Campo

Field-cadastrator e o nivel operacional basico para coleta de dados no REURBCAD sem menu completo, sem deletar registros ou aprovar unidades. Field-coordinator herda essas permissoes e adiciona supervisao de equipe.

## Ramo de Escritorio

Analyst destina-se a analistas GEOWEB que aprovam ou rejeitam unidades cadastradas e geram relatorios. Nao herda de field-coordinator pois sao contextos distintos (escritorio versus campo).

## Unificacao

Manager unifica ambos os ramos herdando analyst e field-coordinator. Admin herda de manager adicionando gestao de usuarios. Super-admin herda de admin com capacidades cross-tenant.

## Role Transversal

Role dev nao participa da hierarquia e pode ser combinada com qualquer role. Nao concede permissoes operacionais, requerendo atribuicao explicita. Ver [02-role-dev.md](./02-role-dev.md).
