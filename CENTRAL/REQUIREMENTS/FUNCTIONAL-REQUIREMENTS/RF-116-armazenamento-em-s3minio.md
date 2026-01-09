---
modules: [GEOAPI]
epic: scalability
---

# RF-116: Armazenamento em S3/MinIO

Este requisito especifica que arquivos documentos e fotos devem ser armazenados em object storage compatível com S3 ao invés de filesystem local, onde o sistema pode utilizar Amazon S3 MinIO ou qualquer serviço compatível com API S3, garantindo escalabilidade durabilidade e separação entre aplicação e storage. O sistema deve implementar integração completa com S3-compatible storage através de SDK apropriado configurado com credenciais e endpoint do serviço, permitindo operações de upload download e deleção de objetos via API S3 padrão. Para downloads seguros, o sistema deve gerar URLs presigned temporárias com expiração configurável, onde cada URL permite acesso ao arquivo por tempo limitado sem expor credenciais ou permitir acesso permanente, garantindo segurança mesmo se URL vazar. Os arquivos devem ser organizados hierarquicamente por tenant e entidade usando prefixos de chave apropriados, onde estrutura típica seria tenant-id/entity-type/entity-id/filename, facilitando gestão backup e aplicação de políticas por tenant. O sistema deve configurar metadados adequados em cada objeto incluindo Content-Type cache-control e custom metadata para rastreabilidade. A funcionalidade deve ser implementada no módulo GEOAPI através de camada de abstração de storage que permite trocar provider sem alterar lógica de negócio.

---

**Última atualização:** 2025-12-30