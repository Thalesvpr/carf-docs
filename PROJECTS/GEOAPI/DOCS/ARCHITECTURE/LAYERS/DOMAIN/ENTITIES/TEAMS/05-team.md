---
type: leaf
status: approved
updated: 2026-02-07
---

# Team

Entidade aggregate root representando equipe de campo que agrupa usuarios para atribuicao coletiva de acesso a comunidades. Cada equipe tipicamente contem um coordenador e um ou mais cadastradores que operam juntos em campo usando o app REURBCAD. Herda de BaseAggregateRoot suportando domain events.

## Papel no Dominio

A equipe e a unidade organizacional que conecta pessoas a comunidades. Quando uma CommunityAuthorization e concedida a uma equipe, todos os seus membros ativos herdam automaticamente o acesso. Isso simplifica a gestao de permissoes: o manager atribui acesso a equipe uma vez em vez de configurar cada membro individualmente.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. |
| Name | string | nao | Nome da equipe. |
| Description | string | sim | Descricao opcional. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Colecao de TeamMembers vinculando Accounts com roles especificas (COORDINATOR ou CADASTRATOR). Colecao de CommunityAuthorizations definindo quais comunidades a equipe pode acessar e com qual nivel de permissao.

## Invariantes de Negocio

Cada equipe deve ter ao menos um membro com role COORDINATOR. Tentativa de remover o ultimo coordenador gera erro. Um Account pode pertencer a multiplas equipes mas com apenas um vinculo ativo por equipe.

## Domain Events

TeamCreatedEvent emitido ao criar. TeamMemberAddedEvent emitido ao adicionar membro. TeamMemberRemovedEvent emitido ao remover membro.
