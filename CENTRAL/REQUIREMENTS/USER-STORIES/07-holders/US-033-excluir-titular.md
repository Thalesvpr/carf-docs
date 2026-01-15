---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-033: Excluir Titular

Como gestor, quero excluir titular cadastrado por engano para que base fique limpa, onde o sistema permite remover registros de titulares que foram criados incorretamente ou não são mais necessários, garantindo integridade referencial através de validações que previnem exclusão de titulares atualmente vinculados a unidades. O cenário principal de uso ocorre quando gestor identifica titular que foi cadastrado por engano e não está vinculado a nenhuma unidade, permitindo executar exclusão que marca registro como removido sem deletá-lo fisicamente do banco de dados preservando histórico para auditoria. Os critérios de aceitação incluem implementação de soft delete onde titular é marcado com flag is_deleted=true ao invés de ser fisicamente removido da base de dados, restrição de exclusão permitindo apenas quando titular não está vinculado a nenhuma unit onde sistema valida ausência de relacionamentos ativos antes de permitir operação, e exigência de confirmação obrigatória através de diálogo que alerta gestor sobre irreversibilidade da ação e solicita confirmação explícita antes de prosseguir. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint DELETE /api/holders/{id} com validações de vínculos e soft delete) e GEOWEB (botão de exclusão com modal de confirmação e tratamento de erros), garantindo rastreabilidade com RF-086 (Exclusão de Titulares), onde titulares excluídos não aparecem em listagens normais mas permanecem no banco permitindo recuperação se necessário, incluindo audit log registrando quem executou exclusão e quando, e mensagens de erro claras quando exclusão é bloqueada devido a vínculos existentes orientando usuário a primeiro desvincular unidades.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
