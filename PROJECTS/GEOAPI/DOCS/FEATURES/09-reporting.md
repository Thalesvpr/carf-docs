---
type: leaf
status: review
updated: 2026-02-08
---

# Reporting Feature

A feature de relatorios permite exportacao de dados do sistema em multiplos formatos incluindo PDF para relatorios formais, CSV para analise em planilhas, Shapefile para compatibilidade com sistemas GIS legados e GeoJSON para integracao com ferramentas geoespaciais modernas. Exportacoes grandes sao processadas de forma assincrona via Hangfire com notificacao ao usuario quando o arquivo estiver pronto para download.

## User Stories

US-080 Exportar Relatorio PDF: o analista solicita geracao de relatorio em PDF contendo dados de unidades, titulares e comunidades filtrados por criterios especificos. O relatorio e gerado de forma assincrona e disponibilizado para download via URL pre-assinada do S3.

US-081 Exportar Dados CSV: o analista solicita exportacao de dados tabulares em formato CSV para analise externa em planilhas. Os dados podem ser filtrados por comunidade, status e periodo.

US-082 Exportar Dados Geoespaciais: o analista solicita exportacao em Shapefile ou GeoJSON contendo geometrias de unidades e comunidades com propriedades associadas. O formato Shapefile gera arquivo ZIP contendo os componentes obrigatorios (.shp, .dbf, .shx, .prj).

US-083 Exportar com Fotos e Documentos: o analista solicita exportacao incluindo fotos de fachada e documentos vinculados, gerando pacote ZIP com estrutura de pastas organizada por unidade contendo dados e arquivos associados.

## Regras de Negocio

RN-080: exportacoes com mais de 1000 registros sao processadas de forma assincrona via Hangfire, retornando jobId para acompanhamento. RN-081: relatorios PDF sao gerados via biblioteca de geracao de PDF com template padronizado contendo cabecalho institucional, dados do tenant e informacoes solicitadas. RN-082: Shapefiles sao gerados em EPSG:4326 (WGS84) com arquivo .prj correspondente. RN-083: exportacoes com fotos e documentos empacotam binarios baixados do S3 em estrutura de pastas dentro do ZIP. RN-084: URLs pre-assinadas para download de relatorios gerados expiram em 24 horas. RN-085: dados exportados respeitam o isolamento por tenant, incluindo apenas registros do tenant do usuario autenticado.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Exportar PDF | nao | nao | sim | sim | sim | sim |
| Exportar CSV | nao | nao | sim | sim | sim | sim |
| Exportar GeoJSON | sim | sim | sim | sim | sim | sim |
| Exportar Shapefile | nao | nao | sim | sim | sim | sim |
| Exportar com fotos | nao | nao | sim | sim | sim | sim |
