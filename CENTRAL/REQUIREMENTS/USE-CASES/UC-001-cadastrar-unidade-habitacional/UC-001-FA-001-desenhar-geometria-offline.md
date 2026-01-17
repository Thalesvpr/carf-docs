---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# UC-001-FA-001: Desenhar Geometria Offline (Mobile)

Fluxo alternativo do UC-001 Cadastrar Unidade Habitacional desviando no passo 5 (desenho de geometria) quando usuário FIELD_AGENT opera app mobile React Native em campo sem conexão de rede, onde ao invés de desenhar polígono manualmente no mapa o app oferece opção Capturar com GPS ativando módulo de geolocalização do dispositivo que coleta pontos GPS em tempo real conforme agente caminha pelo perímetro da unidade habitacional marcando vértices a cada 3-5 metros automaticamente ou manualmente pressionando botão Adicionar Ponto, sistema exibe trilha em tempo real no mapa offline carregado previamente via tiles cached mostrando precisão atual do GPS em metros (ideal <5m aceitável <10m), usuário pode ajustar manualmente os vértices arrastando marcadores no mapa touchscreen para corrigir imprecisões do GPS ou obstáculos que impediram caminhada exata no perímetro, ao finalizar captura usuário pressiona Concluir Polígono e sistema fecha automaticamente conectando último ponto ao primeiro verificando que polígono é válido (mínimo 3 pontos sem auto-interseções), calcula área aproximada em m², e salva geometria localmente em banco SQLite do WatermelonDB incluindo metadados de precisão GPS média timestamp de captura e flag needs_sync=true indicando pendência de sincronização com servidor. Geometria salva localmente permanece editável até sincronização permitindo ajustes posteriores, aparece no mapa offline com badge laranja Pendente Sincronização, e quando conexão de rede retornar (detectada por listener de conectividade) o SyncService dispara automaticamente sincronização incremental enviando geometria para backend via POST /api/units endpoint que valida servidor-side e retorna confirmação atualizando flag needs_sync=false e alterando badge para verde Sincronizado, com tratamento de conflito se unidade foi modificada no servidor entre captura offline e sincronização exibindo tela de merge manual.

**Ponto de Desvio:** Passo 5 do UC-001 (desenho de geometria)

**Tecnologias:**
- React Native Geolocation API para captura GPS
- WatermelonDB (SQLite) para persistência offline
- MapLibre GL Native para renderização de mapa offline
- SyncService para sincronização incremental

**Retorno:** Volta ao passo 6 do UC-001 (cálculo de área) com geometria capturada via GPS salva localmente

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
