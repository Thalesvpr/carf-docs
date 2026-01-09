---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: performance
---

# RF-041: Estatísticas de Comunidade

Sistema deve calcular automaticamente estatísticas agregadas de comunidade incluindo contagem de unidades por status (DRAFT PENDING APPROVED REJECTED CHANGES_REQUESTED) exibindo distribuição percentual e quantidades absolutas permitindo análise de progresso de cadastramento e aprovação, total de titulares únicos vinculados a unidades da comunidade calculado através de query agregada distinct eliminando duplicações onde mesmo titular pode possuir múltiplas unidades contabilizando indivíduos únicos para estimativas demográficas, área total em metros quadrados calculada através de soma de áreas individuais de unidades ou cálculo direto de área de polígono de comunidade utilizando funções geoespaciais do PostgreSQL (ST_Area) com conversão apropriada de unidades e formatação para exibição legível (m² hectares km²), implementação em módulo GEOAPI com endpoints dedicados retornando estatísticas pré-calculadas ou calculadas sob demanda com caching para otimizar performance e módulo GEOWEB exibindo métricas em cards dashboards ou painéis de resumo de comunidade.

---

**Última atualização:** 2025-12-30
