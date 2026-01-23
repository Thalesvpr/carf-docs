---
type: readme
status: review
updated: 2026-01-22
---

# PROCESS-WORKFLOWS

Fluxos de trabalho end-to-end documentando sequencias de atividades coordenadas entre atores humanos e sistema, atravessando multiplos aggregates para completar processos de negocio completos desde configuracao inicial ate certificacao final.

O workflow de [integracao WMS](./01-wms-integration-workflow.md) documenta consumo de ortofotos via servidores WMS/WMTS conforme padroes OGC, desde levantamento aerofotogrametrico ate publicacao de tiles para visualizacao no sistema. O workflow de [coleta em campo](./02-field-data-collection-workflow.md) descreve o processo de cadastramento de unidades e titulares usando dispositivo movel com suporte offline.

O workflow de [sincronizacao offline](./03-offline-sync-workflow.md) detalha a reconciliacao bidirecional entre dispositivo movel e servidor quando conexao e restabelecida, incluindo resolucao de conflitos. O workflow de [validacao por analista](./04-analyst-validation-workflow.md) cobre revisao e aprovacao de dados coletados em campo pelo analista tecnico.

O workflow de [topografia](./05-topography-workflow.md) documenta levantamento topografico com receptor GNSS para georreferenciamento preciso de vertices. E o workflow de [legitimacao](./06-legitimation-workflow.md) descreve o processo completo de legitimacao fundiaria conforme Lei 13.465/2017, desde solicitacao ate emissao de certificado.

<!-- CARF-INDEX-START -->
## Documentos

- [[CENTRAL/REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/01-wms-integration-workflow|WMS Integration Workflow]]
- [[CENTRAL/REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/02-field-data-collection-workflow|Field Data Collection Workflow]]
- [[CENTRAL/REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/03-offline-sync-workflow|Offline Sync Workflow]]
- [[CENTRAL/REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/04-analyst-validation-workflow|Analyst Validation Workflow]]
- [[CENTRAL/REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/05-topography-workflow|Topography Workflow]]
- [[CENTRAL/REQUIREMENTS/USE-CASES/PROCESS-WORKFLOWS/06-legitimation-workflow|Legitimation Workflow]]

<!-- CARF-INDEX-END -->
