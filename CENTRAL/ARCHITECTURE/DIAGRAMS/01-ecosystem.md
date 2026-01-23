---
type: leaf
status: current
updated: 2026-01-22
---

# Ecossistema CARF

Visao geral de todos os sistemas do ecossistema CARF e suas conexoes, mostrando como usuarios interagem com aplicacoes frontend que consomem o backend central e servicos de autenticacao.

```mermaid
flowchart TB
    subgraph Usuarios["Usuarios"]
        Analista["Analista<br/>Portal Web"]
        Agente["Agente Campo<br/>App Mobile"]
        Admin["Administrador<br/>Console Admin"]
        GIS["Especialista GIS<br/>Plugin QGIS"]
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
    end

    subgraph Data["Persistencia"]
        POSTGRES[("PostgreSQL<br/>+ PostGIS")]
        STORAGE[("Object Storage<br/>Documentos/Midias")]
    end

    subgraph External["Servicos Externos"]
        WMS["WMS/WMTS<br/>Camadas Base"]
    end

    Analista --> GEOWEB
    Agente --> REURBCAD
    Admin --> ADMINUI
    GIS --> GEOGIS

    GEOWEB --> GEOAPI
    REURBCAD --> GEOAPI
    ADMINUI --> GEOAPI
    GEOGIS --> GEOAPI
    WEBDOCS --> GEOAPI

    GEOWEB --> KEYCLOAK
    REURBCAD --> KEYCLOAK
    ADMINUI --> KEYCLOAK
    GEOGIS --> KEYCLOAK

    GEOAPI --> KEYCLOAK
    GEOAPI --> POSTGRES
    GEOAPI --> STORAGE
    GEOAPI --> WMS
```
