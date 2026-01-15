---
modules: [GEOWEB]
epic: performance
---

# RF-044: Dashboard de Comunidade

Interface deve apresentar visualização consolidada de métricas e gráficos específicos da comunidade onde gráficos de status de unidades exibem distribuição por workflow state (DRAFT PENDING APPROVED) utilizando gráficos de pizza barras ou rosca com cores distintas por status e valores percentuais/absolutos, mapa de calor de densidade mostra concentração espacial de unidades dentro do boundary da comunidade utilizando heatmap layer com gradiente de cores indicando áreas de maior densidade ocupacional facilitando identificação de clusters e padrões de distribuição, indicadores numéricos exibem KPIs essenciais em cards destacados incluindo total de unidades total de titulares área total taxa de aprovação tempo médio de processamento e outros métricas relevantes atualizadas em tempo real ou near-real-time, implementação em módulo GEOWEB utilizando bibliotecas de visualização (Chart.js D3.js Recharts) integração com mapa para heatmap layer queries otimizadas em GEOAPI para agregações complexas e caching de métricas calculadas para garantir performance.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
