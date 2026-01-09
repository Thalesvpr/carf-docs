---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: performance
---

# RF-064: Anexar Documentos a Unidade

O sistema deve permitir que usuários façam upload de documentos comprobatórios relacionados a unidades habitacionais, incluindo formatos PDF JPG PNG para acomodar diferentes tipos de documentação como contratos digitalizados, comprovantes escaneados, certidões e declarações. Cada documento pode ser classificado por tipo configurável no sistema (RG CPF COMPROVANTE_RESIDENCIA CONTRATO ESCRITURA DECLARACAO_POSSE OUTRO), permitindo organização sistemática e localização eficiente de documentação específica quando necessário. O sistema valida tamanho máximo de 10MB por arquivo prevenindo uploads excessivos que comprometam armazenamento e performance, apresentando mensagem clara quando limite é excedido e sugerindo compressão ou divisão de arquivos grandes. A validação de tipo MIME garante que apenas formatos permitidos sejam aceitos bloqueando uploads de tipos de arquivo não suportados ou potencialmente perigosos, onde cada documento anexado armazena metadados como nome original, tamanho, data de upload, usuário responsável e hash para verificação de integridade, garantindo rastreabilidade e autenticidade da documentação ao longo do tempo.

---

**Última atualização:** 2025-12-30
