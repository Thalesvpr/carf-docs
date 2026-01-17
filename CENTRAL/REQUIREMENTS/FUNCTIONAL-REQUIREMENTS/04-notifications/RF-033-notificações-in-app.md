---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: scalability
---

# RF-033: Notificações In-App

Usuários recebem notificações de ações relevantes incluindo aprovações de unidades submetidas comentários em documentos vinculados solicitações de alteração por MANAGER atribuição a nova equipe ou comunidade e outras interações importantes para workflow, badge de notificações não lidas exibido em ícone de sino ou similar na barra de navegação mostrando quantidade numérica de notificações pendentes com destaque visual (cor vermelha pulsante) chamando atenção para itens não visualizados, painel de notificações acessível via clique em badge expandindo dropdown ou modal exibindo lista cronológica reversa de notificações com timestamp tipo de notificação resumo de conteúdo e link direto para recurso relacionado permitindo navegação contextual rápida, funcionalidade de marcação como lida/não lida implementada permitindo usuário gerenciar estado de notificações individualmente ou em lote (marcar todas como lidas) com persistência de estado entre sessões, implementação em módulos GEOWEB e GEOAPI com sistema de eventos backend publicando notificações em fila (Redis RabbitMQ) e frontend consumindo via polling ou WebSocket para atualizações em tempo real.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
