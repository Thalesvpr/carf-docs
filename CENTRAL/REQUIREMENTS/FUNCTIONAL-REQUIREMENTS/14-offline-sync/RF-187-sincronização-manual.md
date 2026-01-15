---
modules: [GEOWEB, REURBCAD]
epic: reliability
---

# RF-187: Sincronização Manual

O sistema disponibiliza botão de sincronização manual facilmente acessível na interface do aplicativo mobile que permite ao usuário acionar processo de sincronização de dados entre dispositivo local e servidor central no momento que julgar apropriado, proporcionando controle sobre quando transmissão de dados ocorrerá. Ao acionar sincronização, o sistema exibe indicador de progresso visível que informa usuário sobre andamento da operação incluindo quantos registros estão sendo enviados (push), quantos sendo recebidos (pull), percentual concluído e etapa atual como "enviando unidades", "baixando atualizações" ou "processando conflitos", mantendo transparência sobre processo complexo que pode envolver milhares de registros. Ao concluir sincronização, o sistema apresenta feedback claro e detalhado de sucesso indicando quantos registros foram sincronizados com êxito, ou feedback de erro especificando natureza do problema ocorrido como falha de conexão, timeout, erro de validação no servidor ou conflitos detectados, permitindo que usuário compreenda resultado da operação e tome ações corretivas se necessário. Esta abordagem de sincronização manual é preferível em contextos de conectividade limitada onde usuário deseja controlar quando consumir dados móveis ou aguardar disponibilidade de WiFi para realizar transferências de grande volume.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
