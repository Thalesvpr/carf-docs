---
modules: [GEOWEB, REURBCAD]
epic: maintainability
---

# RF-091: Tipos de Relacionamento com Unidade

O sistema deve suportar categorização de vínculos entre titulares e unidades através de tipos predefinidos de relacionamento (PROPRIETARIO POSSUIDOR USUFRUTUARIO LOCATARIO COMODATARIO OUTRO), onde cada tipo representa natureza jurídica ou social específica da relação entre pessoa e imóvel. A implementação utiliza enumeração armazenada no campo relationship da tabela associativa unit_holders garantindo valores consistentes e possibilitando queries e filtros baseados em tipo de relacionamento para análises segmentadas. Cada tipo de relacionamento pode ter validações específicas associadas, por exemplo proprietários podem requerer documentação comprobatória diferente de locatários, ou coproprietários podem ter regras de percentual de propriedade enquanto possuidores não, permitindo customização de regras de negócio conforme natureza do vínculo. A interface apresenta seletor de tipo de relacionamento durante vinculação de titular a unidade oferecendo descrições claras de cada categoria para orientar usuário na seleção adequada, incluindo opção OUTRO para situações não contempladas pelos tipos predefinidos com campo de texto livre para especificação. Implementado no módulo GEOAPI com prioridade Must-have, este requisito é fundamental para modelagem fiel da complexidade de relações fundiárias existentes em contextos de ocupação informal onde diferentes naturezas de vínculo coexistem.

---

**Última atualização:** 2025-12-30
