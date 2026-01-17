# Session

Entidade representando sessão usuário autenticado sistema armazenando informações autenticação e contexto acesso para rastreamento segurança controle sessões ativas. Herda de BaseEntity fornecendo auditoria temporal soft delete. Campos principais incluem AccountId Guid FK para Account usuário autenticado, TokenHash string SHA256 JWT nunca armazenando texto claro, DeviceInfo informações dispositivo navegador ou app mobile, IpAddress endereço IP conexão, ExpiresAt DateTime quando sessão expira baseado configuração Keycloak e LastActivityAt DateTime última atividade atualizada cada request.

Campos controle revogação incluem IsRevoked bool indicando sessão manualmente revogada antes expiração, RevokedAt DateTime nullable quando revogada e RevokedBy Guid nullable quem revogou permitindo auditoria. Métodos incluem Revoke(revokedBy) marcando sessão revogada, IsActive() verificando não expirou nem revogada, UpdateActivity() atualizando LastActivityAt estendendo vida sliding expiration e IsExpired() comparando Now ExpiresAt.

Integra middleware autenticação validando TokenHash cada request identificando sessões revogadas expiradas forçando novo login, suporta logout todos dispositivos revogando todas Sessions do Account e permite auditoria acessos rastreando IP DeviceInfo padrões temporais detecção anomalias registrando AuditLog.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
