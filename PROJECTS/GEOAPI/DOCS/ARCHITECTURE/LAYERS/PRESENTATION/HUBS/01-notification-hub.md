# Notification Hub

SignalR Hub para comunicação real-time.

## NotificationHub

```csharp
[Authorize]
public class NotificationHub : Hub
{
    private readonly ITenantContext _tenantContext;

    public override async Task OnConnectedAsync()
    {
        // Adicionar cliente ao grupo do tenant
        var tenantGroup = $"tenant:{_tenantContext.TenantId}";
        await Groups.AddToGroupAsync(Context.ConnectionId, tenantGroup);

        // Adicionar ao grupo do usuário
        var userGroup = $"user:{_tenantContext.UserId}";
        await Groups.AddToGroupAsync(Context.ConnectionId, userGroup);

        await base.OnConnectedAsync();
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        // Grupos são automaticamente limpos
        await base.OnDisconnectedAsync(exception);
    }
}
```

## INotificationService

```csharp
public interface INotificationService
{
    Task NotifyUnitCreated(Guid tenantId, UnitSummaryDto unit);
    Task NotifyUnitUpdated(Guid tenantId, Guid unitId);
    Task NotifyLegitimationStatusChanged(Guid userId, Guid legitimationId, string newStatus);
}

public class SignalRNotificationService : INotificationService
{
    private readonly IHubContext<NotificationHub> _hubContext;

    public async Task NotifyUnitCreated(Guid tenantId, UnitSummaryDto unit)
    {
        await _hubContext.Clients
            .Group($"tenant:{tenantId}")
            .SendAsync("UnitCreated", unit);
    }

    public async Task NotifyLegitimationStatusChanged(Guid userId, Guid legitimationId, string newStatus)
    {
        await _hubContext.Clients
            .Group($"user:{userId}")
            .SendAsync("LegitimationStatusChanged", new { legitimationId, newStatus });
    }
}
```

## Cliente JavaScript

```typescript
// Conectar ao hub
const connection = new signalR.HubConnectionBuilder()
    .withUrl("/hubs/notifications", {
        accessTokenFactory: () => getAccessToken()
    })
    .withAutomaticReconnect()
    .build();

// Listeners
connection.on("UnitCreated", (unit) => {
    console.log("Nova unidade criada:", unit);
    refreshUnitList();
});

connection.on("LegitimationStatusChanged", ({ legitimationId, newStatus }) => {
    showNotification(`Status atualizado para: ${newStatus}`);
});

// Iniciar conexão
await connection.start();
```

## Configuração

```csharp
// Program.cs
services.AddSignalR();

app.MapHub<NotificationHub>("/hubs/notifications");
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
