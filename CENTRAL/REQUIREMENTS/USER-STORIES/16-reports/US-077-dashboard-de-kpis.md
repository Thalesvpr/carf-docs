---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-077: Dashboard de KPIs

Como gestor, quero visualizar dashboard interativo com indicadores-chave de performance (KPIs) principais do sistema para que acompanhamento visual e em tempo real do progresso de cadastramento e legitimação seja possível, onde a funcionalidade deve exibir cards destacados mostrando totalizadores (total de unidades total de titulares área total cadastrada), garantindo gráficos de evolução temporal mostrando crescimento de cadastros ao longo do tempo, permitindo visualização de funil de aprovação indicando quantidade de unidades em cada estágio do workflow e taxa de conclusão percentual do processo. Esta funcionalidade é implementada pelo módulo GEOWEB com dashboard interativo consumindo GEOAPI através do endpoint GET /api/dashboard/kpis que agrega métricas em tempo real, integrada ao RF-209 (Dashboard Gerencial) para monitoramento executivo. Os critérios de aceitação incluem exibição de cards numéricos destacados mostrando KPIs principais (total_units total_holders total_area_m2 communities_count), card adicional mostrando taxa de conclusão percentual calculada como unidades APPROVED dividido por total de unidades, gráfico de linha ou barra mostrando evolução temporal de cadastros ao longo de meses ou semanas, gráfico de funil mostrando quantidade de unidades em cada estágio do workflow (DRAFT PENDING APPROVED REJECTED), gráficos interativos permitindo drill-down clicando em segmento para ver detalhes, atualização automática de métricas em tempo real ou com refresh periódico sem recarregar página, filtro opcional por comunidade permitindo visualizar KPIs de comunidade específica versus consolidado geral, filtro temporal permitindo analisar KPIs de período específico (último mês último trimestre ano completo), indicadores visuais de tendência (setas ou cores) mostrando se métrica está crescendo ou decrescendo versus período anterior, e exportação de dashboard completo como PDF ou imagem para inclusão em apresentações. A rastreabilidade conecta esta user story ao RF-209 (Visualização de Indicadores) e ao endpoint GET /api/dashboard/kpis, garantindo visibilidade executiva e tomada de decisão baseada em dados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
