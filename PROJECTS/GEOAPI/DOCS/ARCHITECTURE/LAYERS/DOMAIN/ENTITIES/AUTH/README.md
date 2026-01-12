# AUTH

Entities autenticação do GEOAPI gerenciando sessões usuário e API keys para integração programática. Session rastreia login ativo com UserId referenciando Account, TokenJti string identificando JWT emitido Keycloak permitindo revogação via blacklist, ExpiresAt timestamp UTC validando sessão ainda ativa, IpAddress e UserAgent capturando contexto request para auditoria e detecção anomalias e LastActivityAt atualizado cada request renovando timeout idle. ApiKey permite sistemas externos autenticarem via header X-API-Key sem OAuth flow contendo Name descritivo, KeyValue hash SHA-256 do secret comparado durante validação nunca armazenando plain text, Scopes lista permissões granulares limitando operações permitidas, ExpiresAt opcional para keys temporárias e IsActive boolean permitindo revogação imediata sem deletar registro mantendo auditoria.

## Arquivos

- **[16-session.md](./16-session.md)** - Sessões login ativas JWT tracking revogação
- **[17-api-key.md](./17-api-key.md)** - API keys autenticação programática sistemas externos

---

**Última atualização:** 2026-01-12
