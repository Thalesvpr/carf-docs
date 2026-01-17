---
modules: [GEOWEB, REURBCAD]
epic: authentication
---

# UC-004-FE-003: Bateria Baixa

Fluxo de exceção do UC-004 Coletar Dados Campo Mobile ocorrendo em qualquer momento durante coleta quando app detecta nível de bateria crítico (<15%) arriscando desligamento inesperado e perda de dados não salvos, onde monitoramento executa via react-native-battery listener observando mudanças de battery level disparando callback quando cruza threshold configurado, app exibe notificação local persistente com ícone vermelho de bateria título "Bateria Baixa" mensagem "15% restantes. Salve dados importantes e considere modo economia" e botão Ativar Modo Economia. FIELD_AGENT pode ignorar notificação continuando operação normal assumindo risco, ou clicar Ativar Modo Economia disparando otimizações: desabilita GPS tracking contínuo mantendo apenas captura pontual quando necessário reduzindo drain de bateria significativo, reduz frequência de refresh de mapa de 60fps para 30fps economizando processamento gráfico, desabilita background sync automático mantendo apenas manual on-demand, reduz brilho de tela para 70% via react-native-screen-brightness, e exibe badge amarelo "Modo Economia" no header. App força auto-save a cada mudança de campo ao invés de apenas no final economizando dados parciais caso desligamento inesperado, exibe prompt de confirmação ao tentar tirar foto alertando "Tirar foto consome bateria. Continuar?" permitindo FIELD_AGENT decidir se essencial, e se bateria atingir nível crítico <5% força salvamento de unidade atual em progresso mesmo incompleta marcando flag incomplete=true e exibe modal urgente "Bateria crítica! Salvando dados..." com countdown antes de fechar app gracefully evitando corrupção de SQLite.

**Ponto de Desvio:** Qualquer momento durante UC-004 (monitora bateria continuamente)

**Monitoramento de Bateria:**

App importa Battery de pacote @react-native-community/battery, executa Battery.getBatteryLevel() retornando Promise com level entre zero e um representando percentual, encadeia then recebendo callback com level verificando condição if level menor zero ponto quinze AND NOT powerSavingMode chamando showBatteryWarning passando level exibindo notificação quando bateria atinge quinze por cento, else if level menor zero ponto zero cinco chamando emergencySave() forçando salvamento de emergência quando bateria crítica abaixo cinco por cento evitando perda de dados por desligamento inesperado.

**Modo Economia:**

Função async enablePowerSavingMode executa cinco otimizações sequenciais sendo await stopGPSTracking() desabilitando tracking contínuo mantendo apenas captura pontual reduzindo drain significativo, mapView.setFramerate com trinta reduzindo refresh de sessenta para trinta fps economizando processamento gráfico, disableAutoSync() desabilitando background sync automático mantendo apenas manual on-demand, await ScreenBrightness.setBrightness com zero ponto sete reduzindo brilho para setenta por cento, enableAutoSave passando callback onFieldChange salvando incrementalmente a cada mudança ao invés de apenas no final, finalizando com setState atualizando powerSavingMode para true exibindo badge amarelo "Modo Economia" no header.

**Emergency Save (Bateria <5%):**

Função async emergencySave executa showModal passando objeto com title igual "Bateria Crítica" com ícone vermelho, message igual "Salvando dados...", e countdown igual três exibindo contagem regressiva, executa await saveCurrentUnit passando objeto com incomplete igual true e reason igual battery_critical salvando unidade em progresso mesmo parcialmente preenchida marcando flag para revisão posterior, chama setTimeout com callback executando BackHandler.exitApp() e delay três mil milissegundos fechando app gracefully após três segundos permitindo salvamento completo evitando corrupção de SQLite por desligamento abrupto durante escrita.

**Retorno:** Modo economia ativo, FIELD_AGENT continua com limitações ou salva e encerra

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
