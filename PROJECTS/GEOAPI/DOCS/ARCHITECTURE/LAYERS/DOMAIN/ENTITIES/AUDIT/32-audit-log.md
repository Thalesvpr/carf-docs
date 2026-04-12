---
type: leaf
status: approved
updated: 2026-02-07
---

# AuditLog

Entidade representando registro imutavel de auditoria rastreando todas as operacoes de escrita no sistema. Cada criacao, atualizacao ou exclusao de qualquer entidade gera um registro com valores anteriores e novos, permitindo rastreabilidade completa para conformidade LGPD e investigacao de incidentes. Registros sao capturados automaticamente pelo interceptor do EF Core durante SaveChanges.

## Papel no Dominio

O AuditLog implementa a trilha de auditoria exigida pela LGPD para operacoes sobre dados pessoais. Permite reconstruir o historico completo de qualquer registro (quem criou, quem modificou, quais campos mudaram, quando e de qual IP), investigar incidentes de seguranca e gerar relatorios de conformidade. A retencao minima e de 7 anos conforme orientacao da ANPD.

## Propriedades

| Propriedade | Tipo | Nullable | Descricao |
|-------------|------|----------|-----------|
| Id | Guid | nao | Chave primaria UUID. |
| TenantId | Guid | nao | Municipio. FK para Tenant. Isolado via RLS. |
| UserId | Guid | sim | Account do usuario. Null se operacao automatica (job). |
| Action | string | nao | Tipo de acao: CREATE, UPDATE, DELETE, LOGIN, LOGOUT, STATUS_CHANGE. |
| EntityType | string | nao | Tipo da entidade afetada. |
| EntityId | Guid | nao | ID da entidade afetada. |
| OldValues | JsonDocument | sim | Valores anteriores em JSON. Null em CREATE. |
| NewValues | JsonDocument | sim | Novos valores em JSON. Null em DELETE. |
| IpAddress | string | sim | IP de origem. IPv4 ou IPv6. |
| UserAgent | string | sim | User-Agent do cliente HTTP. |
| Timestamp | DateTime | nao | Momento da operacao. |

## Relacionamentos

Vinculado a Tenant via RLS. Referencia um Account via UserId quando operacao humana.

## Invariantes de Negocio

Append-only: registros nunca sao atualizados ou deletados, garantindo imutabilidade da trilha de auditoria. OldValues e null em CREATE, NewValues e null em DELETE, ambos preenchidos em UPDATE. Particionamento por mes recomendado para tabelas com alto volume.
