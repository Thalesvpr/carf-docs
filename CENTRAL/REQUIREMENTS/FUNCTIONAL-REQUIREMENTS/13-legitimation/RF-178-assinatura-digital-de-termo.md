---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: security
---

# RF-178: Assinatura Digital de Termo

O sistema possibilita assinatura digital qualificada de Termos de Legitimação através de integração com infraestrutura de chaves públicas brasileira ICP-Brasil ou soluções similares compatíveis com padrões internacionais de certificação digital, garantindo autenticidade, integridade e validade jurídica dos documentos emitidos. A funcionalidade implementa validação rigorosa de certificados digitais que verifica cadeia de certificação, período de validade, revogação em LCR ou OCSP, e conformidade com políticas de assinatura apropriadas ao tipo de documento, assegurando que apenas assinaturas válidas e de autoridades competentes sejam aceitas pelo sistema. Após assinatura bem-sucedida, o sistema armazena permanentemente arquivo PDF assinado incluindo representação criptográfica da assinatura digital embarcada no documento, preservando evidências que permitem verificação posterior de autenticidade mesmo após expiração do certificado do signatário, conforme estabelecido por padrões como PAdES (PDF Advanced Electronic Signatures). Esta capacidade de assinatura digital reduz significativamente tempo e custos associados a processos convencionais de assinatura manuscrita, elimina necessidade de deslocamentos físicos de documentos entre setores ou instituições, e confere maior segurança jurídica aos títulos emitidos através de mecanismos criptográficos robustos de não repúdio.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
