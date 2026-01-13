---
modules: [GEOAPI]
epic: performance
---

# RF-106: Download de Documento

O sistema deve permitir que usuários autorizados baixem documentos anexados através de endpoint dedicado que valida permissões antes de servir arquivo, onde verificação garante que usuário possui acesso à entidade (unidade titular comunidade) à qual documento está vinculado conforme regras de controle de acesso baseado em papéis e propriedade. A validação de permissões verifica se usuário possui role adequado (ADMIN MANAGER ANALYST VIEWER) e se tem acesso ao tenant e comunidade específicos onde entidade vinculada está cadastrada, bloqueando downloads não autorizados mesmo quando URL direta do documento é conhecida. O download utiliza streaming de arquivo ao invés de carregar completamente em memória antes de enviar, garantindo performance adequada e consumo eficiente de recursos mesmo para documentos grandes próximos ao limite de 10MB, onde bytes são transmitidos progressivamente conforme lidos do storage. Headers HTTP apropriados são configurados incluindo Content-Type correto baseado em MIME type do documento, Content-Disposition para forçar download ao invés de exibição inline quando apropriado, e Content-Length para permitir barras de progresso precisas em navegadores. Implementado nos módulos GEOWEB e GEOAPI com prioridade Must-have, este recurso completa ciclo de gestão documental permitindo recuperação segura e performática de arquivos anexados, essencial para workflows onde documentos precisam ser consultados, compartilhados ou incluídos em dossiês e processos externos.

---

**Última atualização:** 2025-12-30
