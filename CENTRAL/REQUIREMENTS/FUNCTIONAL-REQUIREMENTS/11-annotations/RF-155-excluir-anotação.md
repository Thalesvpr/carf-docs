---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# RF-155: Excluir Anotação

Este requisito estabelece que usuários devem poder excluir anotações que não são mais relevantes ou foram criadas erroneamente através de processo controlado que previne remoções acidentais, onde exclusão é implementada via soft delete preservando dados para auditoria. O sistema deve implementar soft delete marcando anotação como excluída através de campo deleted_at ou status deleted ao invés de remover registro do banco de dados, permitindo rastreabilidade completa e possível recuperação se exclusão foi inadvertida, conforme práticas de governança de dados. Antes de executar exclusão, o sistema deve exigir confirmação explícita do usuário através de diálogo modal ou toast que apresenta resumo da anotação sendo removida incluindo texto e autor, onde usuário deve confirmar intenção através de botão de confirmação evitando deleções acidentais por cliques únicos não intencionais. Após confirmação e execução da exclusão lógica, a anotação deve ser imediatamente removida do mapa e de listagens padrão garantindo que não apareça mais em visualizações normais mas permaneça acessível através de interfaces administrativas ou queries de auditoria que incluem registros soft-deleted. O sistema deve registrar exclusão no log de auditoria incluindo identificação do usuário executor timestamp identificador da anotação e conteúdo removido. A funcionalidade deve estar disponível nos módulos GEOWEB através de opções de exclusão em popups ou listagens e GEOAPI via endpoint DELETE.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
