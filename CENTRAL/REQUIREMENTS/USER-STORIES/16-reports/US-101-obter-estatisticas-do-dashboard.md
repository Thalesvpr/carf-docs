---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-101: Obter Estatísticas do Dashboard

Como gerente operacional do tenant, quero visualizar KPIs do dashboard principal consolidando métricas globais do sistema para que acompanhar performance geral do tenant seja possível através de visão panorâmica de todas as operações, facilitando gestão estratégica e identificação de tendências. A funcionalidade deve apresentar dashboard executivo agregando estatísticas de múltiplas comunidades e projetos incluindo total de unidades habitacionais no tenant, quantidade de comunidades ativas sob gestão, número de usuários ativos no sistema, volume de processos de legitimação em andamento, taxa de conclusão média ponderada considerando todas as comunidades, e estatísticas de uso de armazenamento e recursos computacionais. O sistema deve calcular indicadores de produtividade incluindo média de unidades cadastradas por dia nos últimos 30 dias, distribuição de workload entre membros da equipe, taxa de crescimento do cadastro territorial comparando períodos mensais ou trimestrais, e alertas de proximidade a limites contratuais de usuários ou armazenamento. As métricas devem ser apresentadas com visualizações gráficas intuitivas incluindo gráficos de linha para evolução temporal, gráficos de pizza para distribuições percentuais, e cartões de resumo com valores destacados e indicadores de tendência (crescimento, estabilidade, declínio). Os critérios de aceitação incluem endpoint implementado retornando estrutura JSON completa com métricas agregadas de todo o tenant, validação de permissões restringindo acesso a usuários com roles gerenciais (manager, admin), tratamento adequado de erros incluindo tenant não encontrado ou sessão expirada, documentação OpenAPI detalhada com exemplos de response, e testes unitários e de integração validando agregações complexas e performance de consultas. Esta User Story está relacionada ao RF-205 e é implementada através do endpoint GET /api/dashboard/stats no backend GEOAPI com consultas otimizadas para grandes volumes, e componentes de visualização no frontend GEOWEB, pertencendo ao Epic 2: Cadastro de Unidades. O status atual é proposed, com endpoint existente mas documentação formal criada recentemente.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
