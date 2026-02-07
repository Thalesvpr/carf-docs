---
type: leaf
status: approved
updated: 2026-02-07
---

# Tenant

Entidade representando um municipio ou orgao cliente do sistema em arquitetura multi-tenant com isolamento completo de dados via Row-Level Security do PostgreSQL. Cada tenant opera como instancia logica independente compartilhando a mesma infraestrutura fisica. Herda de BaseEntity fornecendo auditoria e soft delete.

## Papel no Dominio

O Tenant e a raiz do isolamento de dados. Toda entidade no sistema possui tenant_id e toda query e automaticamente filtrada pela policy RLS que compara tenant_id com a variavel de sessao app.current_tenant definida pelo middleware de autenticacao a partir do claim do JWT. Isso garante que um municipio nunca acessa dados de outro, mesmo em caso de bug na aplicacao.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| Code | string | nao | Codigo unico curto para URLs e subdominios. Exemplos: ITERJ, HAB-RJ, PMN. |
| Name | string | nao | Nome completo da instituicao. |
| Document | string | nao | CNPJ formatado. |
| ContactEmail | string | nao | Email para comunicacoes oficiais. |
| ContactPhone | string | sim | Telefone do responsavel. |
| Address | string | sim | Endereco da sede. |
| Logo | string | sim | URL do logotipo para white-label em relatorios e certidoes. |
| PrimaryColor | string | sim | Cor primaria em hex para tema. |
| SecondaryColor | string | sim | Cor secundaria em hex. |
| Settings | JsonDocument | sim | Configuracoes especificas em JSONB: campos customizados, integracoes, limites. |
| Subscription | JsonDocument | sim | Plano contratado em JSON: limites de usuarios, unidades, storage e data de renovacao. |
| IsActive | bool | nao | Acesso global ao tenant. False bloqueia todos os usuarios. |
| TrialEndsAt | DateTime | sim | Data de fim do periodo trial. Null se plano pago. |
| CreatedAt | DateTime | nao | Data de criacao. |
| UpdatedAt | DateTime | nao | Ultima atualizacao. |
| DeletedAt | DateTime | sim | Soft delete. |

## Relacionamentos

Contem colecoes de Accounts vinculados, Communities do municipio, Units cadastradas e AuditLogs de operacoes.

## Invariantes de Negocio

Code unico globalmente (nao por tenant, pois tenants sao top-level). IsActive false bloqueia acesso de todos os usuarios do tenant imediatamente. A policy RLS filtra automaticamente todas as queries por tenant_id igual a current_setting('app.current_tenant')::uuid, garantindo isolamento mesmo se a aplicacao falhar em filtrar.

Caminho base S3 para arquivos do tenant: tenant_id/ como prefixo de todos os caminhos de storage, garantindo isolamento fisico de arquivos.

## Domain Events

TenantCreatedEvent emitido ao criar. TenantDeactivatedEvent emitido ao desativar.
