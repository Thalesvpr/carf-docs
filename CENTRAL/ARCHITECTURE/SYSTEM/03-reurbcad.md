---
type: leaf
status: approved
updated: 2026-01-24
---

# REURBCAD

Aplicativo mobile React Native Expo para operacao em campo usado por Agentes de regularizacao. Opera em modo offline-first permitindo trabalho em areas sem conectividade, sincronizando dados quando conexao esta disponivel. O Agente so tem acesso aos dados apos o Analista publicar seu trabalho no backend.

Stack mobile com React Native, Expo, WatermelonDB para banco local SQLite, react-native-maps para visualizacao de mapas e poligonos, expo-camera para fotos e leitura de QR Code, expo-location para GPS. Autenticacao OAuth2 PKCE com custom URL scheme e armazenamento seguro de tokens. Antes de operar offline, o agente realiza download unico e temporario do pacote contendo ortofoto e poligonos do tenant designado.

## Capacidades

Visualizacao de comunidades, quadras e lotes georreferenciados pelo Analista. Navegacao por GPS com orientacao no mapa. Captura de fotos geolocalizadas da unidade e documentos. Registro de titulares com validacao de CPF offline. Formularios de cadastro com assinatura digital. Leitura de QR Code para protocolos de ausencia. Fila de sincronizacao com retry automatico. Detalhes tecnicos no repositorio carf-reurbcad.
