---
modules: [GEOAPI, REURBCAD]
epic: security
---

# UC-005-FE-004: Espaço Insuficiente (Pull)

Fluxo de exceção do UC-005 Sincronizar Dados Offline ocorrendo na fase PULL quando app baixa atualizações do servidor enviando GET /api/sync/pull recebendo response JSON com delta de dados modificados incluindo arrays de units holders photos com total_size header indicando tamanho estimado em bytes do payload completo incluindo binários de fotos, app verifica espaço disponível em dispositivo usando DeviceInfo.getFreeDiskStorage() retornando bytes livres comparando com total_size + buffer_safety (margem segurança 100MB) detectando free_space < required_space indicando armazenamento insuficiente para baixar todas atualizações sem arriscar preencher disco completamente travando sistema operacional, onde app aborta pull imediatamente sem baixar parcialmente evitando estado inconsistente exibe modal amarelo warning com ícone de storage título "Espaço Insuficiente" mensagem "Necessário 250 MB livres para baixar atualizações. Disponível: 85 MB" mostrando diferença clara, e oferece ações: Liberar Espaço abrindo gerenciador de storage nativo via Linking.openSettings() permitindo usuário deletar apps fotos vídeos desnecessários manualmente, Sincronizar Apenas Enviar executando apenas fase PUSH do UC-005 enviando pendências locais ao servidor liberando espaço após confirmação sem baixar atualizações (operação segura pois envia divergências locais primeiro priorizando não perder coletas de campo), Limpar Cache deletando tiles de mapa WMS layers temporários armazenados em cache_dir recuperando espaço típico 50-200MB sem perder dados de unidades, ou Cancelar abortando sincronização mantendo estado atual, após liberar espaço suficiente FIELD_AGENT retenta sincronização e app re-verifica free_space agora satisfazendo threshold prossegue com pull baixando atualizações normalmente, garantindo integridade impedindo corrupção de banco SQLite por disco cheio e orientando usuário com opções claras recovery sem requerer conhecimento técnico avançado típico de campo.

**Ponto de Desvio:** Fase PULL do UC-005 (após receber total_size mas antes de baixar)

**Retorno:** Após liberar espaço, FIELD_AGENT retenta e pull completa com sucesso

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
