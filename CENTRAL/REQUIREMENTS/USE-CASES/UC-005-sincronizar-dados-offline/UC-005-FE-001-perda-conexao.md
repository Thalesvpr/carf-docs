---
modules: [REURBCAD]
epic: authentication
---

# UC-005-FE-001: Perda de Conexão Durante Sync

Fluxo de exceção do UC-005 Sincronizar Dados Offline ocorrendo em qualquer fase (PULL ou PUSH) quando app detecta perda de conexão com internet via listener NetInfo.addEventListener monitorando eventos de mudança de conectividade disparando callback com isConnected=false, onde app imediatamente pausa operação de sincronização em progresso cancelando requests HTTP pendentes via axios.CancelToken evitando timeout demorado, salva estado atual de sincronização em AsyncStorage armazenando sync_checkpoint JSON contendo last_synced_item_id items_remaining current_phase (PULL ou PUSH) e timestamp permitindo resumo posterior do ponto exato de parada, exibe modal amarelo warning com ícone de WiFi cortado título "Conexão Perdida" mensagem "Sincronização pausada em 8 de 12 unidades. Será retomada quando conexão voltar" e botões Retentar Agora tentando reconectar imediatamente ou Cancelar abortando e mantendo dados pendentes, se FIELD_AGENT escolhe Retentar app verifica conectividade via NetInfo.fetch() e se isConnected=true retoma de checkpoint carregando sync_checkpoint de AsyncStorage recuperando IDs já processados filtrando WHERE id NOT IN (synced_ids) evitando reenviar duplicatas e continua fase interrompida, se escolhe Cancelar app mantém needs_sync=true em todos registros pendentes incrementa retry_count e agenda retry automático com exponential backoff próxima tentativa em 1min depois 5min depois 15min máximo 3 tentativas, e listener de conectividade permanece ativo monitorando isConnected então quando conexão retorna app exibe notificação local "Conexão restaurada. Sincronizar agora?" com ação tap disparando retomada automática de checkpoint garantindo nenhum dado perdido e experiência resiliente em campo com conectividade instável típica de áreas rurais e comunidades periféricas.

**Ponto de Desvio:** Qualquer momento durante PULL ou PUSH (monitora conectividade continuamente)

**Retorno:** Sincronização pausada com checkpoint salvo, retomada quando conexão volta

---

**Última atualização:** 2025-12-30
