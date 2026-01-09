---
modules: [GEOWEB, REURBCAD]
epic: authentication
---

# UC-004-FE-003: Bateria Baixa

Fluxo de exceção do UC-004 Coletar Dados Campo Mobile ocorrendo em qualquer momento durante coleta quando app detecta nível de bateria crítico (<15%) arriscando desligamento inesperado e perda de dados não salvos, onde monitoramento executa via react-native-battery listener observando mudanças de battery level disparando callback quando cruza threshold configurado, app exibe notificação local persistente com ícone vermelho de bateria título "Bateria Baixa" mensagem "15% restantes. Salve dados importantes e considere modo economia" e botão Ativar Modo Economia. FIELD_AGENT pode ignorar notificação continuando operação normal assumindo risco, ou clicar Ativar Modo Economia disparando otimizações: desabilita GPS tracking contínuo mantendo apenas captura pontual quando necessário reduzindo drain de bateria significativo, reduz frequência de refresh de mapa de 60fps para 30fps economizando processamento gráfico, desabilita background sync automático mantendo apenas manual on-demand, reduz brilho de tela para 70% via react-native-screen-brightness, e exibe badge amarelo "Modo Economia" no header. App força auto-save a cada mudança de campo ao invés de apenas no final economizando dados parciais caso desligamento inesperado, exibe prompt de confirmação ao tentar tirar foto alertando "Tirar foto consome bateria. Continuar?" permitindo FIELD_AGENT decidir se essencial, e se bateria atingir nível crítico <5% força salvamento de unidade atual em progresso mesmo incompleta marcando flag incomplete=true e exibe modal urgente "Bateria crítica! Salvando dados..." com countdown antes de fechar app gracefully evitando corrupção de SQLite.

**Ponto de Desvio:** Qualquer momento durante UC-004 (monitora bateria continuamente)

**Monitoramento de Bateria:**
```typescript
import Battery from '@react-native-community/battery';

Battery.getBatteryLevel().then((level) => {
  if (level < 0.15 && !powerSavingMode) {
    showBatteryWarning(level);
  } else if (level < 0.05) {
    emergencySave();
  }
});
```

**Modo Economia:**
```typescript
const enablePowerSavingMode = async () => {
  // Desabilitar GPS contínuo
  await stopGPSTracking();

  // Reduzir framerate do mapa
  mapView.setFramerate(30);

  // Desabilitar sync automático
  disableAutoSync();

  // Reduzir brilho
  await ScreenBrightness.setBrightness(0.7);

  // Auto-save contínuo
  enableAutoSave(onFieldChange);

  setState({ powerSavingMode: true });
};
```

**Emergency Save (Bateria <5%):**
```typescript
const emergencySave = async () => {
  showModal({
    title: '🔴 Bateria Crítica',
    message: 'Salvando dados...',
    countdown: 3
  });

  // Salvar unidade atual mesmo incompleta
  await saveCurrentUnit({ incomplete: true, reason: 'battery_critical' });

  // Fechar app gracefully após 3s
  setTimeout(() => {
    BackHandler.exitApp();
  }, 3000);
};
```

**Retorno:** Modo economia ativo, FIELD_AGENT continua com limitações ou salva e encerra

---

**Última atualização:** 2025-12-30
