# USER-STORIES

Histórias de usuário compartilhadas do CARF focadas em funcionalidades cross-cutting como autenticação (login SSO Keycloak, refresh token, logout), auditoria (rastreamento de alterações, logs de acesso, compliance LGPD), e multi-tenancy (isolamento de dados por município via RLS, seleção de tenant). Cada US segue nomenclatura US-NNN-titulo-descritivo.md, possui metadados YAML (epic, persona, prioridade, story_points), formato narrativo "Como [persona] quero [ação] para [objetivo]" explicando contexto e motivação, critérios de aceitação em formato Gherkin (Given/When/Then) testáveis automaticamente, e rastreabilidade para RFs e UCs relacionados. USs específicas de cada projeto (backend .NET, frontend React, mobile React Native, plugin QGIS) ficam em PROJECTS/*/REQUIREMENTS/USER-STORIES/ organizadas por epic e módulo.

## Navegação

**[index-by-epic.md](./index-by-epic.md)** - Índice de todas as 140 User Stories organizadas por épica (security, performance, compatibility, scalability)

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica, [índice por módulo](../index-by-module.md) organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de user stories por equipe de desenvolvimento, e [matriz de rastreabilidade](../traceability-matrix.md) mapeando relacionamentos bidirecionais UC→RF→US→RNF estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2025-12-29
