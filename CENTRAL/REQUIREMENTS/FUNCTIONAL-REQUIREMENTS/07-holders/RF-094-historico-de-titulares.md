---
modules: [GEOWEB, REURBCAD]
epic: maintainability
---

# RF-094: Histórico de Titulares

O sistema deve registrar histórico completo de titulares de cada unidade habitacional ao longo do tempo através de tabela holder_history capturando data de início do vínculo, data de término quando aplicável, tipo de relacionamento vigente no período, percentual de propriedade e motivo de alteração (venda herança separação doação regularizacao outro). Quando titular é removido de unidade ou substituído por outro, sistema cria automaticamente registro histórico preservando informação sobre quem foi titular anteriormente facilitando rastreamento de sucessões, transferências e evolução de direitos sobre imóvel ao longo do processo de regularização. A interface de visualização de unidade apresenta timeline de titulares mostrando cronologicamente quem foram os responsáveis em diferentes períodos, incluindo sobreposições temporais quando aplicável em situações de copropriedade transitória ou processos de transferência gradual de direitos. Cada registro histórico captura contexto da mudança através de campo motivo que pode ser selecionado de lista predefinida ou especificado livremente, documentando razões de alterações que podem ser relevantes para processos jurídicos, auditorias ou simplesmente compreensão da trajetória fundiária da unidade. Implementado no módulo GEOAPI com prioridade Should-have, este recurso é valioso para rastreabilidade de direitos e documentação de processos de regularização que frequentemente envolvem sucessões complexas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
