---
type: leaf
status: approved
updated: 2026-02-07
---

# Realm Configuration

O realm CARF e criado como realm dedicado no Keycloak, isolando toda a configuracao de clients, users e roles do master realm. O display name "CARF - Sistema de Regularizacao Fundiaria" identifica o realm nas interfaces de usuario e e configuravel via Admin Console ou API.

## Configuracoes de Login

O realm define comportamento de autenticacao com auto-registro desabilitado (registrationAllowed: false) pois usuarios sao criados exclusivamente via ADMIN por coordenadores ou administradores. Login com email esta habilitado (loginWithEmailAllowed: true) permitindo autenticacao tanto por CPF quanto por email. Remember me esta ativo para estender sessoes. Recuperacao de senha esta habilitada (resetPasswordAllowed: true) com envio de email de reset. Verificacao de email esta desabilitada (verifyEmail: false).

## Configuracao de Tokens

Access Token Lifespan de 5 minutos (300 segundos) forca refresh frequente minimizando janela de exposicao. SSO Session Idle de 30 minutos (1800 segundos) encerra sessao apos inatividade. SSO Session Max de 10 horas (36000 segundos) limita duracao total independente de atividade. Offline Session Idle de 30 dias (2592000 segundos) atende REURBCAD em campo com scope offline_access. Refresh Token Max Reuse de 0 previne replay attacks.

## Clients OAuth2

Seis clients atendem as aplicacoes do ecossistema. O GEOWEB e public com Standard Flow e PKCE, redirect URIs para localhost:5173 (desenvolvimento) e geoweb.carf.gov.br (producao), Web Origins "+" para CORS automatico. O REURBCAD e public com PKCE e redirect URIs de custom scheme carf://callback para deep links mobile e portas Expo para desenvolvimento. O GEOAPI e bearer-only sem redirect URIs pois apenas valida tokens JWT recebidos dos frontends.

O GEOGIS e confidential com Standard Flow e Service Accounts habilitados, suportando tanto Authorization Code com PKCE quanto Client Credentials. O secret e gerado e armazenado em vault seguro, nunca no Git. O ADMIN e public com PKCE e client roles especificos manage-users, manage-tenants e view-audit-logs. O WEBDOCS e public com auth necessario apenas para secao /dev/ que requer role dev.

## Roles

Seis realm roles formam hierarquia em arvore via composite roles. Field-cadastrator e a base de campo sem heranca. Field-coordinator herda field-cadastrator adicionando menu mobile completo e reurbcad:manage-team. Analyst e ramo separado de escritorio para aprovacoes e relatorios. Manager herda analyst E field-coordinator unificando campo e escritorio. Admin herda manager com manage-users e view-audit-logs. Super-admin herda admin com manage-tenants e acesso cross-tenant. A defaultRole default-roles-carf e atribuida automaticamente a novos usuarios.

## Export e Import

A configuracao e exportada como realm-export.json com clients e roles (sem usuarios por LGPD), versionada no Git em CENTRAL/INTEGRATION/KEYCLOAK/. Import automatico via Docker Compose com volume mount em /opt/keycloak/data/import/ e flag --import-realm importa na primeira inicializacao e ignora se realm ja existe. Partial import via Admin Console permite importar recursos especificos sem sobrescrever configuracoes divergentes. Automacao via Admin REST API viabiliza GitOps com validacao, diff, aprovacao e aplicacao programatica.
