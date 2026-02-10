---
type: leaf
status: review
updated: 2026-02-08
---

# Role

Value object enum imutavel representando o papel funcional de um usuario no sistema, definindo nivel de acesso, permissoes e responsabilidades conforme hierarquia organizacional. Implementa controle de acesso baseado em roles (RBAC).

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| SUPER_ADMIN | Super administrador. Acesso irrestrito a todos tenants. Destinado a operadores da plataforma SaaS. |
| ADMIN | Administrador de tenant. Gestao completa do proprio tenant: usuarios, teams, configuracoes. |
| MANAGER | Gestor operacional. Supervisao, aprovacao de processos, relatorios consolidados. |
| ANALYST | Analista tecnico. Analise e validacao de processos, pareceres tecnicos. |
| FIELD_COORDINATOR | Coordenador de campo. Menu mobile completo, visualiza dados da equipe, coordena trabalho. |
| FIELD_CADASTRATOR | Cadastrador de campo. Acesso restrito a mapa e formularios, apenas dados proprios. |

## Hierarquia de Permissoes

| Nivel | Role | Pode fazer tudo de |
|-------|------|--------------------|
| 6 | SUPER_ADMIN | Todos os roles abaixo + gestao cross-tenant. |
| 5 | ADMIN | MANAGER + gestao de usuarios e configuracoes. |
| 4 | MANAGER | ANALYST + aprovacao de processos e gestao de equipes. |
| 3 | ANALYST | FIELD_COORDINATOR + analise e pareceres. |
| 2 | FIELD_COORDINATOR | FIELD_CADASTRATOR + visualizacao de dados da equipe. |
| 1 | FIELD_CADASTRATOR | Operacoes basicas de cadastro. |

## Regras de Atribuicao

| Regra | Descricao |
|-------|-----------|
| Role padrao | Novo usuario recebe FIELD_CADASTRATOR por padrao (privilegio minimo). |
| Primeiro do tenant | Primeiro usuario de novo tenant e automaticamente ADMIN. |
| SUPER_ADMIN restrito | So pode ser atribuido via acesso administrativo da plataforma. |
| Role obrigatorio | Account.role e obrigatorio. Nao pode ser removido, apenas alterado. |
| Promocao requer superior | Mudanca de role requer acao de usuario com role superior. |
