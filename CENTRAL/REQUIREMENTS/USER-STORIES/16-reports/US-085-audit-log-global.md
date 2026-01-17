---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-085: Audit Log Global

Como administrador do sistema, quero visualizar log de auditoria completo de todas as operações realizadas no tenant para que rastreamento seja total, permitindo análise de segurança, investigação de incidentes e conformidade com regulamentações de proteção de dados. A funcionalidade deve apresentar interface de consulta ao histórico de auditoria oferecendo múltiplos critérios de filtragem incluindo usuário específico que executou a ação, tipo de operação realizada (CREATE, UPDATE, DELETE, LOGIN, EXPORT), e intervalo de datas para análise temporal de atividades. O sistema deve exibir registros de auditoria em formato tabular com paginação eficiente para grandes volumes de dados, incluindo informações detalhadas de timestamp preciso, identificação do usuário, tipo de entidade afetada, ação executada, endereço IP de origem e payload de dados modificados quando aplicável. Deve ser oferecida funcionalidade de exportação completa dos logs filtrados em formato CSV para análise externa, arquivamento de longo prazo ou submissão a auditorias regulatórias. Os critérios de aceitação incluem filtros funcionais por user_id, action_type e date_range com aplicação combinada, paginação com controle de tamanho de página e navegação entre páginas, e botão de exportação gerando CSV com todas as colunas relevantes respeitando filtros aplicados. Esta User Story está relacionada ao RF-016 e é implementada através do endpoint GET /api/audit-log no backend GEOAPI com consultas otimizadas para grandes volumes, e interface de consulta no frontend GEOWEB, pertencendo ao Epic 11: Administração. O status atual é implemented, com testes validando integridade dos logs e performance de consultas complexas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
