---
type: leaf
status: approved
updated: 2026-02-07
---

# Account

Entidade representando usuario do sistema vinculado a um Tenant especifico, sincronizado com Keycloak para autenticacao OAuth2/OIDC. Armazena perfil local, preferencias e relacionamentos internos. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

O Account e a representacao local de um usuario do Keycloak dentro do contexto do CARF. Enquanto o Keycloak gerencia autenticacao, senhas e tokens, o Account armazena dados de dominio como role dentro do sistema, vinculacao com equipes e preferencias de interface. A sincronizacao e bidirecional: criacao ou atualizacao no Keycloak dispara webhook que atualiza o Account local, mantendo email, nome e roles consistentes entre os sistemas.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio vinculado. FK para Tenant. Isolamento via RLS. |
| ExternalId | Guid | nao | UUID do usuario no Keycloak para sincronizacao bidirecional. |
| Name | string | nao | Nome completo. |
| Email | string | nao | Email unico por tenant. Usado para login. |
| PhoneNumber | string | sim | Telefone de contato. |
| Role | string | nao | Role que define permissoes. Valores: SUPER_ADMIN (acesso total cross-tenant), ADMIN (administrador do tenant), MANAGER (gestor com poder de aprovacao), ANALYST (analista tecnico), FIELD_COORDINATOR (coordenador de equipe de campo), FIELD_CADASTRATOR (cadastrador de campo). |
| ProfilePhoto | string | sim | URL da foto de perfil no S3 ou Gravatar. |
| Preferences | JsonDocument | sim | Configuracoes de UI em JSON: tema, idioma, timezone. |
| IsActive | bool | nao | Indica se conta esta ativa. Desabilitar impede acesso sem deletar. |
| LastLoginAt | DateTime | sim | Ultimo acesso registrado. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

TeamMember vinculando Account a Teams com role especifica (COORDINATOR ou CADASTRATOR). CommunityAuthorization para acessos individuais a comunidades que sobrescrevem autorizacoes de equipe. Session rastreando sessoes ativas. ApiKey para chaves de API do plugin QGIS.

## Invariantes de Negocio

Email unico por tenant. ExternalId deve corresponder a um usuario valido no Keycloak. IsActive false bloqueia acesso a todas as funcionalidades sem excluir dados historicos.

## Domain Events

AccountCreatedEvent emitido ao criar. AccountDeactivatedEvent emitido ao desativar.
