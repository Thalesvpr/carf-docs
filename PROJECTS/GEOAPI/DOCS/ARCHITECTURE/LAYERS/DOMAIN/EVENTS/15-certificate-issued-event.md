---
type: leaf
status: review
updated: 2026-02-08
---

# CertificateIssuedEvent

Domain event emitido quando certidao de legitimacao e emitida apos aprovacao. Documento oficial reconhecendo direitos de propriedade gerado.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo. |
| CertificateId | Guid | Certidao. |
| CertificateNumber | string | CERT-AAAA-NNNNN. |
| UnitId | Guid | Unidade. |
| PdfPath | string | S3 do PDF. |
| TenantId | Guid | Tenant. |

## Handlers

| Handler | Acao |
| --- | --- |
| CertificateNotificationHandler | Notifica requerente. |
| CertificateRegistryHandler | Envia para cartorio se integrado. |
| CertificateMetricsHandler | Atualiza dashboard. |

## Contexto de Emissao

Emitido no metodo IssueCertificate(). Numero sequencial por tenant.
