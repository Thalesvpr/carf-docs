# USER-STORIES

Histórias de usuário compartilhadas do CARF focadas em funcionalidades cross-cutting como autenticação (login SSO Keycloak, refresh token, logout), auditoria (rastreamento de alterações, logs de acesso, compliance LGPD), e multi-tenancy (isolamento de dados por município via RLS, seleção de tenant). Cada US segue nomenclatura US-NNN-titulo-descritivo.md, possui metadados YAML (epic, persona, prioridade, story_points), formato narrativo "Como [persona] quero [ação] para [objetivo]" explicando contexto e motivação, critérios de aceitação em formato Gherkin (Given/When/Then) testáveis automaticamente, e rastreabilidade para RFs e UCs relacionados. USs específicas de cada projeto (backend .NET, frontend React, mobile React Native, plugin QGIS) ficam em PROJECTS/*/REQUIREMENTS/USER-STORIES/ organizadas por epic e módulo.

## Navegação

**[index-by-epic.md](./index-by-epic.md)** - Índice de todas as 140 User Stories organizadas por épica (security, performance, compatibility, scalability)

Ver também:
- **[../README.md](../README.md)** - Overview completo de Requirements com índices adicionais
- **[../index-by-module.md](../index-by-module.md)** - Requirements organizados por módulo implementador
- **[../traceability-matrix.md](../traceability-matrix.md)** - Matriz de rastreabilidade UC→RF→US→RNF

---

**Última atualização:** 2025-12-29
