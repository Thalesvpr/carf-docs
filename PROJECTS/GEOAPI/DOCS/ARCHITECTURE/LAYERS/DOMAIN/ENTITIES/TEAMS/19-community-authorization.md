---
type: leaf
status: approved
updated: 2026-02-07
---

# CommunityAuthorization

Entidade representando autorizacao de acesso a uma Community especifica, concedida a uma Team inteira ou a um Account individual. Controla de forma granular quem pode ler, criar e editar dados em cada comunidade. Herda de BaseEntity fornecendo auditoria temporal.

## Papel no Dominio

A CommunityAuthorization e o mecanismo de controle de acesso por escopo geografico. Enquanto o Role do Account define o que o usuario pode fazer (aprovar, rejeitar, cadastrar), a CommunityAuthorization define onde ele pode fazer: em quais comunidades tem permissao. Isso permite que equipes trabalhem isoladamente em comunidades diferentes sem interferir umas nas outras. O download de pacotes offline no REURBCAD e filtrado por comunidades autorizadas.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| CommunityId | Guid | nao | FK para Community autorizada. |
| TeamId | Guid | sim | FK para Team. Mutuamente exclusivo com AccountId (XOR). |
| AccountId | Guid | sim | UUID do usuario individual. Mutuamente exclusivo com TeamId (XOR). |
| PermissionLevel | string | nao | Nivel de acesso. Valores: READ (somente leitura), WRITE (leitura e criacao/edicao), ADMIN (controle total incluindo exclusao). |
| GrantedAt | DateTime | nao | Quando a autorizacao foi concedida. |
| GrantedBy | Guid | nao | Account que concedeu a autorizacao. |

## Relacionamentos

Pertence a uma Community (obrigatorio). Vinculada a uma Team OU a um Account (mutuamente exclusivo).

## Invariantes de Negocio

Exatamente um entre TeamId e AccountId deve estar preenchido (XOR). Ambos null ou ambos preenchidos gera erro de validacao. Autorizacao individual de Account sobrescreve autorizacao de Team quando ambas existem para a mesma comunidade, permitindo excecoes granulares.
