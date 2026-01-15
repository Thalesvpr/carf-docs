---
modules: [GEOWEB, REURBCAD]
epic: communities
---

# US-046: Ver Contador de Pendências

Como agente de campo, quero visualizar quantas unidades ainda faltam sincronizar com o servidor para que eu saiba o progresso do meu trabalho e possa planejar adequadamente o momento de sincronização, onde a funcionalidade deve exibir um badge visual com o número de registros pendentes de envio, garantindo acesso rápido a uma lista detalhada das unidades não sincronizadas com ordenação por data de criação, permitindo que o agente monitore continuamente o status de sincronização e tome decisões sobre quando executar upload dos dados coletados. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com contadores em tempo real baseados no banco de dados local, integrada ao UC-005 (Sincronizar Dados Offline) para gestão do processo de sync. Os critérios de aceitação incluem exibição de badge numérico visível na tela principal indicando quantidade total de registros pendentes de sincronização, atualização automática do contador em tempo real conforme novas unidades são cadastradas ou sincronizadas, acesso através de toque no badge a lista completa de unidades pendentes com informações resumidas (código nome data_cadastro), ordenação padrão da lista por data de criação descendente mostrando registros mais recentes primeiro, indicação visual diferenciada para unidades com erros de validação que impediriam sincronização, filtros opcionais na lista de pendências por comunidade ou data de criação, capacidade de acessar detalhes completos de cada unidade pendente diretamente da lista, e sincronização do contador entre diferentes sessões do aplicativo mantendo precisão após reinicialização. A rastreabilidade conecta esta user story ao UC-005 (Sincronizar Dados Offline), garantindo visibilidade do progresso de trabalho e status de sincronização para o agente de campo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
