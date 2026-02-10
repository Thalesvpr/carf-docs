---
type: leaf
status: review
updated: 2026-02-08
---

# Team Management Feature

A feature de gerenciamento de equipes permite organizar usuarios em equipes de campo com papeis especificos e controlar quais comunidades cada equipe pode acessar. Cada equipe tem no maximo um coordenador e ate quatro cadastradores. A autorizacao por comunidade determina o escopo de trabalho da equipe no app mobile REURBCAD.

## User Stories

US-040 Criar Equipe: o gestor cria uma equipe informando nome e descricao opcional. A equipe e criada vazia, sem membros, no tenant do gestor.

US-041 Adicionar Membro: o gestor adiciona um usuario a equipe informando account_id (UUID Keycloak) e role (COORDINATOR ou CADASTRATOR). O sistema valida o limite de 1 coordenador e 4 cadastradores por equipe.

US-042 Autorizar Comunidade: o gestor concede acesso de uma equipe a uma comunidade especifica com nivel de permissao READ, WRITE ou ADMIN. Todos os membros ativos da equipe herdam automaticamente a autorizacao.

US-043 Consultar Metricas: o gestor ou coordenador visualiza metricas de produtividade da equipe filtradas por periodo (TODAY, WEEK, MONTH, ALL), incluindo total de unidades cadastradas, contagem por status de atendimento, producao por membro e evolucao diaria.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | /api/teams | Listar equipes do tenant |
| GET | /api/teams/{id} | Obter equipe com membros |
| GET | /api/teams/{id}/metrics | Metricas de produtividade |
| GET | /api/teams/{id}/communities | Comunidades autorizadas |

## Regras de Negocio

RN-040: cada equipe pode ter no maximo 1 membro com role COORDINATOR e no maximo 4 membros com role CADASTRATOR. RN-041: um usuario nao pode ser membro da mesma equipe duas vezes, constraint UNIQUE em (team_id, account_id). RN-042: autorizacao por comunidade pode ser concedida a uma equipe inteira (team_id) ou a um usuario individual (account_id), mas nunca ambos no mesmo registro, implementado via constraint XOR. RN-043: quando um membro sai da equipe (left_at preenchido), ele perde automaticamente o acesso herdado as comunidades, mantendo apenas autorizacoes individuais. RN-044: metricas sao calculadas em tempo real agregando dados de unidades criadas pelos membros da equipe no periodo solicitado.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Listar equipes | nao | nao | nao | sim | sim | sim |
| Ver equipe | nao | propria | nao | sim | sim | sim |
| Ver metricas | nao | propria | nao | sim | sim | sim |
| Ver comunidades | sim (propria) | sim (propria) | nao | sim | sim | sim |
