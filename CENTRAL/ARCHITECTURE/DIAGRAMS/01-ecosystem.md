---
type: leaf
status: review
updated: 2026-01-24
---

# Ecossistema CARF

Visao geral de todos os sistemas do ecossistema CARF e suas conexoes, mostrando como usuarios interagem com aplicacoes frontend que consomem o backend central e servicos de autenticacao. O Plugin QGIS (GEOGIS) exige autenticacao em duas etapas via Keycloak OAuth2 seguido de AUTHENTICATION KEY.

```mermaid
flowchart TB
    subgraph Usuarios["Usuarios"]
        AnalistaDrone["Analista Drone<br/>Entrega Ortofotos"]
        Analista["Analista<br/>Portal Web"]
        AnalistaGIS["Analista GIS<br/>Plugin QGIS"]
        Agente["Agente Campo<br/>App Mobile"]
        Admin["Administrador<br/>Console Admin"]
    end

    subgraph Frontend["Aplicacoes Frontend"]
        GEOWEB["GEOWEB<br/>React SPA"]
        REURBCAD["REURBCAD<br/>React Native"]
        ADMINUI["ADMIN<br/>React SPA"]
        GEOGIS["GEOGIS<br/>Plugin QGIS"]
        WEBDOCS["WEBDOCS<br/>Astro/Starlight"]
    end

    subgraph Backend["Backend"]
        GEOAPI["GEOAPI<br/>.NET 9 REST API"]
    end

    subgraph Identity["Identity"]
        KEYCLOAK["KEYCLOAK<br/>OAuth2/OIDC"]
        AUTHKEY["AUTHENTICATION KEY<br/>Chave Plugin"]
    end

    subgraph Data["Persistencia"]
        POSTGRES[("PostgreSQL<br/>+ PostGIS")]
        BUCKET[("Bucket S3/MinIO<br/>por TENANT")]
    end

    subgraph External["Servicos Externos"]
        WMS["WMS/WMTS<br/>Camadas Base"]
    end

    AnalistaDrone --> GEOAPI
    Analista --> GEOWEB
    AnalistaGIS --> GEOGIS
    Agente --> REURBCAD
    Admin --> ADMINUI

    GEOWEB --> GEOAPI
    REURBCAD --> GEOAPI
    ADMINUI --> GEOAPI
    GEOGIS --> GEOAPI
    WEBDOCS --> GEOAPI

    GEOWEB --> KEYCLOAK
    REURBCAD --> KEYCLOAK
    ADMINUI --> KEYCLOAK
    GEOGIS --> KEYCLOAK
    GEOGIS --> AUTHKEY

    GEOAPI --> KEYCLOAK
    GEOAPI --> POSTGRES
    GEOAPI --> BUCKET
    GEOAPI --> WMS
```
