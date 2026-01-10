# Audit Logging - GEOAPI

## Sistema de Auditoria

Audit logging no GEOAPI captura TODAS as operações de escrita (Commands) registrando quem (user_id do JWT), quando (timestamp UTC), o quê (tipo de comando, entity afetada, entity_id), onde (tenant_id), e detalhes (JSON com valores antes/depois para updates) armazenados em tabela `audit_logs` com colunas `id`, `timestamp`, `user_id`, `tenant_id`, `entity_type`, `entity_id`, `action` (CREATE/UPDATE/DELETE), `old_values` (JSONB), `new_values` (JSONB), `ip_address`, implementado via interceptor MediatR que envolve todos CommandHandlers executando log após sucesso do comando, logs são imutáveis (apenas INSERT, nunca UPDATE/DELETE), retention de 7 anos conforme LGPD, e queries via endpoint `/api/audit-logs` restrito a admin users com filtros por entity, user, date range retornando timeline de mudanças para compliance e troubleshooting.

## Schema da Tabela

```sql
CREATE TABLE audit_logs (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp         TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    user_id           UUID NOT NULL,
    user_email        VARCHAR(255) NOT NULL,
    tenant_id         UUID NOT NULL,
    entity_type       VARCHAR(100) NOT NULL,  -- 'Unit', 'Holder', 'Community'
    entity_id         UUID NOT NULL,
    action            VARCHAR(20) NOT NULL,   -- 'CREATE', 'UPDATE', 'DELETE'
    old_values        JSONB,                  -- NULL para CREATE
    new_values        JSONB,                  -- NULL para DELETE
    ip_address        INET,
    user_agent        TEXT,
    command_type      VARCHAR(255) NOT NULL,  -- 'CreateUnitCommand', 'UpdateHolderCommand'

    -- Índices para queries rápidas
    INDEX idx_audit_entity (entity_type, entity_id),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_timestamp (timestamp DESC),
    INDEX idx_audit_tenant (tenant_id)
);

-- Particionamento por mês para performance (opcional)
CREATE TABLE audit_logs_2026_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

## Implementação com MediatR

### Behavior Pipeline

```csharp
public class AuditLoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IAuditLogRepository _auditLogRepository;
    private readonly ICurrentUserService _currentUserService;
    private readonly IHttpContextAccessor _httpContextAccessor;

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        // Apenas audita Commands, não Queries
        if (!typeof(TRequest).Name.EndsWith("Command"))
            return await next();

        // Snapshot ANTES (para UPDATE/DELETE)
        var oldValues = await GetCurrentStateAsync(request);

        // Executar comando
        var response = await next();

        // Snapshot DEPOIS (para CREATE/UPDATE)
        var newValues = await GetNewStateAsync(request, response);

        // Salvar audit log
        var auditLog = new AuditLog
        {
            Timestamp = DateTime.UtcNow,
            UserId = _currentUserService.UserId,
            UserEmail = _currentUserService.Email,
            TenantId = _currentUserService.TenantId,
            EntityType = ExtractEntityType(request),
            EntityId = ExtractEntityId(request, response),
            Action = DetermineAction(request),
            OldValues = oldValues,
            NewValues = newValues,
            IpAddress = _httpContextAccessor.HttpContext?.Connection.RemoteIpAddress?.ToString(),
            UserAgent = _httpContextAccessor.HttpContext?.Request.Headers["User-Agent"],
            CommandType = typeof(TRequest).Name
        };

        await _auditLogRepository.AddAsync(auditLog, cancellationToken);

        return response;
    }

    private string DetermineAction(TRequest request)
    {
        var commandName = typeof(TRequest).Name;

        if (commandName.StartsWith("Create")) return "CREATE";
        if (commandName.StartsWith("Update")) return "UPDATE";
        if (commandName.StartsWith("Delete")) return "DELETE";

        return "UNKNOWN";
    }
}
```

### Registro no DI

```csharp
// Program.cs
services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(CreateUnitCommand).Assembly);
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(AuditLoggingBehavior<,>));
});
```

## Exemplos de Logs

### CREATE - Criação de Unidade

```json
{
  "id": "a1b2c3d4-...",
  "timestamp": "2026-01-10T14:30:00Z",
  "user_id": "e5f6g7h8-...",
  "user_email": "joao.silva@municipio.gov.br",
  "tenant_id": "m9n0o1p2-...",
  "entity_type": "Unit",
  "entity_id": "q3r4s5t6-...",
  "action": "CREATE",
  "old_values": null,
  "new_values": {
    "code": "UN-001",
    "address": "Rua das Flores, 123",
    "area": 250.0,
    "status": "ACTIVE"
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "command_type": "CreateUnitCommand"
}
```

### UPDATE - Atualização de Posseiro

```json
{
  "id": "u7v8w9x0-...",
  "timestamp": "2026-01-10T15:45:00Z",
  "user_id": "e5f6g7h8-...",
  "user_email": "joao.silva@municipio.gov.br",
  "tenant_id": "m9n0o1p2-...",
  "entity_type": "Holder",
  "entity_id": "y1z2a3b4-...",
  "action": "UPDATE",
  "old_values": {
    "name": "Maria Santos",
    "cpf": "123.456.789-00",
    "phone": "(11) 98888-7777"
  },
  "new_values": {
    "name": "Maria Santos Silva",  // Nome mudou
    "cpf": "123.456.789-00",
    "phone": "(11) 99999-8888"     // Telefone mudou
  },
  "ip_address": "192.168.1.100",
  "command_type": "UpdateHolderCommand"
}
```

### DELETE - Deleção de Documento

```json
{
  "id": "c5d6e7f8-...",
  "timestamp": "2026-01-10T16:00:00Z",
  "user_id": "e5f6g7h8-...",
  "user_email": "joao.silva@municipio.gov.br",
  "tenant_id": "m9n0o1p2-...",
  "entity_type": "Document",
  "entity_id": "g9h0i1j2-...",
  "action": "DELETE",
  "old_values": {
    "filename": "contrato.pdf",
    "file_size": 1024000,
    "uploaded_at": "2026-01-05T10:00:00Z"
  },
  "new_values": null,
  "ip_address": "192.168.1.100",
  "command_type": "DeleteDocumentCommand"
}
```

## Consultas de Auditoria

### Endpoint API

```csharp
[HttpGet("api/audit-logs")]
[Authorize(Roles = "ADMIN,SUPER_ADMIN")]
public async Task<IActionResult> GetAuditLogs(
    [FromQuery] string? entityType = null,
    [FromQuery] Guid? entityId = null,
    [FromQuery] Guid? userId = null,
    [FromQuery] DateTime? startDate = null,
    [FromQuery] DateTime? endDate = null,
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 50)
{
    var query = _context.AuditLogs.AsQueryable();

    if (entityType != null)
        query = query.Where(a => a.EntityType == entityType);

    if (entityId.HasValue)
        query = query.Where(a => a.EntityId == entityId.Value);

    if (userId.HasValue)
        query = query.Where(a => a.UserId == userId.Value);

    if (startDate.HasValue)
        query = query.Where(a => a.Timestamp >= startDate.Value);

    if (endDate.HasValue)
        query = query.Where(a => a.Timestamp <= endDate.Value);

    var total = await query.CountAsync();

    var logs = await query
        .OrderByDescending(a => a.Timestamp)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    return Ok(new
    {
        total,
        page,
        pageSize,
        data = logs
    });
}
```

### Timeline de Mudanças

```csharp
[HttpGet("api/audit-logs/timeline/{entityType}/{entityId}")]
[Authorize(Roles = "ADMIN")]
public async Task<IActionResult> GetEntityTimeline(string entityType, Guid entityId)
{
    var logs = await _context.AuditLogs
        .Where(a => a.EntityType == entityType && a.EntityId == entityId)
        .OrderBy(a => a.Timestamp)
        .Select(a => new
        {
            a.Timestamp,
            a.Action,
            a.UserEmail,
            Changes = DiffValues(a.OldValues, a.NewValues)
        })
        .ToListAsync();

    return Ok(logs);
}

private object DiffValues(string? oldJson, string? newJson)
{
    if (oldJson == null) return new { type = "created" };
    if (newJson == null) return new { type = "deleted" };

    var old = JsonSerializer.Deserialize<Dictionary<string, object>>(oldJson);
    var @new = JsonSerializer.Deserialize<Dictionary<string, object>>(newJson);

    var changes = new Dictionary<string, object>();

    foreach (var key in @new!.Keys)
    {
        if (!old!.ContainsKey(key) || !old[key].Equals(@new[key]))
        {
            changes[key] = new
            {
                from = old.ContainsKey(key) ? old[key] : null,
                to = @new[key]
            };
        }
    }

    return changes;
}
```

## Compliance e Retenção

### LGPD

- **Logs retidos por 7 anos** - Conforme Art. 16 da LGPD
- **Logs anonimizados após solicitação** - Direito ao esquecimento (Art. 18)
- **Acesso restrito** - Apenas ADMIN e SUPER_ADMIN
- **Criptografia em repouso** - PostgreSQL com TDE (Transparent Data Encryption)

### Retenção Automática

```sql
-- Job que roda mensalmente deletando logs antigos
CREATE OR REPLACE FUNCTION cleanup_old_audit_logs()
RETURNS void AS $$
BEGIN
    DELETE FROM audit_logs
    WHERE timestamp < NOW() - INTERVAL '7 years';
END;
$$ LANGUAGE plpgsql;

-- Agendar com pg_cron
SELECT cron.schedule('cleanup-audit-logs', '0 0 1 * *', 'SELECT cleanup_old_audit_logs()');
```

## Performance

### Particionamento

Para performance em tabelas grandes (>10M rows), usar particionamento por mês:

```sql
-- Tabela pai
CREATE TABLE audit_logs (...) PARTITION BY RANGE (timestamp);

-- Partições mensais
CREATE TABLE audit_logs_2026_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE audit_logs_2026_02 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

### Índices Otimizados

```sql
-- Queries por entity
CREATE INDEX idx_audit_entity ON audit_logs (entity_type, entity_id, timestamp DESC);

-- Queries por usuário
CREATE INDEX idx_audit_user ON audit_logs (user_id, timestamp DESC);

-- Queries por tenant
CREATE INDEX idx_audit_tenant ON audit_logs (tenant_id, timestamp DESC);
```

## Referências

- [LGPD - Lei 13.709/2018](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [PostgreSQL Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [MediatR Pipeline Behaviors](https://github.com/jbogard/MediatR/wiki/Behaviors)
