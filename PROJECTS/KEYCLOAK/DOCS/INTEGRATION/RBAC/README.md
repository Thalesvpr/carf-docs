---
type: readme
status: review
description: "README usa tabela resumo com bullets - reescrever tabela em prosa densa"
updated: 2026-01-22
---

# RBAC

Sistema de controle de acesso baseado em roles (Role-Based Access Control) definindo permissões para cada tipo de usuário no ecossistema CARF.

A [hierarquia de roles](./01-roles-hierarchy.md) define seis níveis: `user` (base), `field-agent`, `analyst`, `admin`, `super-admin` (operacionais com herança), e `dev` (transversal). A [role dev](./02-role-dev.md) é transversal e concede acesso a ferramentas de desenvolvimento. As [permissões detalhadas](./03-permissions.md) especificam ações permitidas por role em cada módulo do sistema.

## Tabela Resumo

| Role | Tipo | Descrição |
|------|------|-----------|
| `user` | Operacional | Usuário padrão, funcionalidades básicas |
| `field-agent` | Operacional | Agente de campo, coleta REURBCAD |
| `analyst` | Operacional | Analista REURB, aprovações |
| `admin` | Operacional | Administrador de tenant |
| `super-admin` | Operacional | Acesso multi-tenant |
| `dev` | Transversal | Desenvolvedor, acesso /dev/ |


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-roles-hierarchy](./01-roles-hierarchy.md) | Hierarquia de Roles |
| [02-role-dev](./02-role-dev.md) | Role Dev |
| [03-permissions](./03-permissions.md) | Permissões Detalhadas |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [Hierarquia de Roles](./01-roles-hierarchy.md) | ⚠ |
| [Role Dev](./02-role-dev.md) | ⚠ |
| [Permissões Detalhadas](./03-permissions.md) | ⚠ |

<!-- CARF-INDEX-END -->
