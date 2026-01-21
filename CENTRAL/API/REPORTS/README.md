---
status: rejected
description: "Stub incompleto. Spec de API deve ter request/response schemas, exemplos, erros. Mover implementacao para PROJECTS/GEOAPI."
updated: 2026-01-15
---

# REPORTS

Schemas JSON para geração de relatórios do CARF.

O ReportGenerateRequest contém type (PDF, Excel, GeoJSON, Shapefile), scope (Unit, Community, Municipality), filters e template_id opcional. A geração é assíncrona, retornando job_id para polling de status.

Relatórios suportados: lista de unidades com filtros customizados, resumo de comunidade com demographics e mapas, relatório consolidado do município.

Processamento assíncrono com armazenamento temporário e expiração em 7 dias.

## Endpoints

- POST /api/reports/generate - Iniciar geração
- GET /api/reports/{job_id}/status - Consultar status
- GET /api/reports/{job_id}/download - Download quando completo
- GET /api/reports - Listar histórico de relatórios

## Schemas

- ReportGenerateRequest / ReportGenerateResponse
- ReportStatusRequest / ReportStatusResponse
- ReportDownloadRequest
- ReportListResponse


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-pdf-export](./01-pdf-export.md) | PDF Export |
| [02-data-export](./02-data-export.md) | Data Export |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/API/REPORTS/01-pdf-export.md|PDF Export]]
- ○ [[CENTRAL/API/REPORTS/02-data-export.md|Data Export]]

<!-- CARF-INDEX-END -->
