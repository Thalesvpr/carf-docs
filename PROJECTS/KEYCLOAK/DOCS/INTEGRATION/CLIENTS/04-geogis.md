---
type: leaf
status: review
updated: 2026-01-19
---

# Client GEOGIS

Plugin QGIS para análises espaciais configurado como confidential client com service account enabled permitindo Client Credentials flow para autenticação server-to-server sem contexto de usuário.

Client secret gerado com openssl rand -base64 32 armazenado de forma segura em QSettings encrypted do QGIS. Plugin executa POST direto para token endpoint enviando grant_type client_credentials, client_id geogis, e client_secret obtendo access_token sem user claims.

Token contém client_id geogis, allowed-origins configurados, e resource_access com roles específicos do service account como gis-reader e gis-writer definidos em Service Account Roles no Keycloak Admin Console. Roles controlam acesso a operações WFS/WMS no GEOAPI.

Também suporta standard flow com PKCE para cenários onde usuário humano precisa autenticar. Plugin abre browser local em http://localhost:random_port/ para capturar callback OAuth, útil quando operações GIS precisam de contexto de tenant específico do usuário.
