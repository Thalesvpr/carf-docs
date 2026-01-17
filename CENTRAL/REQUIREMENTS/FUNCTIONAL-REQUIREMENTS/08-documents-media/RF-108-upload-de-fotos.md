---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# RF-108: Upload de Fotos

Este requisito especifica que usuários devem poder fazer upload de fotos no sistema através de interface web ou mobile, onde o sistema deve suportar os formatos JPG PNG HEIC garantindo compatibilidade com diferentes dispositivos e câmeras, incluindo formatos modernos utilizados em dispositivos Apple. O sistema deve validar que o tamanho máximo de cada arquivo seja de 20MB, rejeitando uploads que excedam este limite com mensagem de erro clara e orientações para o usuário sobre compressão ou redimensionamento. Após o upload bem-sucedido, o sistema deve automaticamente gerar miniatura da foto para otimizar exibição em listas e galerias, onde a miniatura é criada em dimensões reduzidas mantendo proporções e qualidade adequada para visualização rápida, sendo armazenada separadamente da imagem original. O processo de upload deve incluir validação de integridade do arquivo, verificação de tipo MIME real versus extensão declarada, e feedback visual de progresso para uploads de arquivos maiores. A funcionalidade deve estar disponível nos módulos GEOWEB para uploads via navegador, REURBCAD para capturas mobile em campo, e GEOAPI fornecendo endpoints multipart/form-data para processamento backend.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
