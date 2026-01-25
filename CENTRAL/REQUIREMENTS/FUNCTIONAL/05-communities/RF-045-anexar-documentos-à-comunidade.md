---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-045: Anexar Documentos a Comunidade

## Descricao

Usuarios com role ADMIN podem anexar documentos administrativos a comunidade. Upload suporta formatos PDF, DOC, DOCX, XLS, XLSX validando tipo MIME e tamanho maximo configuravel. Tipos de documentos classificados atraves de enum incluindo Decreto municipal, Portaria de regularizacao, Ata de reuniao comunitaria, Laudo tecnico e Planta cadastral. Download disponivel para usuarios autorizados com streaming eficiente e log de acesso.

## Criterios de Aceitacao

1. Upload de PDF, DOC, XLS com validacao
2. Classificacao por tipo de documento
3. Armazenamento em object storage (S3)
4. Download com URLs assinadas temporariamente
5. Log de acesso registrando downloads

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-034, RF-008
