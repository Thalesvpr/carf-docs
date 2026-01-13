---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: usability
---

# RF-095: Buscar Titular por CPF

O sistema deve oferecer busca rápida de titulares através de CPF ou CNPJ utilizando endpoint dedicado que retorna resultados em tempo real enquanto usuário digita, onde funcionalidade de autocomplete apresenta sugestões imediatas facilitando localização de titulares existentes durante vinculação a unidades. A busca normaliza entrada removendo formatação (pontos hífens barras) antes de consultar banco de dados garantindo que titular seja encontrado independente de como usuário digita o documento (com ou sem formatação), aplicando mesma normalização durante armazenamento para consistência. Quando múltiplos titulares com mesmo CPF são encontrados (indicando possível duplicação), sistema exibe todos os registros conflitantes alertando usuário sobre situação anômala e oferecendo funcionalidade de mesclagem para consolidar registros duplicados em único titular correto. A interface de formulário de unidade integra busca de titular através de campo com autocomplete onde digitação de CPF dispara busca em tempo real apresentando nome e dados básicos do titular encontrado, permitindo seleção direta para vinculação ou opção de criar novo titular se busca não retornar resultados. Implementado nos módulos GEOWEB e GEOAPI com prioridade Must-have, este recurso previne duplicações, acelera vinculação de titulares a unidades e melhora experiência de usuário através de busca inteligente e responsiva.

---

**Última atualização:** 2025-12-30
