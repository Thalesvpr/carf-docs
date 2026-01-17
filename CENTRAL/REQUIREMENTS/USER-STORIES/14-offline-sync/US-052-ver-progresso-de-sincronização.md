---
modules: [GEOWEB, REURBCAD]
epic: audit
---

# US-052: Ver Progresso de Sincronização

Como agente de campo, quero visualizar o progresso detalhado da sincronização em andamento para que eu saiba quanto tempo ainda falta e quantos itens já foram processados, onde a funcionalidade deve exibir barra de progresso visual com percentual de conclusão atualizado em tempo real, garantindo exibição clara de contador mostrando "X de Y itens sincronizados" para transparência do processo, permitindo que o agente cancele a sincronização em andamento caso necessário retornando ao estado anterior sem corromper dados. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com feedback visual contínuo durante processo coordenado pelo GEOAPI, integrada ao UC-005 (Sincronizar Dados Offline) para transparência operacional. Os critérios de aceitação incluem exibição de barra de progresso visual com percentual de 0% a 100% durante sincronização ativa, atualização em tempo real do percentual conforme itens são processados sem travamentos de interface, contador textual mostrando quantidade absoluta "X de Y itens sincronizados" complementando percentual, diferenciação visual entre fase de envio (push) e recebimento (pull) quando aplicável, botão "Cancelar" acessível durante todo processo de sincronização, confirmação antes de cancelar alertando que processo será interrompido, garantia de integridade de dados após cancelamento sem deixar registros em estado inconsistente, e persistência de progresso permitindo retomar sincronização de onde parou caso aplicativo seja fechado acidentalmente. A rastreabilidade conecta esta user story ao UC-005 (Sincronizar Dados Offline), garantindo transparência completa e controle sobre processo de sincronização.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
