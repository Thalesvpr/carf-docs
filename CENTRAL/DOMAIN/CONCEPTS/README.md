---
type: readme
status: approved
updated: 2026-01-24
---

# CONCEPTS

Entidades conceituais do dominio REURB que formam o vocabulario ubiquo do sistema CARF. Cada arquivo descreve um conceito de negocio com definicao, contexto e relacoes.

Os conceitos centrais sao [Unit](./02-unit.md) (unidade habitacional), [Holder](./03-holder.md) (titular/ocupante) e [Community](./04-community.md) (assentamento). A hierarquia espacial completa e: Community > [Block](./12-block.md) (quadra) > [Plot](./13-plot.md) (lote) > [Building](./38-building.md) (edificacao) > Unit. O fluxo de legitimacao envolve [LegitimationRequest](./25-legitimation-request.md), [LegitimationResponse](./26-legitimation-response.md) e [LegitimationCertificate](./27-legitimation-certificate.md).

Multi-tenancy e definido por [Tenant](./07-tenant.md) e [BucketTenant](./36-bucket-tenant.md). Georreferenciamento usa [Ortofoto](./35-ortofoto.md) e [AuthenticationKey](./37-authentication-key.md) para o Plugin QGIS.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (37)

| Documento | Status |
|-----------|--------|
| [Unidade Habitacional](./02-unit.md) | ✓ |
| [Titular](./03-holder.md) | ⚠ |
| [Comunidade](./04-community.md) | ⚠ |
| [Contestacao](./05-contestation.md) | ⚠ |
| [Templates de Documento](./06-pdf-templates.md) | ⚠ |
| [Tenant](./07-tenant.md) | ⚠ |
| [Usuario](./08-account.md) | ⚠ |
| [Equipe](./09-team.md) | ⚠ |
| [Membro de Equipe](./10-team-member.md) | ⚠ |
| [Autorizacao de Comunidade](./11-community-authorization.md) | ⚠ |
| [Quadra](./12-block.md) | ⚠ |
| [Lote](./13-plot.md) | ⚠ |
| [Documento](./14-document.md) | ⚠ |
| [Anotacao](./15-annotation.md) | ⚠ |
| [Vinculo Unidade-Titular](./16-unit-holder.md) | ⚠ |
| [Registro de Sincronizacao](./17-sync-log.md) | ⚠ |
| [Log de Auditoria](./18-audit-log.md) | ⚠ |
| [Topografo](./19-surveyor.md) | ⚠ |
| [Ponto Topografico](./20-survey-point.md) | ⚠ |
| [Estacao RBMC](./21-rbmc-station.md) | ⚠ |
| [Processamento de Levantamento](./22-survey-processing.md) | ⚠ |
| [Monografia de Marco](./23-monograph.md) | ⚠ |
| [Memorial Descritivo](./24-descriptive-memorial.md) | ⚠ |
| [Processo de Legitimacao](./25-legitimation-request.md) | ⚠ |
| [Parecer de Legitimacao](./26-legitimation-response.md) | ⚠ |
| [Certidao de Legitimacao](./27-legitimation-certificate.md) | ⚠ |
| [Planta de Legitimacao](./28-legitimation-plan.md) | ⚠ |
| [Servidor WMS](./29-wms-server.md) | ⚠ |
| [Camada WMS](./30-wms-layer.md) | ⚠ |
| [Camada Vetorial](./31-layer.md) | ⚠ |
| [Elemento de Camada](./32-layer-feature.md) | ⚠ |
| [Sessao](./33-session.md) | ⚠ |
| [Chave de API](./34-api-key.md) | ⚠ |
| [Ortofoto](./35-ortofoto.md) | ⚠ |
| [Bucket por Tenant](./36-bucket-tenant.md) | ⚠ |
| [Authentication Key](./37-authentication-key.md) | ⚠ |
| [Edificacao](./38-building.md) | ✓ |

<!-- CARF-INDEX-END -->
