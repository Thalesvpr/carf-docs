# FUNCTIONAL-REQUIREMENTS

Requisitos funcionais do CARF especificando o que o sistema deve fazer sem detalhar como implementar. Cada RF segue nomenclatura RF-NNN-titulo-descritivo.md, possui metadados YAML (epic, módulo, prioridade, story_points), descrição objetiva focada no comportamento esperado, critérios de aceitação em formato checklist testável, e rastreabilidade bidirecional para UCs e USs que implementam o requisito. Organizados por domínio: autenticação e autorização (login, JWT, RBAC, multi-tenancy), unidades habitacionais (CRUD, validação geográfica, cálculo de área), titulares (cadastro, CPF, vinculação), comunidades (agregação, relatórios), processos de legitimação (workflow aprovação, documentos Lei 13.465/2017), relatórios (PDF, Excel, GeoJSON, Shapefile), e auditoria (logs de acesso, alterações). Servem como fonte única de verdade (SSOT) - projetos linkam via _INDEX ao invés de duplicar.

## Navegação

Índice de todos os 221 Requisitos Funcionais organizados por épica (security: 87, performance: 104, compatibility: 88, scalability: 45)

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de funcionalidades por equipe de desenvolvimento estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.



---

**Última atualização:** 2025-12-29

---

<!-- GENERATED:START - Não edite abaixo desta linha -->
## Índice por Domínio (221 requisitos)

| # | Domínio | Arquivos |
|:--|:--------|:--------:|
| 01 | [Autenticação e Segurança](./01-auth-security/README.md) | 16 |
| 02 | [Gestão de Tenants](./02-tenants/README.md) | 4 |
| 03 | [Usuários e Equipes](./03-users-teams/README.md) | 12 |
| 04 | [Notificações](./04-notifications/README.md) | 1 |
| 05 | [Gestão de Comunidades](./05-communities/README.md) | 15 |
| 06 | [Gestão de Unidades](./06-units/README.md) | 35 |
| 07 | [Gestão de Titulares](./07-holders/README.md) | 18 |
| 08 | [Documentos e Mídia](./08-documents-media/README.md) | 25 |
| 09 | [Camadas e Features](./09-layers-features/README.md) | 15 |
| 10 | [Análise Espacial](./10-spatial-analysis/README.md) | 11 |
| 11 | [Anotações](./11-annotations/README.md) | 4 |
| 12 | [Levantamentos Topográficos](./12-surveys/README.md) | 15 |
| 13 | [Processos de Legitimação](./13-legitimation/README.md) | 10 |
| 14 | [Modo Offline e Sincronização](./14-offline-sync/README.md) | 15 |
| 15 | [Exportação de Dados](./15-data-export/README.md) | 6 |
| 16 | [Relatórios](./16-reports/README.md) | 9 |
| 17 | [Integrações WMS/WMTS](./17-wms-wmts/README.md) | 10 |

*Gerado automaticamente em 2026-01-13 19:11*
<!-- GENERATED:END -->
