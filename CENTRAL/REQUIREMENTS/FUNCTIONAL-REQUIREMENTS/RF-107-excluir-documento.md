---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# RF-107: Excluir Documento

Este requisito estabelece que usuários autorizados devem poder excluir documentos do sistema de forma controlada e auditável, onde a exclusão é implementada através de soft delete para preservar o histórico e rastreabilidade dos dados, garantindo que o documento não seja removido fisicamente do banco de dados mas marcado como excluído através de um campo deleted_at ou status, permitindo auditoria futura e possível recuperação. O sistema deve exigir confirmação obrigatória antes de executar a exclusão, prevenindo remoções acidentais através de modal ou diálogo que solicite confirmação explícita do usuário, incluindo opcionalmente a razão da exclusão para registro. Toda operação de exclusão deve gerar registro detalhado no log de auditoria, incluindo informações sobre qual usuário executou a ação, timestamp preciso, identificador do documento excluído e contexto da operação, garantindo rastreabilidade completa e conformidade com requisitos de auditoria e governança de dados. A funcionalidade deve estar disponível nos módulos GEOWEB através da interface de gerenciamento de documentos e GEOAPI via endpoint DELETE apropriado com validações de permissão.

---

**Última atualização:** 2025-12-30