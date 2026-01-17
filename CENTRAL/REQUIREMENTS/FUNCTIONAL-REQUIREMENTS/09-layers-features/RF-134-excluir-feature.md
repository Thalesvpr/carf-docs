---
modules: [GEOAPI, REURBCAD]
epic: performance
---

# RF-134: Excluir Feature

Este requisito especifica que usuários autorizados devem poder excluir features geográficas do sistema através de processo controlado que previne remoções acidentais e mantém rastreabilidade, onde exclusão é implementada via soft delete preservando dados para auditoria. O sistema deve implementar soft delete marcando feature como excluída através de campo deleted_at ou status ao invés de remover registro fisicamente do banco de dados, permitindo auditoria futura recuperação se necessário e conformidade com requisitos de governança de dados. Antes de executar exclusão, o sistema deve exigir confirmação explícita do usuário através de diálogo ou modal que previne deleções acidentais, onde confirmação pode incluir descrição da feature sendo removida e potencial impacto da operação. Após confirmação e execução da exclusão lógica, a feature deve ser imediatamente removida da renderização no mapa e de listagens padrão, garantindo que usuários não vejam mais elemento excluído em visualizações normais mas dados permaneçam acessíveis através de queries administrativas ou de auditoria. O sistema deve registrar operação no log incluindo identificação do usuário executor timestamp identificador da feature e contexto da exclusão. A funcionalidade deve estar disponível nos módulos GEOWEB através de opções de exclusão em popups ou painéis de feature e GEOAPI via endpoint DELETE com validações de permissão.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
