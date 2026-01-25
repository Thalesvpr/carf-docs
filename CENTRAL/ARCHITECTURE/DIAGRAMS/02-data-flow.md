---
type: leaf
status: review
updated: 2026-01-24
---

# Fluxo de Dados

Ilustra como dados fluem entre sistemas seguindo as tres partes do workflow: entrega de ortofotos pelo Analista de Drone, georreferenciamento e publicacao pelo Analista GIS, e operacao em campo pelo Agente com sincronizacao offline.

```mermaid
flowchart TB
    subgraph PARTE1["PARTE 1: Entrega Ortofotos"]
        Drone["Analista Drone"]
        Upload["Link Upload<br/>Keycloak Auth"]
        Processa["Backend Processa<br/>Reduz Tamanho"]
        Bucket[("Bucket S3/MinIO<br/>por TENANT")]
    end

    subgraph PARTE2["PARTE 2: Georreferenciamento"]
        AnalistaGIS["Analista GIS"]
        Plugin["Plugin QGIS<br/>Keycloak + AUTH KEY"]
        Ortofotos["Acessa Ortofotos<br/>do TENANT"]
        Georref["Georreferencia<br/>Poligonos"]
        Publica["Publica no Backend"]
    end

    subgraph PARTE3["PARTE 3: Operacao Campo"]
        Agente["Agente Campo"]
        Download["Download Unico<br/>Temporario"]
        Pacote["Pacote: Ortofoto<br/>+ Poligonos"]
        LocalDB[("WatermelonDB<br/>SQLite Local")]
        Operacao["GPS + Acoes<br/>Formulario + Assinatura<br/>QR Code + Anexos"]
        Sync["Sincronizacao<br/>quando Online"]
    end

    subgraph Backend["Backend Central"]
        GEOAPI["GEOAPI<br/>.NET 9"]
        POSTGRES[("PostgreSQL<br/>+ PostGIS")]
    end

    %% PARTE 1: Drone -> Backend -> Bucket
    Drone -->|"Ortofoto"| Upload
    Upload --> Processa
    Processa -->|"Original + Reduzida"| Bucket

    %% PARTE 2: Plugin -> Georref -> Publica
    AnalistaGIS --> Plugin
    Plugin -->|"Acesso TENANT"| Ortofotos
    Bucket -.->|"Ortofotos"| Ortofotos
    Ortofotos --> Georref
    Georref -->|"Poligonos"| Publica
    Publica --> GEOAPI
    GEOAPI --> POSTGRES

    %% PARTE 3: Campo (so apos publicacao)
    Publica -.->|"Libera Dados"| Download
    Agente --> Download
    Download --> Pacote
    Bucket -.->|"Ortofoto"| Pacote
    POSTGRES -.->|"Poligonos"| Pacote
    Pacote --> LocalDB
    LocalDB --> Operacao
    Operacao --> LocalDB
    LocalDB -->|"Push"| Sync
    Sync --> GEOAPI
```
