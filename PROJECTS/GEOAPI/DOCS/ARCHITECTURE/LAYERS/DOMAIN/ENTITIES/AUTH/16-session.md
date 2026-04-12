---
type: leaf
status: approved
updated: 2026-02-07
---

# Session

Entidade representando sessao de usuario autenticado, armazenando informacoes de autenticacao e contexto de acesso para rastreamento de seguranca e controle de sessoes ativas. Herda de BaseEntity fornecendo auditoria temporal e soft delete.

## Papel no Dominio

A Session rastreia cada login ativo no sistema, permitindo auditar acessos, detectar padroes anomalos (multiplos logins simultaneos de IPs diferentes) e forcar logout de todos os dispositivos quando necessario. O token JWT nunca e armazenado em texto claro; apenas seu hash SHA-256 e persistido para validacao.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| AccountId | Guid | nao | FK para Account do usuario autenticado. |
| TokenHash | string | nao | Hash SHA-256 do JWT. Nunca armazena o token em texto claro. |
| DeviceInfo | string | nao | Informacoes do dispositivo ou navegador. |
| IpAddress | string | nao | Endereco IP da conexao. IPv4 ou IPv6. |
| ExpiresAt | DateTime | nao | Quando a sessao expira conforme configuracao do Keycloak. |
| LastActivityAt | DateTime | nao | Ultima atividade, atualizada a cada request para sliding expiration. |
| IsRevoked | bool | nao | Indica sessao revogada manualmente antes da expiracao. Default false. |
| RevokedAt | DateTime | sim | Quando foi revogada. |
| RevokedBy | Guid | sim | Account que revogou. Permite auditoria. |
| CreatedAt | DateTime | nao | Momento do login. |

## Relacionamentos

Pertence a um Account (obrigatorio).

## Invariantes de Negocio

TokenHash e unico. Sessao revogada ou expirada nao pode ser reativada. O middleware de autenticacao valida o TokenHash a cada request, identificando sessoes revogadas e forcando novo login.

Logout de todos os dispositivos revoga todas as Sessions ativas do Account de uma vez.
