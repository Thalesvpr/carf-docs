---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: reliability
---

# US-041: Desenhar Geometria com GPS

Como agente de campo, quero capturar geometria usando GPS do celular para que a precisão dos dados coletados seja adequada durante o cadastramento de unidades no campo, onde a funcionalidade deve incluir um modo "caminhar perímetro" que coleta pontos automaticamente a cada 2 segundos enquanto o agente percorre os limites da unidade, garantindo precisão mínima de 5 metros através da validação de sinal GPS antes de iniciar a captura, permitindo que o polígono seja fechado automaticamente ao completar o perímetro ou manualmente pelo agente caso necessário. Esta funcionalidade é implementada principalmente pelo módulo GEOWEB na interface mobile e processada pelo GEOAPI no backend, incluindo validações geométricas como detecção de auto-interseção e cálculo de área mínima aceitável. Os critérios de aceitação incluem a disponibilidade do modo de captura por perímetro caminhado, coleta automática de pontos georreferenciados em intervalos regulares de 2 segundos, validação de precisão GPS mínima de 5 metros antes de aceitar cada ponto, capacidade de fechar o polígono automaticamente quando o agente retorna ao ponto inicial ou manualmente via botão dedicado, exibição em tempo real dos pontos coletados no mapa offline, feedback visual da qualidade do sinal GPS (EXCELENTE BOM REGULAR RUIM), opção de pausar e retomar a captura sem perder dados, e capacidade de desfazer os últimos pontos capturados caso necessário. A rastreabilidade conecta esta user story ao RF-066 (Captura de Geometria por GPS) e ao UC-004 (Cadastrar Unidade no Campo), garantindo alinhamento com os requisitos funcionais do sistema.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
