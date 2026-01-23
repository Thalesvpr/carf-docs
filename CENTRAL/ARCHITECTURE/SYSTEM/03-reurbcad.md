---
type: leaf
status: current
updated: 2026-01-22
---

# REURBCAD

Aplicativo mobile React Native Expo para coleta de dados cadastrais em campo usado por agentes de regularizacao. Opera em modo offline-first permitindo trabalho em areas sem conectividade, sincronizando dados quando conexao esta disponivel.

Stack mobile com React Native, Expo, WatermelonDB para banco local SQLite, react-native-maps para mapas offline, expo-camera para fotos e expo-location para GPS. Autenticacao OAuth2 PKCE com custom URL scheme e armazenamento seguro de tokens. Sincronizacao inteligente com resolucao de conflitos e priorizacao de uploads.

## Capacidades

Cadastro de unidades com desenho de geometria no mapa usando GPS ou digitalizacao manual. Captura de fotos geolocalizadas da unidade e documentos. Registro de titulares com validacao de CPF offline. Coleta de dados em formularios dinamicos. Fila de sincronizacao com retry automatico. Detalhes tecnicos em [PROJECTS/REURBCAD/DOCS/](../../../PROJECTS/REURBCAD/DOCS/README.md).
