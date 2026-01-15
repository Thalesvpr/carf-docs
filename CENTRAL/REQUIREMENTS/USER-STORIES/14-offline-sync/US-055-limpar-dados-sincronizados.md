---
modules: [GEOWEB, REURBCAD]
epic: reliability
---

# US-055: Limpar Dados Sincronizados

Como agente de campo, quero limpar dados locais que já foram sincronizados com sucesso ao servidor para que espaço de armazenamento do dispositivo seja liberado, onde a funcionalidade deve fornecer botão "Limpar sincronizados" acessível em configurações ou menu de sincronização, garantindo confirmação obrigatória antes de executar limpeza para prevenir exclusões acidentais, permitindo que dados ainda não sincronizados sejam mantidos intactos no dispositivo possibilitando redownload posterior quando necessário. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com gestão de banco de dados local, integrada ao UC-005 (Sincronizar Dados Offline) para manutenção de armazenamento. Os critérios de aceitação incluem disponibilidade de botão "Limpar dados sincronizados" em menu de configurações ou tela de sincronização, exibição de diálogo de confirmação obrigatório mostrando quantidade de registros que serão removidos e espaço a ser liberado, execução de limpeza apenas de registros marcados como synced:true ou com confirmação de sincronização, preservação completa de registros com synced:false ou pendentes de sincronização durante limpeza, indicação visual de progresso durante processo de limpeza se volume de dados for significativo, exibição de resumo após conclusão mostrando quantidade de registros removidos e espaço liberado, capacidade de redownload de dados limpos através de nova sincronização pull quando necessário, e limpeza automática de arquivos associados (fotos documentos) cujos registros pais foram removidos para liberar espaço completo. A rastreabilidade conecta esta user story ao UC-005 (Sincronizar Dados Offline), garantindo gestão eficiente de armazenamento local sem comprometer dados pendentes de sincronização.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
