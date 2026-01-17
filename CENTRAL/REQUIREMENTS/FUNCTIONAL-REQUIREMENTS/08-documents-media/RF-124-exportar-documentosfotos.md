---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# RF-124: Exportar Documentos/Fotos

Este requisito especifica que usuários devem poder exportar todos os documentos e fotos associados a uma entidade específica em arquivo ZIP consolidado para backup compartilhamento ou arquivamento externo, onde sistema coleta todos os arquivos vinculados e os empacota em formato comprimido único. O arquivo ZIP gerado deve conter estrutura de pastas organizada hierarquicamente separando documentos e fotos em diretórios distintos, onde estrutura típica seria raiz/documentos/ e raiz/fotos/ com possível subdivisão adicional por tipo ou data, facilitando navegação no conteúdo extraído. O sistema deve incluir arquivo CSV de metadados dentro do ZIP contendo informações sobre cada arquivo incluindo nome original tipo tamanho data de upload usuário responsável e descrição se disponível, permitindo que receptor do ZIP compreenda contexto de cada arquivo sem acesso ao sistema. A geração do ZIP deve ocorrer de forma assíncrona para exportações grandes, onde sistema inicia processo em background fornece feedback de progresso ao usuário e notifica quando arquivo está pronto para download, evitando timeouts de requisição HTTP. O ZIP gerado deve ser disponibilizado via URL temporária com expiração configurada ou enviado diretamente como download. A funcionalidade deve estar disponível nos módulos GEOWEB através de botão de exportação e GEOAPI via endpoint que processa geração e retorna arquivo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
