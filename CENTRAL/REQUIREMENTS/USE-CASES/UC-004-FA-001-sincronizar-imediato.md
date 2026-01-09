---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# UC-004-FA-001: Sincronizar Imediatamente

Fluxo alternativo do UC-004 Coletar Dados Campo Mobile desviando no passo 12 (após salvar localmente) quando app detecta conexão de rede disponível WiFi ou dados móveis permitindo sincronização imediata ao invés de acumular pendências para sync posterior, onde após salvar unidade localmente app verifica conectividade via NetInfo.fetch() retornando isConnected=true e exibe botão flutuante Sincronizar Agora com badge numérico indicando quantidade de itens pendentes. FIELD_AGENT opcionalmente clica em Sincronizar Agora disparando processo descrito detalhadamente em UC-005 Sincronizar Dados Offline que envia unidades fotos titulares pendentes para servidor via POST /api/sync/units endpoint, aguarda confirmação exibindo spinner com progresso "Sincronizando 3 de 12 unidades...", atualiza registros locais marcando needs_sync=false após sucesso, remove badges de pendência, e exibe toast "12 unidades sincronizadas com sucesso" permitindo continuar trabalho com storage local liberado.

**Ponto de Desvio:** Passo 12 do UC-004 (após salvar, antes de mover para próxima)

**Detecção de Conectividade:**
```typescript
import NetInfo from '@react-native-community/netinfo';

const state = await NetInfo.fetch();
if (state.isConnected && state.isInternetReachable) {
  showSyncButton();
}
```

**Retorno:** Dados sincronizados, storage local limpo, FIELD_AGENT continua coleta

---

**Última atualização:** 2025-12-30
