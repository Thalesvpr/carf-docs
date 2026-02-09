---
type: leaf
status: review
updated: 2026-02-08
---

# Realm Export - Roles, Users e Auth Flows

Secoes do realm-export.json referentes a roles, usuarios seed e authentication flows.

## Realm Roles

| Role | Descricao | Composta | Herda |
|:-----|:----------|:---------|:------|
| field-cadastrator | Cadastrador de campo | nao | - |
| field-coordinator | Coordenador de campo | sim | field-cadastrator |
| analyst | Analista de regularizacao | nao | - |
| manager | Gerente de operacoes | sim | analyst, field-coordinator |
| admin | Administrador do tenant | sim | manager |
| super-admin | Super administrador | sim | admin |
| dev | Desenvolvedor (transversal) | nao | - |

## Client Roles

| Client | Role | Descricao |
|:-------|:-----|:----------|
| admin | manage-users | Gerenciar usuarios |
| admin | manage-tenants | Gerenciar prefeituras |
| admin | view-audit-logs | Logs de auditoria |
| reurbcad | sync-data | Sincronizar dados |
| reurbcad | manage-team | Gerenciar equipe |
| geogis | gis-reader | Leitura de dados geoespaciais e ortofotos |
| geogis | gis-writer | Publicacao de poligonos georreferenciados |

A defaultRole default-roles-carf e composta e atribuida automaticamente a novos usuarios.

## Users Seed

O usuario seed admin-carf possui realm role super-admin e todas client roles do admin. Attributes definem tenants wildcard e current_tenant tenant-001. Senha via variavel de ambiente, marcada temporaria para forcar troca. Senhas reais nunca devem constar em arquivos versionados.

## Authentication Flows

O flow carf-browser possui duas executions: auth-cookie como ALTERNATIVE (prioridade 10) e auth-username-password-form como REQUIRED (prioridade 20). Definido como browserFlow do realm.

## Identity Providers

IdPs externos seguem formato com alias, providerId, enabled, trustEmail e config com clientId e clientSecret via variaveis de ambiente.

## Import e Export

Para import no startup usar --import-realm. Para import manual usar subcomando import --file. Para export de backup usar export --file --realm. Variaveis de ambiente injetaveis no JSON via sintaxe ${VAR_NAME}.

Ver [06-realm-export-schema](./06-realm-export-schema.md) para estrutura raiz e [06a-realm-export-clients](./06a-realm-export-clients.md) para clients.
