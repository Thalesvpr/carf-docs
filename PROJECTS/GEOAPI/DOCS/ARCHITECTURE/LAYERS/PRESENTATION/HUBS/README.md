# HUBS

SignalR hubs do GEOAPI fornecendo comunicação real-time bidirecional entre servidor e clientes conectados via WebSockets (fallback long-polling) para notificações push instantâneas quando domain events ocorrem. NotificationsHub gerencia conexões clientes autenticados via JWT access token validado em OnConnectedAsync, agrupa connections por tenant_id e user_id em groups permitindo broadcast direcionado e escuta domain events via IDomainEventDispatcher despachando mensagens typed para clientes específicos quando UnitCreatedEvent (notificar analistas dessa comunidade), LegitimationApprovedEvent (notificar solicitante e município) ou SyncConflictEvent (alertar field agent para resolver). Clients subscritos a topics específicos (units.{communityId}, legitimations.pending) recebem apenas eventos relevantes reduzindo noise, server methods invocáveis por clients permitem actions como MarkNotificationAsRead ou SubscribeToEntity com autorização verificada antes de executar. Hub scale-out via Redis backplane permite múltiplas instâncias API compartilharem connections distribuindo mensagens para todos servers do cluster garantindo client recebe notificação independente de qual instância está conectado.

## Arquivos Principais (a criar)

- 01-notifications-hub.md - Real-time push notifications
- 02-connection-management.md - Groups e user mapping
- 03-domain-events-integration.md - Listener e dispatcher
- 04-redis-backplane.md - Scale-out múltiplas instâncias
- 05-authorization.md - JWT validation em WebSocket
- 06-topics-subscription.md - Filtering relevante por feature

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (6) antes do rodapé - considerar converter para parágrafo denso.
