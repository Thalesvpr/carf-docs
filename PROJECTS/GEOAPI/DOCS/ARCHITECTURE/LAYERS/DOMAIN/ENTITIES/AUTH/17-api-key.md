# ApiKey

Entidade representando chave API para autenticação integrações externas permitindo sistemas terceiros acessarem endpoints GEOAPI sem OAuth usuário humano com controle granular permissões expiração. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem AccountId Guid FK para Account usuário responsável chave, Name string descritivo identificando uso (Script Importação, Integração Mobile), KeyPrefix prefixo visível geoapi_sk_ mostrado identificação, KeyHash SHA256 valor completo nunca armazenando texto claro e Permissions JSON array permissões específicas (units.read units.create holders.read) ao invés roles completos.

Campos controle incluem ExpiresAt DateTime nullable expiração null se permanente, LastUsedAt DateTime nullable última vez usada atualizado cada request, IsRevoked bool indicando revogada e RevokedAt quando revogada. Métodos incluem Revoke() desativando permanentemente, IsActive() verificando não expirou nem revogada, UpdateLastUsed() rastreando uso, HasPermission(permission) verificando JSON contém permissão e GenerateKey() estático gerando geoapi_sk_ seguido 32 caracteres retornando texto claro mostrado UMA vez e hash armazenamento.

Integra middleware autenticação verificando header X-API-Key comparando hash validando permissões expiração via ApiKeyValue, permite rotação criando nova revogando antiga mantendo auditoria e suporta rate limiting por ApiKey rastreando requests por minuto.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
