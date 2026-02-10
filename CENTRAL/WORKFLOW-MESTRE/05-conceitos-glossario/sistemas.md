---
type: glossary
status: approved
updated: 2026-02-07
category: sistemas
---

# Sistemas

Definicoes dos sistemas que compoem o CARF.

## Backend (GEOAPI)

Sistema central que recebe e processa ortofotos, armazena dados em bucket, fornece APIs para Plugin e App e recebe e processa sincronizacao.

**Tecnologias:** API REST, PostgreSQL com PostGIS, integracao com S3/MinIO.

**Endpoints principais:** /api/ortofotos para gerenciamento de ortofotos, /api/poligonos para gerenciamento de poligonos e /api/pacotes para pacotes de campo.

## Keycloak

Identity Provider que autentica todos os usuarios, emite tokens JWT, gerencia roles e permissoes e inclui tenant_id nos claims.

**Funcionalidades:** OAuth2/OIDC, PKCE para apps desktop/mobile, gerenciamento de usuarios e grupos, claims customizados (tenant_id).

## App REURBCAD

Aplicativo mobile para Agentes de Campo que funciona offline-first, armazena dados localmente (WatermelonDB), exibe mapas com GPS e permite cadastros e sincronizacao.

**Tecnologias:** React Native, WatermelonDB (banco local), mapas georreferenciados.

**Funcionalidades:** download de pacote temporario, visualizacao de mapa com GPS, formularios de cadastro, coleta de assinatura digital, sincronizacao PUSH/PULL.

## Bucket (S3/MinIO)

Armazenamento de objetos que guarda ortofotos (originais e reduzidas), organiza por TENANT e fornece URLs presigned para acesso.

**Estrutura:**

| Caminho | Conteudo |
|---------|----------|
| /{tenant_id}/ortofotos/{ano}/{mes}/original/ | Ortofoto original |
| /{tenant_id}/ortofotos/{ano}/{mes}/otimizada/ | Versao reduzida |
| /{tenant_id}/ortofotos/{ano}/{mes}/tiles/ | Tiles para visualizacao |
| /{tenant_id}/documentos/ | Documentos anexados |
| /{tenant_id}/fotos/ | Fotos de campo |

**Seguranca:** URLs presigned com expiracao, isolamento por TENANT, acesso via backend apenas.
