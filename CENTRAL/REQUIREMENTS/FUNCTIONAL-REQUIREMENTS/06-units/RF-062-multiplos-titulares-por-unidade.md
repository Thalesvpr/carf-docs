---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: units
---

# RF-062: Múltiplos Titulares por Unidade

O sistema deve permitir que uma unidade habitacional tenha múltiplos titulares vinculados simultaneamente com diferentes tipos de relacionamento e percentuais de propriedade, onde a implementação utiliza tabela associativa unit_holders contendo campos relationship, ownership_percentage e is_primary. Cada vínculo representa uma relação específica entre pessoa (física ou jurídica) e unidade, permitindo modelagem de situações reais como copropriedade, condomínio, posse compartilhada ou múltiplos responsáveis com papéis distintos na mesma unidade. O sistema deve validar que a soma dos percentuais de propriedade não ultrapasse 100% quando aplicável, alertando o usuário sobre inconsistências e bloqueando salvamento se configuração de percentuais for inválida. Apenas um titular pode ser marcado como principal (is_primary=true) por unidade, garantindo identificação clara do responsável primário para comunicações, notificações e exibição prioritária em listagens e relatórios, onde o titular principal aparece destacado visualmente facilitando reconhecimento rápido da responsabilidade principal sobre cada unidade cadastrada.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
