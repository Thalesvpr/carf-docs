---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-100: Ver Estatísticas de Comunidade

Como gerente de projeto de regularização fundiária, quero visualizar KPIs consolidados de uma comunidade específica para que acompanhar progresso de regularização seja facilitado através de métricas quantitativas objetivas, permitindo tomada de decisão baseada em dados e identificação de gargalos operacionais. A funcionalidade deve apresentar dashboard dedicado à comunidade selecionada exibindo indicadores-chave de performance incluindo total de unidades habitacionais cadastradas, distribuição por status de processamento (rascunho, em análise, aprovado, rejeitado), percentual de conclusão do cadastramento territorial, quantidade de titulares únicos identificados, área total mapeada em metros quadrados ou hectares, e timeline de evolução do cadastro ao longo do tempo. O sistema deve calcular e exibir métricas derivadas incluindo taxa de aprovação de processos, tempo médio de processamento por unidade, densidade habitacional da comunidade, e comparativo com metas estabelecidas no planejamento inicial do projeto. As estatísticas devem ser atualizadas em tempo real ou com latência mínima refletindo operações recentes de cadastramento, validação e aprovação realizadas pela equipe técnica. Os critérios de aceitação incluem endpoint implementado retornando objeto JSON com todas as métricas estatísticas da comunidade, validação de permissões garantindo que apenas usuários com role adequado possam acessar dados sensíveis, tratamento robusto de erros incluindo comunidade não encontrada ou acesso negado, documentação OpenAPI completa descrevendo estrutura de response e códigos de status HTTP, e cobertura de testes unitários e de integração validando cálculos estatísticos e regras de acesso. Esta User Story está relacionada ao RF-041 e é implementada através do endpoint GET /api/communities/{id}/stats no backend GEOAPI, com widget de visualização no frontend GEOWEB, pertencendo ao Epic 2: Cadastro de Unidades. O status atual é proposed, indicando que o endpoint existe na base de código mas a User Story não estava formalmente documentada até consolidação recente da arquitetura.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
