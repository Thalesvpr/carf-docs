---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# RF-113: Excluir Foto

Este requisito estabelece que usuários autorizados devem poder excluir fotos do sistema através de processo controlado e auditável, onde a exclusão é implementada via soft delete marcando registro como excluído sem remoção física imediata do banco de dados, garantindo possibilidade de auditoria e recuperação. O sistema deve exigir confirmação explícita antes de executar exclusão, apresentando diálogo ou modal que previne remoções acidentais e permite que usuário revise decisão antes de confirmar. Após confirmação, além de marcar registro no banco como deleted, o sistema deve programar ou executar remoção do arquivo físico correspondente no storage S3/MinIO, liberando espaço de armazenamento mas mantendo registro de metadados para auditoria. A exclusão deve gerar entrada no log de auditoria incluindo identificação do usuário executor, timestamp, identificador da foto e contexto da operação. A interface deve remover imediatamente a foto da visualização após exclusão bem-sucedida, atualizando galeria sem necessidade de refresh manual. A funcionalidade deve estar disponível nos módulos GEOWEB através de botões de exclusão em galerias e GEOAPI via endpoint DELETE com validações de permissão adequadas.

---

**Última atualização:** 2025-12-30