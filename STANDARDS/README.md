---
type: readme
status: rejected
description: "Incompleto. Standards devem ter regras claras e validaveis, nao apenas diretrizes vagas."
updated: 2026-01-15
---

# STANDARDS

Convenções e padrões de documentação do projeto CARF garantindo consistência entre todos os arquivos markdown em CENTRAL e PROJECTS. Estes padrões são validados automaticamente pelos scripts em .scripts/carf_validator que auditam a documentação e reportam violações.

As [convenções de status](./01-file-status-convention.md) definem os metadados obrigatórios no rodapé de cada arquivo indicando se está Pronto, Incompleto ou Errado, incluindo campos específicos para ADRs. A [estrutura de README](./02-readme-structure.md) padroniza como cada pasta deve ter seu README com parágrafo denso, links para filhos e índice gerado automaticamente. As [convenções de nomenclatura](./03-naming-conventions.md) definem prefixos obrigatórios como RF-XXX, UC-XXX e US-XXX, além de terminologia técnica correta para produtos como PostgreSQL e Keycloak.

Os [tipos de documento](./04-document-types.md) especificam seções obrigatórias por tipo como Critérios de Aceitação para RFs e Regras de Negócio para UCs. As [diretrizes de conteúdo](./05-content-guidelines.md) definem limites de tamanho por tipo de documento, densidade de parágrafos e uso adequado de listas. As [convenções de links](./06-link-conventions.md) padronizam formato de paths relativos e isolamento entre CENTRAL e PROJECTS.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (14)

| Documento | Status |
|-----------|--------|
| [STD-001: Convenção de Status de Arquivo](./STD-001-file-status-convention.md) | ○ |
| [STD-002: Estrutura de README](./STD-002-readme-structure.md) | ○ |
| [STD-003: Convenções de Nomenclatura](./STD-003-naming-conventions.md) | ○ |
| [STD-004: Tipos de Documento](./STD-004-document-types.md) | ○ |
| [STD-005: Diretrizes de Conteúdo](./STD-005-content-guidelines.md) | ○ |
| [STD-006: Convenções de Links](./STD-006-link-conventions.md) | ○ |
| [STD-010: PostgreSQL como Database](./STD-010-postgresql-database.md) | ○ |
| [STD-011: .NET 9 para Backend](./STD-011-dotnet-backend.md) | ○ |
| [STD-012: Keycloak para Autenticacao](./STD-012-keycloak-auth.md) | ○ |
| [STD-013: React Native para Mobile](./STD-013-react-native-mobile.md) | ○ |
| [STD-014: Multi-tenancy via RLS](./STD-014-multi-tenancy-rls.md) | ○ |
| [STD-015: Clean Architecture com CQRS](./STD-015-clean-architecture.md) | ○ |
| [STD-016: Stack Frontend Web](./STD-016-frontend-stack.md) | ○ |
| [STD-017: Docker e Kubernetes](./STD-017-containerization.md) | ○ |

<!-- CARF-INDEX-END -->
