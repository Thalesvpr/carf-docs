---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-067: Excluir Documento

Como analista, quero excluir documentos anexados por engano ou que se tornaram obsoletos para que armazenamento seja limpo e apenas documentação relevante seja mantida, onde a funcionalidade deve exigir confirmação obrigatória antes de executar exclusão para prevenir remoções acidentais, garantindo implementação de soft delete através de flag deleted_at em vez de remoção física imediata, permitindo manutenção de audit log completo registrando quem excluiu qual documento e quando para rastreabilidade e conformidade. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de gerenciamento de documentos consumindo GEOAPI através do endpoint DELETE /api/documents/{id} que executa soft delete e registra auditoria, sem requisitos funcionais específicos mas relacionada à gestão de documentos. Os critérios de aceitação incluem disponibilidade de botão ou ícone de exclusão em cada documento listado na interface, exibição de diálogo de confirmação obrigatório antes de executar exclusão perguntando "Tem certeza que deseja excluir?", implementação de soft delete marcando documento com flag deleted_at ou is_deleted em vez de remover fisicamente, ocultação de documentos soft deleted da interface normal mantendo invisíveis para usuários comuns, registro automático em audit log incluindo user_id timestamp document_id e ação DELETE, possibilidade de restauração por administradores através de interface administrativa caso exclusão tenha sido indevida, limpeza física periódica (garbage collection) de documentos soft deleted após período configurável (exemplo 90 dias), e atualização automática da interface removendo documento da lista após exclusão bem-sucedida. A rastreabilidade conecta esta user story ao endpoint DELETE /api/documents/{id}, garantindo gestão responsável de armazenamento com auditoria e possibilidade de recuperação.

---

**Última atualização:** 2025-12-30
