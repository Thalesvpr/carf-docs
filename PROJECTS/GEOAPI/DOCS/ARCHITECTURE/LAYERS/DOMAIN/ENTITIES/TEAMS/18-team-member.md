---
type: leaf
status: approved
updated: 2026-02-07
---

# TeamMember

Entidade representando a participacao de um Account em uma Team com papel especifico. Define se o membro atua como coordenador (responsavel pela equipe e com acesso ao dashboard) ou cadastrador (operador de campo com acesso ao formulario de cadastro). Herda de BaseEntity fornecendo auditoria temporal.

## Papel no Dominio

O TeamMember materializa o vinculo pessoa-equipe e define o papel do membro dentro do app mobile. COORDINATOR tem acesso ao dashboard de metricas, lista de membros da equipe e pode selecionar regioes de trabalho. CADASTRATOR tem acesso apenas ao mapa e formularios de cadastro, com regiao pre-atribuida pelo coordenador.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TeamId | Guid | nao | FK para Team. |
| AccountId | Guid | nao | UUID do usuario no Keycloak. |
| Role | string | nao | COORDINATOR ou CADASTRATOR. Define permissoes no app mobile. |
| JoinedAt | DateTime | nao | Data de entrada na equipe. |
| LeftAt | DateTime | sim | Data de saida. Null indica membro ativo. |

## Relacionamentos

Pertence a uma Team (obrigatorio). Referencia um Account (obrigatorio). O par (TeamId, AccountId) e unico impedindo membro duplicado.

## Invariantes de Negocio

Cada equipe deve manter ao menos um membro com role COORDINATOR ativo (LeftAt null). Remover ou mudar role do ultimo coordenador gera erro.
