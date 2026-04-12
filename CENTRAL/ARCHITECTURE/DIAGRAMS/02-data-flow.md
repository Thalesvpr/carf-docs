---
type: leaf
status: review
updated: 2026-02-21
---

# Fluxo de Dados

Ilustra como dados fluem entre sistemas seguindo as tres partes do workflow: entrega de ortofotos pelo Operador de Drone, georreferenciamento e publicacao pelo Analista GIS, e operacao em campo pelo Agente com sincronizacao offline.

## Parte 1: Entrega de Ortofotos

O Operador de Drone autentica via Keycloak e envia a ortofoto pelo link de upload. O backend processa o arquivo, gerando versao original e reduzida, e armazena ambas no bucket S3/MinIO segregado por tenant.

## Parte 2: Georreferenciamento

O Analista GIS autentica no plugin QGIS via Keycloak e AUTHENTICATION KEY, acessa as ortofotos do tenant no bucket e georreferencia poligonos (comunidades, quadras, lotes). Ao publicar, o plugin envia os poligonos ao GEOAPI, que persiste no PostgreSQL.

## Parte 3: Operacao em Campo

Somente apos a publicacao pelo Analista, a equipe de campo pode baixar um pacote temporario contendo ortofoto e poligonos. O pacote e armazenado localmente no WatermelonDB (SQLite). O agente opera com GPS, acoes no mapa, formularios e coleta de assinatura, tudo offline. Quando ha conectividade, o app sincroniza com o GEOAPI via push.

## Fluxo de Dados entre Sistemas

| Origem | Destino | Dados | Condicao |
|--------|---------|-------|----------|
| Operador Drone | GEOAPI | Ortofoto bruta | Autenticacao Keycloak |
| GEOAPI | Bucket S3/MinIO | Ortofoto original e reduzida | Processamento concluido |
| Bucket S3/MinIO | Plugin QGIS | Ortofotos do tenant | Autenticacao dupla |
| Plugin QGIS | GEOAPI | Poligonos georreferenciados | Publicacao |
| GEOAPI | PostgreSQL | Poligonos persistidos | Recebimento |
| PostgreSQL e Bucket | REURBCAD | Pacote (ortofoto e poligonos) | Publicacao concluida |
| REURBCAD | WatermelonDB local | Dados de campo | Operacao offline |
| WatermelonDB local | GEOAPI | Cadastros sincronizados | Conectividade disponivel |
