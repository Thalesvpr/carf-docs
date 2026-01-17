---
modules: [GEOAPI, GEOWEB, GEOGIS]
epic: security
---

# RF-003: Client Credentials Flow

Plugin QGIS (GEOGIS) deve utilizar fluxo OAuth2 Client Credentials para autenticação permitindo que aplicação desktop obtenha tokens de acesso sem interação direta do usuário onde autenticação ocorre via client_id e client_secret configuráveis armazenados de forma segura em arquivo de configuração local ou keychain do sistema operacional, obtenção de token ocorre automaticamente ao iniciar plugin enviando requisição POST para endpoint /token do Keycloak com grant_type=client_credentials incluindo credenciais cliente em header Authorization Basic ou corpo da requisição, renovação automática de token implementada detectando expiração iminente (ex: 5 minutos antes de exp claim) e solicitando novo access_token proativamente garantindo continuidade de operações sem interrupção para usuário, credenciais client_id e client_secret devem ser configuráveis via interface administrativa ou arquivo de configuração permitindo diferentes ambientes (desenvolvimento staging produção) sem necessidade de recompilar plugin.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
