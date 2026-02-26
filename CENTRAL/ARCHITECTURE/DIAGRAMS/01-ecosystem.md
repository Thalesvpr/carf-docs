---
type: leaf
status: review
updated: 2026-02-21
---

# Ecossistema CARF

Visao geral de todos os sistemas do ecossistema CARF e suas conexoes, mostrando como usuarios interagem com aplicacoes frontend que consomem o backend central e servicos de autenticacao. O Plugin QGIS (GEOGIS) exige autenticacao em duas etapas via Keycloak OAuth2 seguido de AUTHENTICATION KEY.

## Atores

| Ator | Descricao | Sistema Principal |
|------|-----------|-------------------|
| Operador Drone | Entrega ortofotos via portal de upload | GEOAPI (direto) |
| Analista | Opera o portal web para analise e aprovacao | REURBWEB |
| Analista GIS | Georreferencia poligonos via plugin QGIS | GEOGIS |
| Agente Campo | Executa cadastros em campo via app mobile | REURBCAD |
| Administrador | Gerencia usuarios, tenants e configuracoes | REURBMASTER |

## Aplicacoes Frontend

| Sistema | Tecnologia | Funcao |
|---------|-----------|--------|
| REURBWEB | React SPA | Portal web de analise e gestao |
| REURBCAD | React Native | App mobile para operacao em campo |
| REURBMASTER | React SPA | Console de administracao |
| GEOGIS | Plugin QGIS | Georreferenciamento de poligonos |
| WEBDOCS | Astro/Starlight | Documentacao publica |

## Backend e Servicos

O backend central e o GEOAPI, uma API REST em .NET 9. Todas as aplicacoes frontend consomem o GEOAPI. A camada de identidade e composta pelo Keycloak (OAuth2/OIDC) e pelo mecanismo de AUTHENTICATION KEY usado exclusivamente pelo plugin QGIS.

## Persistencia

Os dados sao armazenados em PostgreSQL com extensao PostGIS para dados geoespaciais. Arquivos pesados como ortofotos, documentos e fotos ficam em bucket S3/MinIO segregado por tenant.

## Conexoes

Todas as aplicacoes frontend autenticam via Keycloak, exceto o GEOGIS que requer autenticacao dupla (Keycloak mais AUTHENTICATION KEY). Todas as aplicacoes consomem o GEOAPI, que por sua vez acessa PostgreSQL, bucket S3/MinIO e servicos WMS/WMTS para camadas base cartograficas.
