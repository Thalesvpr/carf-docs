---
type: leaf
status: approved
updated: 2026-02-07
---

# Customizacao de Realm

O realm CARF e o container principal de configuracao de identidade no Keycloak, isolando clients, users e roles do master realm. Toda customizacao e declarativa via realm-export.json (fonte da verdade em CENTRAL/INTEGRATION/KEYCLOAK/realm-export.json) e reproduzivel entre ambientes via --import-realm no startup do container.

## Clients OAuth2

O realm configura seis clients com tipos e flows distintos conforme modelo de ameacas de cada aplicacao.

Quatro clients sao public (sem client secret): GEOWEB (React SPA para analistas, Authorization Code com PKCE S256), REURBCAD (React Native mobile com deep links carf:// e suporte offline_access), ADMIN (Next.js para gestao administrativa com PKCE) e WEBDOCS (VitePress com auth para secao /dev/). O GEOAPI opera como bearer-only (.NET backend que apenas valida JWTs sem participar de flows de login). O GEOGIS e o unico confidential, suportando Standard Flow com PKCE para usuario humano e Client Credentials para comunicacao M2M, com secret armazenado em vault seguro.

Valid Redirect URIs incluem localhost para desenvolvimento e dominios de producao com wildcards. Web Origins configurados como "+" herdam automaticamente dos redirect URIs, permitindo CORS apenas de origens registradas.

## Roles e Hierarquia

Seis realm roles formam hierarquia em arvore (nao linear) via composite roles. Field-cadastrator e a base operacional de campo. Field-coordinator herda field-cadastrator e adiciona supervisao de equipe. Analyst e um ramo separado para escritorio (aprovacoes e relatorios), sem heranca de campo. Manager unifica ambos os ramos herdando analyst E field-coordinator. Admin herda manager e adiciona gestao de usuarios e tenants. Super-admin herda admin com capacidades cross-tenant.

Client roles complementam a hierarquia: o client admin define manage-users, manage-tenants e view-audit-logs, enquanto o client reurbcad define sync-data e manage-team. Role dev e transversal, sem heranca, concedendo acesso a ferramentas de desenvolvimento no WebDocs.

## User Attributes e Multi-Tenancy

Atributos customizados de usuario implementam multi-tenancy. O atributo tenants e um array multi-valued contendo identificadores dos municipios acessiveis ao usuario. O atributo current_tenant e single-valued indicando o tenant ativo na sessao. O atributo community_ids lista comunidades acessiveis dentro do tenant. O atributo cpf armazena o documento para validacao adicional.

Protocol mappers no scope carf-tenant transformam esses atributos em claims JWT: tenant_id (extraido de current_tenant, tipo String), allowed_tenants (extraido de tenants, tipo JSON multivalued) e community_ids (extraido de community_ids, tipo JSON multivalued). Todos adicionados a access token, ID token e userinfo.

## Authentication Flows

O flow carf-browser customiza o flow padrao. Auth-cookie verifica sessao existente como step ALTERNATIVE. O formulario de username e senha e REQUIRED. O CPF Validator pode ser adicionado como step adicional para validar formato do documento durante login.

## Configuracoes do Realm

Login permite email como username (loginWithEmailAllowed: true), recuperacao de senha (resetPasswordAllowed: true) e remember me. Auto-registro esta desabilitado (registrationAllowed: false) pois usuarios sao criados via ADMIN por coordenadores ou administradores. Verificacao de email tambem esta desabilitada.

Password policy exige minimo de 8 caracteres (length(8)), incluindo digito, lowercase, uppercase e caractere especial, alem de proibir uso do username. Brute force protection bloqueia apos 5 tentativas falhas (failureFactor: 5) com wait maximo de 15 minutos (maxFailureWaitSeconds: 900) e reset do contador apos 12 horas de inatividade.

## Export e Import

A configuracao completa e exportada via Admin Console selecionando Export clients ON, Export groups and roles ON, e Export users OFF (para evitar dados sensiveis LGPD). O JSON resultante e commitado no Git como Infrastructure as Code. Import automatico ocorre via Docker Compose montando volume em /opt/keycloak/data/import/ com flag --import-realm, que importa se realm nao existe e ignora se ja existe. Partial import via Admin Console permite importar recursos especificos sem sobrescrever configuracoes existentes.

Automacao via Admin REST API permite aplicar mudancas programaticamente usando endpoints PUT /admin/realms/carf com bearer token obtido do admin-cli, viabilizando GitOps workflow onde mudancas no realm-export.json disparam pipeline de validacao, diff, aprovacao e aplicacao.
