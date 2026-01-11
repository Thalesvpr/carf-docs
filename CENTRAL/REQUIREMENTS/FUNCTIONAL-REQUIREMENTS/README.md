# FUNCTIONAL-REQUIREMENTS

Requisitos funcionais do CARF especificando o que o sistema deve fazer sem detalhar como implementar. Cada RF segue nomenclatura RF-NNN-titulo-descritivo.md, possui metadados YAML (epic, módulo, prioridade, story_points), descrição objetiva focada no comportamento esperado, critérios de aceitação em formato checklist testável, e rastreabilidade bidirecional para UCs e USs que implementam o requisito. Organizados por domínio: autenticação e autorização (login, JWT, RBAC, multi-tenancy), unidades habitacionais (CRUD, validação geográfica, cálculo de área), titulares (cadastro, CPF, vinculação), comunidades (agregação, relatórios), processos de legitimação (workflow aprovação, documentos Lei 13.465/2017), relatórios (PDF, Excel, GeoJSON, Shapefile), e auditoria (logs de acesso, alterações). Servem como fonte única de verdade (SSOT) - projetos linkam via _INDEX ao invés de duplicar.

## Navegação

**[index-by-epic.md](./index-by-epic.md)** - Índice de todos os 221 Requisitos Funcionais organizados por épica (security: 87, performance: 104, compatibility: 88, scalability: 45)

Documentação complementar de requirements inclui [overview completo](../README.md) apresentando estrutura hierárquica de 11 UCs 221 RFs 140 USs e 85 RNFs com estatísticas de cobertura por módulo e épica, [índice por módulo](../index-by-module.md) organizando requirements conforme projetos implementadores GEOWEB REURBCAD GEOAPI GEOGIS facilitando descoberta de funcionalidades por equipe de desenvolvimento, e [matriz de rastreabilidade](../traceability-matrix.md) mapeando relacionamentos bidirecionais UC→RF→US→RNF estabelecendo conexões explícitas entre casos de uso requisitos funcionais user stories e requisitos não-funcionais.

---

**Última atualização:** 2025-12-29
