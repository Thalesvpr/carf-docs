---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# RF-092: Percentual de Propriedade

O sistema deve permitir especificação de percentual de propriedade para cada vínculo entre titular e unidade através de campo ownership_percentage com valores numéricos entre 0 e 100 representando fração de propriedade ou posse que cada titular detém sobre a unidade. Quando aplicável ao tipo de relacionamento (especialmente PROPRIETARIO e POSSUIDOR), sistema valida que soma dos percentuais de todos os titulares da mesma unidade totalize exatamente 100%, alertando usuário sobre inconsistências e bloqueando salvamento quando percentuais não somam corretamente ou excedem totalidade. Para tipos de relacionamento onde percentual não se aplica (LOCATARIO USUFRUTUARIO), campo pode ser deixado vazio ou zerado sendo interpretado como não aplicável ao invés de indicar ausência de direito. A interface exibe percentuais formatados com símbolo % e até duas casas decimais permitindo representação precisa de situações como 33,33% para três coproprietários com partes iguais, além de apresentar em visualizações de unidade a distribuição de propriedade através de gráfico visual (pizza ou barras) facilitando compreensão rápida de estrutura de propriedade compartilhada. Implementado no módulo GEOAPI com prioridade Should-have, este recurso é especialmente importante em contextos de copropriedade e sucessão onde múltiplos herdeiros ou compradores compartilham direitos sobre mesmo imóvel.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
