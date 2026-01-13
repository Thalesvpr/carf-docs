---
modules: [GEOWEB]
epic: audit
---

# RF-120: Versionamento de Documentos

Este requisito especifica que o sistema deve manter histórico completo de versões de documentos permitindo rastreamento de alterações ao longo do tempo, onde cada re-upload de documento com mesmo identificador ou substituição de arquivo existente cria nova versão ao invés de sobrescrever arquivo anterior. O sistema deve preservar versões antigas indefinidamente ou conforme política de retenção configurada, armazenando cada versão como objeto separado no storage S3/MinIO com referências adequadas no banco de dados que vinculam todas versões ao mesmo documento lógico. Cada versão deve ter metadados próprios incluindo número de versão sequencial, timestamp de criação, usuário responsável pelo upload e opcionalmente comentário descrevendo mudanças realizadas, permitindo auditoria completa de evolução do documento. O sistema deve fornecer funcionalidade de restauração permitindo que usuários autorizados revertem documento para versão anterior selecionada, onde versão escolhida se torna versão ativa corrente e operação de restauração é registrada no histórico como nova entrada. A interface deve exibir lista de versões ordenada cronologicamente com opções para visualizar baixar ou restaurar cada versão. A funcionalidade deve ser implementada no módulo GEOAPI através de modelo de dados que suporta relacionamento um-para-muitos entre documento e versões.

---

**Última atualização:** 2025-12-30