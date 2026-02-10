---
type: leaf
status: review
updated: 2026-02-08
---

# Role

Value object enum representando papel de usuario no sistema definindo conjunto de permissoes e acesso a funcionalidades conforme hierarquia organizacional. Os papeis sao sincronizados com Keycloak via claims JWT, determinando tanto a UI exibida quanto as operacoes permitidas.

A hierarquia de papeis segue: SUPER_ADMIN > ADMIN > MANAGER > ANALYST > FIELD_COORDINATOR > FIELD_CADASTRATOR.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| SUPER_ADMIN | Administrador do sistema com acesso total a todos os tenants. |
| ADMIN | Administrador do tenant com acesso completo dentro de seu cliente. |
| MANAGER | Gerente coordenando equipes, pode aprovar/rejeitar unidades e ver dashboards. |
| ANALYST | Analista tecnico responsavel por analisar solicitacoes de legitimacao e emitir pareceres. |
| FIELD_COORDINATOR | Coordenador de campo com menu mobile completo e visualizacao de dados da equipe. |
| FIELD_CADASTRATOR | Cadastrador de campo com acesso restrito apenas a mapa e formularios. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Acesso multi-tenant | Apenas SUPER_ADMIN pode trocar de tenant. |
| Aprovacao de unidades | Apenas MANAGER e ANALYST podem aprovar unidades. |
| Gerenciamento de usuarios | Apenas SUPER_ADMIN e ADMIN podem gerenciar usuarios. |
| Papeis de campo | FIELD_COORDINATOR e FIELD_CADASTRATOR operam no app mobile REURBCAD. |

Usado em Account.Role definindo permissoes do usuario, validado em authorization policies, integra com Keycloak onde roles sao sincronizadas via claims JWT, e determina UI exibida em cada aplicacao do ecossistema.
