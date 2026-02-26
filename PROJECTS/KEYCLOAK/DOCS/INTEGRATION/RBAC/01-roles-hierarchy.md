---
type: leaf
status: draft
updated: 2026-02-21
---

# Hierarquia de Roles

Sistema CARF implementa oito realm roles em hierarquia de arvore (nao linear) com composite roles no Keycloak. Seis roles operacionais em dois ramos (campo e escritorio) unificam-se a partir de manager. Role dev e transversal e combinavel com qualquer role operacional. Role drone-operator e uma base isolada exclusiva para upload de ortofotos.

## Tabela de Heranca

| Role | Herda de | Permissoes Principais |
|:-----|:---------|:----------------------|
| field-cadastrator | Nenhuma (base) | REURBCAD mapa e formularios, cria/edita unidades proprias, upload fotos |
| field-coordinator | field-cadastrator | Menu mobile completo, dados da equipe, reurbcad:manage-team |
| analyst | Nenhuma (ramo separado) | REURBWEB aprovacoes/rejeicoes, edicao qualquer unidade, relatorios CSV/PDF |
| manager | analyst E field-coordinator | Juncao campo e escritorio, gerencia equipes, visao completa do tenant |
| admin | manager | Gestao usuarios, config tenant (nome, CNPJ), audit logs, admin:manage-users |
| super-admin | admin | Criar/deletar tenants, switcher sem validacao, Admin API, admin:manage-tenants |
| drone-operator | Nenhuma (base isolada) | Upload de ortofotos via portal, restrito ao tenant designado |
| dev | Nenhuma (transversal) | Secao /dev/ WEBDOCS: Swagger, docs tecnica, metricas debug |

## Ramo de Campo

Field-cadastrator e o nivel operacional basico para coleta de dados no REURBCAD sem menu completo, sem deletar registros ou aprovar unidades. Field-coordinator herda essas permissoes e adiciona supervisao de equipe.

## Ramo de Escritorio

Analyst destina-se a analistas REURBWEB que aprovam ou rejeitam unidades cadastradas e geram relatorios. Nao herda de field-coordinator pois sao contextos distintos (escritorio versus campo).

## Ramo de Operador de Drone

Drone-operator e uma role base isolada que nao pertence ao ramo de campo nem ao ramo de escritorio. Concede exclusivamente permissao de upload de ortofotos (imagens aereas capturadas por drone) no portal do tenant designado. Nao herda de nenhuma outra role e nao concede acesso a qualquer outra capacidade do sistema — nao acessa REURBCAD, REURBWEB, ADMIN, nao visualiza unidades, nao gera relatorios. Nenhuma role herda de drone-operator.

## Unificacao

Manager unifica ambos os ramos herdando analyst e field-coordinator. Admin herda de manager adicionando gestao de usuarios. Super-admin herda de admin com capacidades cross-tenant.

## Role Transversal

Role dev nao participa da hierarquia e pode ser combinada com qualquer role. Nao concede permissoes operacionais, requerendo atribuicao explicita. Ver [02-role-dev.md](./02-role-dev.md).
