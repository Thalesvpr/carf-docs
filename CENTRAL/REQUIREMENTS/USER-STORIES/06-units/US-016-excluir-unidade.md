---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-016: Excluir Unidade

Como gestor, quero excluir unidades cadastradas por engano para que base de dados fique limpa, onde o sistema permite remover unidades que foram criadas incorretamente ou não são mais relevantes, garantindo que apenas gestores com permissões adequadas possam executar esta operação crítica e que a exclusão preserve histórico para auditoria. O cenário principal de uso inicia quando um gestor identifica uma unidade que precisa ser removida e acessa a opção de exclusão, permitindo que o sistema apresente confirmação obrigatória detalhando as implicações da exclusão antes de executar a operação. Os critérios de aceitação incluem implementação de soft delete onde a unidade é marcada com flag is_deleted=true ao invés de ser fisicamente removida do banco de dados preservando histórico, restrição de permissão onde apenas usuários com role MANAGER ou superior podem executar exclusão de unidades, exigência de confirmação obrigatória através de modal ou diálogo que lista informações da unidade e potenciais impactos antes de confirmar, e registro completo no audit log incluindo quem executou a exclusão, quando, e opcionalmente motivo da remoção. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint DELETE /api/units/{id} que executa soft delete e valida permissões) e GEOWEB (botão de exclusão com modal de confirmação e mensagens de feedback), garantindo rastreabilidade com RF-055 (Exclusão de Unidades) e UC-001 (Caso de Uso de Gestão de Unidades), onde unidades excluídas não aparecem em listagens e consultas normais mas permanecem no banco para fins de auditoria e podem ser recuperadas por administradores se necessário, incluindo tratamento de dependências como holders vinculados e documentos anexados que também são marcados como excluídos em cascata.

---

**Última atualização:** 2025-12-30