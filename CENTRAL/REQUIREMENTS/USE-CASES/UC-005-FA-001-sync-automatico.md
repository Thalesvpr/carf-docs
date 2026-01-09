---
modules: [GEOWEB, REURBCAD]
epic: security
---

# UC-005-FA-001: Sincronização Automática em Background

Fluxo alternativo do UC-005 Sincronizar Dados Offline desviando no gatilho de início onde ao invés de FIELD_AGENT clicar manualmente botão Sincronizar, o app executa sincronização automática em background a cada 15 minutos quando conexão disponível usando react-native-background-fetch configurado com minimumFetchInterval=900 registrando task headless que roda mesmo com app minimizado, onde task verifica pré-condições checando se needs_sync=true existem pendências locais via query SELECT COUNT(*) FROM units_local WHERE needs_sync=true AND synced_at IS NULL retornando count > 0, verifica conectividade atual via NetInfo.fetch() retornando isConnected=true e type não metered (WiFi não dados móveis evitando consumo de franquia), e valida token JWT não expirado decodificando exp claim comparando com Date.now(), se todas condições satisfeitas dispara processo completo de sincronização executando fases PULL PUSH RESOLUÇÃO descritas no fluxo principal do UC-005 silenciosamente sem interromper FIELD_AGENT, exibe apenas notificação local discreta após conclusão mostrando "12 unidades sincronizadas em background" com ícone verde checkmark permitindo tap para abrir detalhes, e se falha ocorre armazena erro em sync_errors table agendando retry com exponential backoff próxima tentativa em 1min depois 5min depois 15min máximo 3 tentativas antes de exigir intervenção manual, garantindo dados sempre atualizados minimizando janela de divergência entre local e servidor sem requerer ação explícita de usuário otimizando workflow de campo onde FIELD_AGENT foca em coleta enquanto sincronização gerencia-se automaticamente.

**Ponto de Desvio:** Início do UC-005 (trigger automático ao invés de manual)

**Retorno:** Sincronização completa silenciosa, notificação de resumo exibida

---

**Última atualização:** 2025-12-30
