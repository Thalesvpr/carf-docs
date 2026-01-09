---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: compatibility
---

# RF-045: Anexar Documentos à Comunidade

Usuários com role ADMIN podem anexar documentos administrativos à comunidade onde upload suporta formatos PDF DOC DOCX XLS XLSX validando tipo MIME e tamanho máximo configurável (ex: 10MB por arquivo) com feedback de progresso durante upload, tipos de documentos classificados através de enum ou tabela de referência incluindo categorias como Decreto municipal/estadual Portaria de regularização Ata de reunião comunitária Laudo técnico Planta cadastral e outros tipos relevantes para contexto de regularização fundiária, funcionalidade de download de documentos anexados disponível para usuários autorizados onde clique em documento baixa arquivo original preservando nome e extensão com streaming eficiente para arquivos grandes e log de acesso registrando quem baixou quando, implementação em módulos GEOWEB e GEOAPI com componente de upload drag-and-drop listagem de documentos anexados com metadata (nome tipo tamanho data upload usuário) armazenamento em object storage (S3 Azure Blob) e URLs assinadas temporariamente para download seguro.

---

**Última atualização:** 2025-12-30
