---
type: leaf
status: approved
updated: 2026-02-07
---

# LegitimationCertificate

Entidade representando certidao de legitimacao fundiaria, documento oficial emitido apos aprovacao do processo formalizando o reconhecimento do direito de propriedade conforme Lei 13.465/2017. Herda de BaseEntity fornecendo auditoria temporal.

## Papel no Dominio

A certidao e o produto final do processo de legitimacao. Contem identificacao completa do imovel e proprietarios, fundamento legal, e e gerada em PDF para registro em cartorio de imoveis. O numero da certidao e unico sequencial e permite verificacao de autenticidade.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| RequestId | Guid | nao | FK para LegitimationRequest que fundamenta a emissao. |
| CertificateNumber | string | nao | Numero unico sequencial no formato CERT-AAAA-NNNNN. Globalmente unico. |
| Situation | string | nao | Situacao da area: COVERED (coberta integralmente), CONFRONTING (confrontante), BOTH (ambas). |
| IssuedAt | DateTime | nao | Data e hora de emissao. |
| IssuedBy | Guid | nao | Account com role MANAGER que autorizou a emissao. |
| PdfPath | string | nao | Caminho S3 do PDF da certidao gerado automaticamente. |

## Relacionamentos

Pertence a um LegitimationRequest (obrigatorio). Atraves do request, acessa a Unit e seus Holders para compor o conteudo da certidao.

## Invariantes de Negocio

CertificateNumber unico globalmente (nao por tenant). IssuedBy deve ter role MANAGER ou superior. O processo vinculado deve estar no status APPROVED no momento da emissao. Apos emissao, o status do processo transiciona para TITLE_ISSUED. O PDF e gerado automaticamente com dados do imovel, titular, fundamento legal e selo oficial.

## Domain Events

CertificateIssuedEvent emitido ao criar, notificando o requerente por email com o PDF anexo.
