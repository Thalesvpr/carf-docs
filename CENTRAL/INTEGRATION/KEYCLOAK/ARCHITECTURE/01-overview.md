# Visão Geral da Arquitetura

Sistema CARF utiliza Keycloak como provedor centralizado de autenticação e autorização implementando padrões OAuth2 e OpenID Connect para seis aplicações: GEOWEB portal web React para analistas, REURBCAD app mobile React Native para coleta em campo, GEOAPI backend .NET com API REST, GEOGIS plugin QGIS para análises espaciais, WEBDOCS portal de documentação Astro, e ADMIN console administrativo Next.js.

Single Sign-On permite login único que propaga sessão entre todas aplicações via cookie de sessão Keycloak onde usuário autentica em qualquer aplicação e automaticamente fica autenticado nas demais sem necessidade de reentrada de credenciais. Single Logout invalida sessão Keycloak e desloga usuário de todos aplicativos simultaneamente garantindo segurança em cenários de dispositivo compartilhado ou encerramento de expediente.

OAuth2 define framework de autorização especificando o que usuário pode fazer através de scopes e permissions enquanto OpenID Connect estende OAuth2 adicionando camada de autenticação definindo quem é o usuário através de id_token JWT contendo claims de identidade. Custom claims tenant_id, allowed_tenants e roles são configurados via protocol mappers no realm Keycloak e incluídos em todos os tokens para autorização granular.

Backend GEOAPI valida tokens JWT usando public key do Keycloak obtida via JWKS endpoint permitindo validação offline sem comunicação com Keycloak a cada request melhorando performance e resiliência. Middleware extrai claims do token e configura variável de sessão PostgreSQL para Row Level Security garantindo isolamento de dados entre tenants na camada de banco de dados.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
