# USER-STORIES

Histórias de usuário compartilhadas do CARF focadas em funcionalidades cross-cutting como autenticação (login SSO Keycloak, refresh token, logout), auditoria (rastreamento de alterações, logs de acesso, compliance LGPD), e multi-tenancy (isolamento de dados por município via RLS, seleção de tenant). Cada US segue nomenclatura US-NNN-titulo-descritivo.md, possui metadados YAML (epic, persona, prioridade, story_points), formato narrativo "Como [persona] quero [ação] para [objetivo]" explicando contexto e motivação, critérios de aceitação em formato Gherkin (Given/When/Then) testáveis automaticamente, e rastreabilidade para RFs e UCs relacionados. USs específicas de cada projeto (backend .NET, frontend React, mobile React Native, plugin QGIS) ficam em PROJECTS/*/REQUIREMENTS/USER-STORIES/ organizadas por epic e módulo.

## Navegação

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de user stories por equipe de desenvolvimento estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2025-12-29

---

<!-- GENERATED:START - Não edite abaixo desta linha -->
## Índice por Domínio (140 requisitos)

| # | Domínio | Arquivos |
|:--|:--------|:--------:|
| 01 | [Autenticação e Segurança](./01-auth-security/README.md) | 9 |
| 02 | [Gestão de Tenants](./02-tenants/README.md) | 5 |
| 03 | [Usuários e Equipes](./03-users-teams/README.md) | 7 |
| 04 | [Notificações](./04-notifications/README.md) | 3 |
| 05 | [Gestão de Comunidades](./05-communities/README.md) | 4 |
| 06 | [Gestão de Unidades](./06-units/README.md) | 27 |
| 07 | [Gestão de Titulares](./07-holders/README.md) | 9 |
| 08 | [Documentos e Mídia](./08-documents-media/README.md) | 9 |
| 09 | [Camadas e Features](./09-layers-features/README.md) | 3 |
| 10 | [Análise Espacial](./10-spatial-analysis/README.md) | 10 |
| 11 | [Anotações](./11-annotations/README.md) | 4 |
| 12 | [Levantamentos Topográficos](./12-surveys/README.md) | 9 |
| 13 | [Processos de Legitimação](./13-legitimation/README.md) | 4 |
| 14 | [Modo Offline e Sincronização](./14-offline-sync/README.md) | 11 |
| 15 | [Exportação de Dados](./15-data-export/README.md) | 7 |
| 16 | [Relatórios](./16-reports/README.md) | 12 |
| 17 | [Integrações WMS/WMTS](./17-wms-wmts/README.md) | 7 |

*Gerado automaticamente em 2026-01-13 19:11*
<!-- GENERATED:END -->
