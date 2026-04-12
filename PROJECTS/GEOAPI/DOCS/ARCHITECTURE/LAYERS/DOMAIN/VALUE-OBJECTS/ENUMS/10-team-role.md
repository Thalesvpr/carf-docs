---
type: leaf
status: review
updated: 2026-02-08
---

# TeamRole

Value object enum representando o papel de um membro dentro de uma equipe de trabalho, controlando permissoes e responsabilidades no contexto da Team. No banco de dados, corresponde ao campo team_members.role (varchar(30)).

O papel determina quais acoes o membro pode executar dentro da equipe, como adicionar membros ou gerenciar autorizacoes de acesso a comunidades.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| COORDINATOR | Coordenador da equipe com permissoes para adicionar/remover membros e gerenciar autorizacoes de acesso. |
| CADASTRATOR | Membro regular que herda autorizacoes de acesso da equipe mas nao pode gerenciar a equipe. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Pelo menos um coordenador | Toda equipe deve ter ao menos um membro com papel COORDINATOR. |
| Gerenciamento restrito | Apenas COORDINATOR pode adicionar/remover membros e conceder acesso. |
| Ultimo coordenador | Nao e permitido remover o ultimo COORDINATOR de uma equipe. |

Usado em TeamMember.Role para definir papel de cada Account dentro da Team, validado em metodos como Team.AddMember() e Team.RemoveMember(), e integra com CommunityAuthorization onde COORDINATOR pode conceder acesso para a equipe.
