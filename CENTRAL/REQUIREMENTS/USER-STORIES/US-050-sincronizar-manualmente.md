---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# US-050: Sincronizar Manualmente

Como agente de campo, quero iniciar processo de sincronização manualmente para que o controle sobre quando enviar e receber dados seja meu, onde a funcionalidade deve fornecer botão "Sincronizar agora" facilmente acessível na interface, garantindo exibição de barra de progresso visual detalhada durante o processo de sincronização bidirecional, permitindo que o agente receba notificações claras de sucesso ou falha ao final do processo com acesso a log detalhado de sincronização para diagnóstico de problemas. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile coordenando com GEOAPI através dos endpoints GET /api/sync/pull e POST /api/sync/push, integrada ao UC-005 (Sincronizar Dados Offline) para gestão completa do ciclo de sincronização. Os critérios de aceitação incluem disponibilidade de botão "Sincronizar agora" facilmente acessível na tela principal ou menu lateral, verificação prévia de conectividade antes de iniciar sincronização com alerta se offline, exibição de barra de progresso detalhada mostrando etapas (VALIDANDO ENVIANDO RECEBENDO PROCESSANDO) e percentual de conclusão, indicação visual de quantidade de registros sendo enviados e recebidos durante processo, notificação de sucesso ao completar sincronização mostrando resumo (X unidades enviadas Y atualizações recebidas), notificação de falha com mensagem clara do erro ocorrido e opções de retry, acesso a log detalhado de sincronização mostrando timestamp de cada operação e eventual erro por registro, capacidade de cancelar sincronização em andamento retornando ao estado anterior, e prevenção de edições durante sincronização ativa para evitar conflitos de dados. A rastreabilidade conecta esta user story ao RF-187 (Sincronização Manual) e ao UC-005 (Sincronizar Dados Offline), garantindo controle completo do agente sobre processo de sincronização de dados.

---

**Última atualização:** 2025-12-30
