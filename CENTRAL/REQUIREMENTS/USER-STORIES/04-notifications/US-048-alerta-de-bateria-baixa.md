---
modules: [GEOWEB, REURBCAD]
epic: audit
---

# US-048: Alerta de Bateria Baixa

Como agente de campo, quero ser alertado quando a bateria do dispositivo estiver abaixo de 20% para que eu possa salvar dados e sincronizar antes que o dispositivo desligue, onde a funcionalidade deve exibir alerta visual proeminente quando o nível de bateria atingir o limiar crítico, garantindo sugestão clara de executar sincronização imediata dos dados pendentes, permitindo ativação opcional de modo economia de energia que reduz funcionalidades secundárias para prolongar autonomia do dispositivo durante trabalho de campo. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com monitoramento nativo de bateria do sistema operacional, integrada ao UC-004 (Cadastrar Unidade no Campo) para proteção de dados durante coleta. Os critérios de aceitação incluem monitoramento contínuo do nível de bateria do dispositivo em background sem impacto significativo no consumo, exibição de alerta visual destacado (notificação ou modal) quando bateria atingir exatamente 20% de carga, mensagem clara no alerta sugerindo sincronização imediata de dados pendentes antes que bateria se esgote, botão de ação rápida no alerta permitindo iniciar sincronização diretamente sem navegar menus, opção de ativar modo economia de energia que desabilita funcionalidades de alto consumo (reduz frequência de atualização GPS desabilita animações reduz brilho), indicador visual persistente do modo economia quando ativo, alerta adicional em 10% de bateria caso sincronização ainda não tenha sido realizada, e salvamento automático de rascunhos de formulários em edição quando alerta de bateria crítica é exibido. A rastreabilidade conecta esta user story ao UC-004 (Cadastrar Unidade no Campo), garantindo proteção contra perda de dados por esgotamento de bateria durante trabalho de campo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
