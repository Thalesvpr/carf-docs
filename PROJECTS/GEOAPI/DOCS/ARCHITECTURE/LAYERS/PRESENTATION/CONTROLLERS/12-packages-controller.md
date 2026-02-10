---
type: leaf
status: review
updated: 2026-02-08
---

# Packages Controller

O PackagesController gerencia pacotes de dados para download pelo app mobile REURBCAD. A rota base e /api/packages. Os pacotes contem tiles de ortofoto, poligonos GeoJSON e metadados pre-cadastrados necessarios para operacao em campo offline.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/packages/field | Metadados do pacote | 200 | 403 | field-coordinator, field-cadastrator |
| GET | /api/packages/field/{id}/download | Download binario do pacote | 200 | 404 | field-coordinator, field-cadastrator |

## Comportamento

O endpoint de metadados despacha GetFieldPackageQuery que monta informacoes do pacote baseado nas comunidades autorizadas do usuario. O response retorna packageId, sizeBytes (estimado), communities (array de nomes), createdAt e downloadUrl (URL pre-assinada do S3 para download unico). O pacote contém tiles de ortofoto para as comunidades autorizadas, poligonos GeoJSON de unidades e comunidades existentes, e metadados pre-cadastrados. O endpoint de download retorna binario do pacote compactado em formato ZIP com Content-Type application/zip. A URL pre-assinada expira apos primeiro uso para evitar compartilhamento indevido dos dados de campo.

## Autorizacao

Ambos os endpoints sao restritos a roles field-coordinator e field-cadastrator pois representam funcionalidade exclusiva do app mobile de campo. O conteudo do pacote e filtrado pelas comunidades autorizadas da equipe do usuario, garantindo que cada agente receba apenas os dados necessarios para seu trabalho.
