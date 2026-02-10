---
type: leaf
status: review
updated: 2026-02-08
---

# LegitimationCertificateIssuedEvent

Domain event emitido quando certidao de legitimacao fundiaria e oficialmente emitida apos aprovacao de processo, indicando que documento legal foi gerado. Permite notificacao ao beneficiario, envio para impressao e registro em sistemas externos.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CertificateId | Guid | Identificador da certidao emitida. |
| CertificateNumber | string | Numero oficial unico no formato CERT-AAAA-NNNNN. |
| UnitId | Guid | Unidade habitacional legitimada. |
| RequestId | Guid | Solicitacao original que gerou certidao. |
| Situation | CertificateSituation | COVERED, CONFRONTING ou BOTH. |
| PdfPath | string | Caminho S3 do PDF da certidao. |
| IssuedBy | Guid | AccountId da autoridade que emitiu. |
| IssuedAt | DateTime | Data oficial de emissao. |
| TenantId | Guid | Tenant do contexto. |

## Handlers

| Handler | Acao |
| --- | --- |
| CertificateEmailHandler | Envia email ao beneficiario com PDF anexado. |
| CertificatePrintQueueHandler | Enfileira impressao em plotter se configurado. |
| CertificateMetricsHandler | Incrementa contador de certidoes emitidas no dashboard. |

## Contexto de Emissao

Emitido pelo agregado LegitimationRequest no metodo IssueCertificate() apos validacoes de aprovacao. A certidao recebe numero unico sequencial (CERT-AAAA-NNNNN) e PDF e gerado via IPdfGenerator.
