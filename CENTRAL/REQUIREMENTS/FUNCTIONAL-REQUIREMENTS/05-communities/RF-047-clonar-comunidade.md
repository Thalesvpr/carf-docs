---
modules: [GEOWEB]
epic: compatibility
---

# RF-047: Clonar Comunidade

Usuários com role ADMIN podem clonar comunidade existente criando cópia completa útil para gerenciar fases sequenciais de projeto ou variações de planejamento onde cópia inclui geometria de boundary idêntica configurações de camadas WMS documentos anexados (opcionalmente) e metadados relevantes, unidades vinculadas explicitamente não copiadas garantindo que clone inicia vazio de cadastros permitindo recadastramento específico para nova fase ou contexto preservando separação lógica entre fases de projeto, novo nome gerado automaticamente através de padrão configurável (ex: "Nome Original - Cópia" ou "Nome Original - Fase 2") com possibilidade de edição imediata antes de confirmação final prevenindo confusão entre original e clone, implementação em módulos GEOWEB e GEOAPI com ação de clonagem acessível via menu de contexto ou botão dedicado modal de confirmação permitindo customização de nome e seleção de elementos a copiar processamento assíncrono se operação demorada e redirecionamento automático para edição de comunidade clonada após conclusão.

---

**Última atualização:** 2025-12-30
