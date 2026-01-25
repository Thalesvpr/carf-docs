---
type: glossary
status: approved
updated: 2026-01-25
category: sistemas
---

# Sistemas

Definicoes dos sistemas que compoem o CARF.

## Backend (GEOAPI)

Sistema central que:
- Recebe e processa ortofotos
- Armazena dados em bucket
- Fornece APIs para Plugin e App
- Recebe e processa sincronizacao

**Tecnologias:**
- API REST
- PostgreSQL com PostGIS
- Integracao com S3/MinIO

**Endpoints principais:**
- `/api/ortofotos` - Gerenciamento de ortofotos
- `/api/poligonos` - Gerenciamento de poligonos
- `/api/pacotes` - Pacotes para campo

## Keycloak

Identity Provider que:
- Autentica todos os usuarios
- Emite tokens JWT
- Gerencia roles e permissoes
- Inclui `tenant_id` nos claims

**Funcionalidades:**
- OAuth2/OIDC
- PKCE para apps desktop/mobile
- Gerenciamento de usuarios e grupos
- Claims customizados (tenant_id)

## App REURBCAD

Aplicativo mobile para Agentes de Campo que:
- Funciona offline-first
- Armazena dados localmente (WatermelonDB)
- Exibe mapas com GPS
- Permite cadastros e sincronizacao

**Tecnologias:**
- React Native
- WatermelonDB (banco local)
- Mapas georreferenciados

**Funcionalidades:**
- Download de pacote temporario
- Visualizacao de mapa com GPS
- Formularios de cadastro
- Coleta de assinatura digital
- Sincronizacao PUSH/PULL

## Bucket (S3/MinIO)

Armazenamento de objetos que:
- Guarda ortofotos (originais e reduzidas)
- Organiza por TENANT
- Fornece URLs presigned para acesso

**Estrutura:**
```
/{tenant_id}/
  ├── ortofotos/
  │   └── {ano}/{mes}/
  │       ├── original/
  │       ├── otimizada/
  │       └── tiles/
  ├── documentos/
  └── fotos/
```

**Seguranca:**
- URLs presigned com expiracao
- Isolamento por TENANT
- Acesso via backend apenas
