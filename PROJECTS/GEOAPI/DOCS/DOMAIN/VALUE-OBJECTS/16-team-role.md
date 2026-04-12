---
type: leaf
status: review
updated: 2026-02-08
---

# TeamRole

Value object enum imutavel representando o papel de um membro dentro de uma equipe de campo. Persiste na coluna role varchar(30) da tabela team_members. Define permissoes do membro dentro do contexto do team no app mobile REURBCAD.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| COORDINATOR | Coordenador de equipe. Visualiza dados de todos os membros, coordena trabalho em campo, acesso completo ao menu mobile. |
| CADASTRATOR | Cadastrador de campo. Acesso restrito a mapa e formularios, visualiza apenas dados proprios. |

## Diferenca de Role (Account) e TeamRole

Role e o papel global do usuario no sistema (FIELD_COORDINATOR, FIELD_CADASTRATOR, ANALYST). TeamRole e o papel dentro de um Team especifico. Um usuario pode ser CADASTRATOR em um team e COORDINATOR em outro. Role de Account prevalece para operacoes fora de contexto de team.
