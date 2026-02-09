---
type: leaf
status: draft
updated: 2026-02-07
---

# SPIs Keycloak CARF

Tres SPIs customizadas compoem as extensoes server-side do CARF: um Authenticator para validacao de CPF, um Event Listener para auditoria multi-tenant e um Protocol Mapper para claims de tenant nos tokens.

## Authenticator - CpfValidator

A SPI CpfValidatorAuthenticator implementa a interface Authenticator. No metodo authenticate extrai o username do usuario e valida se e um CPF valido removendo caracteres nao numericos, verificando 11 digitos e digitos verificadores conforme Mod11 compativel com @carf/tscore. Caso invalido retorna AuthenticationFlowError.INVALID_USER, caso valido chama context.success(). O metodo requiresUser retorna true. A Factory CpfValidatorAuthenticatorFactory registra provider ID "carf-cpf-validator" com display type "CARF CPF Validator", nao configuravel.

## Event Listener - TenantAudit

| Metodo | Tipo de Evento | Dados Capturados |
|:-------|:---------------|:-----------------|
| onEvent(Event) | Usuario (LOGIN, LOGOUT, REGISTER) | Tipo, userId, tenantId de atributos, IP |
| onEvent(AdminEvent) | Admin (CREATE_USER, UPDATE_CLIENT) | operationType, resourcePath, userId operador |

TenantAuditEventListener implementa EventListenerProvider. Para eventos de usuario extrai tenant_id dos atributos e registra log estruturado persistindo em storage externo. Para eventos administrativos registra operacao e operador. Factory registra provider como "tenant-audit".

## Protocol Mapper - TenantMapper

TenantProtocolMapper implementa ProtocolMapper para injetar claims customizados (tenant_id, allowed_tenants, community_ids) nos tokens JWT. Consulta atributos do usuario autenticado e mapeia para claims no access token e id token conforme client scope carf-tenant.

## Referencias

- [03a-extension-structure.md](./03a-extension-structure.md) - Estrutura Maven do projeto
- [03c-extension-deploy.md](./03c-extension-deploy.md) - Build, deploy e testes
