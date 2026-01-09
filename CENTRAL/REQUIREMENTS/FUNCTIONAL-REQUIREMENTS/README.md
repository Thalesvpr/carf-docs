# FUNCTIONAL-REQUIREMENTS

Requisitos funcionais do CARF especificando o que o sistema deve fazer sem detalhar como implementar. Cada RF segue nomenclatura RF-NNN-titulo-descritivo.md, possui metadados YAML (epic, módulo, prioridade, story_points), descrição objetiva focada no comportamento esperado, critérios de aceitação em formato checklist testável, e rastreabilidade bidirecional para UCs e USs que implementam o requisito. Organizados por domínio: autenticação e autorização (login, JWT, RBAC, multi-tenancy), unidades habitacionais (CRUD, validação geográfica, cálculo de área), titulares (cadastro, CPF, vinculação), comunidades (agregação, relatórios), processos de legitimação (workflow aprovação, documentos Lei 13.465/2017), relatórios (PDF, Excel, GeoJSON, Shapefile), e auditoria (logs de acesso, alterações). Servem como fonte única de verdade (SSOT) - projetos linkam via _INDEX ao invés de duplicar.

---

**Última atualização:** 2025-12-29
