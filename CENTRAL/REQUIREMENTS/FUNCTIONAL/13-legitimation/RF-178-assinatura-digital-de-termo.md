---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-178: Assinatura Digital de Termo

## Descricao

Sistema deve possibilitar assinatura digital qualificada de Termos de Legitimacao atraves de integracao com infraestrutura de chaves publicas brasileira ICP-Brasil, garantindo autenticidade, integridade e validade juridica dos documentos emitidos. Validacao rigorosa de certificados digitais verifica cadeia de certificacao, periodo de validade, revogacao em LCR ou OCSP, e conformidade com politicas de assinatura. Apos assinatura bem-sucedida, sistema armazena permanentemente arquivo PDF assinado com representacao criptografica embarcada conforme padrao PAdES (PDF Advanced Electronic Signatures), preservando evidencias para verificacao posterior de autenticidade mesmo apos expiracao do certificado do signatario.

## Criterios de Aceitacao

1. Integracao com ICP-Brasil
2. Validacao de certificado digital
3. Verificacao de revogacao via LCR/OCSP
4. Assinatura em padrao PAdES
5. Armazenamento permanente do PDF assinado

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-177
