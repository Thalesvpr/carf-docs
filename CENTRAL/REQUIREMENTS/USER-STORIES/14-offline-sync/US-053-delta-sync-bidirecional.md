---
modules: [GEOAPI, REURBCAD]
epic: performance
---

# US-053: Delta Sync Bidirecional

Como sistema, quero sincronizar apenas mudanças incrementais desde a última sincronização em vez de todos os dados para que o tráfego de rede seja minimizado e performance seja otimizada, onde a funcionalidade deve implementar protocolo de sincronização delta bidirecional enviando timestamp last_pulled_at para receber apenas registros modificados no servidor após esse momento, garantindo que no push apenas registros marcados localmente com synced:false sejam enviados ao servidor, permitindo que o servidor retorne apenas mudanças ocorridas após o timestamp fornecido reduzindo drasticamente volume de dados transferidos. Esta funcionalidade é implementada pelo módulo GEOWEB coordenando com GEOAPI através dos endpoints GET /api/sync/pull?lastPulledAt={timestamp} e POST /api/sync/push, integrada ao UC-005 (Sincronizar Dados Offline) para eficiência de sincronização. Os critérios de aceitação incluem armazenamento local persistente do timestamp last_pulled_at da última sincronização bem-sucedida, inclusão automática desse timestamp como query parameter em requisições GET /api/sync/pull, filtragem no servidor retornando apenas registros com updated_at maior que lastPulledAt recebido, identificação local de registros pendentes através de flag synced:false ou similar em banco local, envio no POST /api/sync/push apenas de registros com synced:false para minimizar payload, marcação automática de registros como synced:true após confirmação de recebimento pelo servidor, tratamento especial de primeira sincronização quando last_pulled_at não existe enviando null ou omitindo parâmetro, e logging detalhado de quantidade de registros transferidos em cada direção para monitoramento de eficiência. A rastreabilidade conecta esta user story ao RF-189 (Sincronização Delta Incremental) e ao UC-005 (Sincronizar Dados Offline), garantindo eficiência de rede e performance em cenários de conectividade limitada.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
