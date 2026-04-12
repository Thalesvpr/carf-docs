---
type: readme
status: review
updated: 2026-02-07
---

# RBAC

Sistema de controle de acesso baseado em roles definindo permissoes para cada tipo de usuario no ecossistema CARF. O realm-export.json configura seis realm roles operacionais em hierarquia de arvore (nao linear) via composite roles, mais uma role transversal dev planejada.

A [hierarquia de roles](./01-roles-hierarchy.md) organiza as roles em dois ramos sob manager: analyst (escritorio, aprovacoes, relatorios) e field-coordinator > field-cadastrator (campo, coleta, supervisao). Admin herda manager, super-admin herda admin. A [role dev](./02-role-dev.md) e transversal, sem relacao de heranca, concedendo acesso a ferramentas de desenvolvimento no WebDocs. As [permissoes detalhadas](./03-permissions.md) especificam acoes permitidas por role em cada endpoint da GEOAPI, incluindo client roles do admin (manage-users, manage-tenants, view-audit-logs) e do reurbcad (sync-data, manage-team).

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
