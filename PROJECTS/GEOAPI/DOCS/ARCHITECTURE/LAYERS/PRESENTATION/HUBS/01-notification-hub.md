---
type: leaf
status: active
updated: 2026-02-07
---

# Notification Hub

A GEOAPI utiliza SignalR para comunicacao real-time com clientes conectados. O hub e protegido por autenticacao JWT e organiza conexoes em grupos por tenant e por usuario.

## NotificationHub

A classe NotificationHub herda de Hub e requer autorizacao. Ao conectar, o metodo OnConnectedAsync adiciona a conexao a dois grupos: "tenant:{tenantId}" para notificacoes de escopo do municipio e "user:{userId}" para notificacoes pessoais. A desconexao nao exige limpeza manual pois o SignalR remove automaticamente conexoes dos grupos.

## Servico de Notificacoes

A interface INotificationService define o contrato de notificacoes do dominio. A implementacao SignalRNotificationService utiliza IHubContext para enviar mensagens aos grupos corretos.

| Metodo | Grupo Alvo | Evento | Payload |
|--------|-----------|--------|---------|
| NotifyUnitCreated | tenant:{tenantId} | UnitCreated | UnitSummaryDto |
| NotifyUnitUpdated | tenant:{tenantId} | UnitUpdated | unitId |
| NotifyLegitimationStatusChanged | user:{userId} | LegitimationStatusChanged | legitimationId e newStatus |

## Integracao com Clientes

O cliente JavaScript conecta ao hub via HubConnectionBuilder apontando para /hubs/notifications, fornecendo o access token JWT via accessTokenFactory. A conexao e configurada com reconexao automatica. Os listeners registram callbacks para os eventos UnitCreated (atualiza lista de unidades) e LegitimationStatusChanged (exibe notificacao de status).

## Configuracao

O SignalR e registrado no container de DI em Program.cs e o hub e mapeado na rota /hubs/notifications no pipeline de middleware.
