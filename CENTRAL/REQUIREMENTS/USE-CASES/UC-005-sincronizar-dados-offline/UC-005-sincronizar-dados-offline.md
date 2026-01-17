---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: security
---

# UC-005: Sincronizar Dados Offline

Caso de uso permitindo app mobile REURBCAD sincronizar dados coletados offline por FIELD_AGENT com servidor backend GEOAPI usando estratégia de delta sync bidirecional incremental minimizando tráfego de dados e otimizando para conexões instáveis de campo, após verificar pré-condições de existência de dados pendentes marcados needs_sync=true em SQLite local, conexão com internet disponível detectada via NetInfo, e token de autenticação JWT válido não expirado. Fluxo principal inicia quando app detecta conexão disponível disparando listener de conectividade ou quando FIELD_AGENT manualmente clica botão Sincronizar após acumular pendências, exibe notificação local "Sincronização disponível (12 pendências)" com ação tap abrindo tela de sincronização fullscreen mostrando progress bar steps indicando fases PULL PUSH RESOLUÇÃO, contador de itens processados "Sincronizando 3 de 12 unidades...", e botão Cancelar permitindo abortar se necessário. Fase 1 PULL baixa atualizações do servidor enviando GET /api/sync/pull com query param last_sync_timestamp contendo ISO 8601 timestamp da última sincronização bem-sucedida armazenado em AsyncStorage, servidor executa query SELECT * FROM units WHERE updated_at > $last_sync AND tenant_id = $tenant retornando apenas delta de dados modificados desde última sync incluindo criações atualizações exclusões agrupadas por tipo de entidade (units holders unit_holders photos), app recebe response JSON processando arrays de changes aplicando localmente onde criações inserem novos registros em tables correspondentes usando IDs do servidor, atualizações fazem UPDATE em registros existentes matchando por server_id verificando row_version para detectar conflitos, exclusões marcam deleted_at em registros locais respeitando soft delete sem apagar fisicamente, e durante processamento app compara timestamps local vs remoto detectando conflitos quando mesma entidade foi editada tanto localmente quanto remotamente armazenando em conflicts table para resolução posterior exibindo badge numérico. Fase 2 PUSH envia alterações locais coletando todos registros WHERE needs_sync=true AND synced_at IS NULL ordenados por created_at garantindo ordem cronológica de operações, agrupa por tipo de entidade (unidades titulares fotos) para batch processing eficiente, comprime fotos antes de envio usando react-native-image-resizer redimensionando para max 2048px mantendo aspect ratio e quality 80% JPEG reduzindo tamanho típico de 3-5MB para 200-400KB economizando dados móveis e tempo de upload, serializa dados em JSON incluindo metadados client_id (UUID local) operation_type (CREATE UPDATE DELETE) timestamp client_timestamp para reconciliação, envia POST /api/sync/push com Content-Type multipart/form-data incluindo JSON de changes e binários de fotos comprimidas respeitando timeout de 5 minutos configurável, servidor processa batch validando cada change executando regras de negócio (CPF válido geometria válida percentuais soma ≤100%) retornando array de results com status SUCCESS ERROR CONFLICT para cada item incluindo server_id gerado para criações bem-sucedidas permitindo mapeamento UUID local → GUID servidor, e app recebe response processando results atualizando registros locais com server_ids retornados, marcando synced_at=NOW() e needs_sync=false para sucessos, mantendo needs_sync=true e incrementando retry_count para erros permitindo retry posterior, e armazenando conflitos em conflicts table para resolução manual. Fase 3 RESOLUÇÃO DE CONFLITOS executa se conflicts detectados exibindo tela listando conflitos com UI diff mostrando lado-a-lado versão local vs remota destacando campos diferentes, para cada conflito FIELD_AGENT decide Manter Local sobrescrevendo servidor enviando PATCH forçado, Aceitar Remoto descartando alterações locais aplicando versão servidor, ou Mesclar Manualmente editando campos individuais escolhendo valor apropriado de cada fonte, após resolver todos conflitos app reenvia dados com flag conflict_resolution=true e strategy escolhida, e servidor aplica resolução atualizando registros definitivamente. App ao concluir todas fases atualiza AsyncStorage salvando current timestamp como last_sync_timestamp para próxima sincronização delta, exibe modal de resumo mostrando estatísticas "12 unidades sincronizadas, 45 fotos enviadas (23 MB), 2 conflitos resolvidos, 1 erro (revisar)" com detalhamento clicável para cada categoria, remove badge numérico de pendências do ícone de sincronização se tudo sincronizado ou mantém badge atualizado se erros pendentes, e exibe toast de sucesso verde "Sincronização concluída com sucesso" ou warning amarelo "Sincronização parcial - 1 item pendente" permitindo FIELD_AGENT revisar erros e retentar. Fluxos alternativos incluem sincronização automática em background a cada 15 minutos quando online (UC-005-FA-001) e sincronização parcial apenas fotos economizando tempo quando dados cadastrais ainda sendo editados (UC-005-FA-002). Fluxos de exceção cobrem perda de conexão durante sync pausando e retomando (UC-005-FE-001), erro de validação no servidor permitindo editar e retentar (UC-005-FE-002), token expirado forçando refresh ou re-login (UC-005-FE-003), e espaço insuficiente para pull sugerindo limpar cache (UC-005-FE-004).

**Fluxos Alternativos:**
- UC-005-FA-001: Sincronização automática em background
- UC-005-FA-002: Sincronização parcial (apenas fotos)

**Fluxos de Exceção:**
- UC-005-FE-001: Perda de conexão durante sync
- UC-005-FE-002: Erro de validação no servidor
- UC-005-FE-003: Token expirado
- UC-005-FE-004: Espaço insuficiente (pull)

**Regras de Negócio:**
- RN-001: Sincronização usa delta sync (apenas dados modificados desde last_sync_timestamp)
- RN-002: Pull antes de push (sempre baixar atualizações do servidor primeiro evitando conflitos)
- RN-003: Conflitos devem ser resolvidos antes de marcar como sincronizado impedindo inconsistências
- RN-004: Fotos comprimidas antes de envio (max 2048px quality 80% JPEG reduzindo ~80% tamanho)
- RN-005: Timeout de sincronização 5 minutos evitando bloqueio infinito em conexões lentas
- RN-006: Retry automático com exponential backoff (1min 5min 15min máximo 3 tentativas)

**Rastreabilidade:**
- RF-187, RF-188, RF-189, RF-190, RF-192, RF-193, RF-194, RF-195
- US-050, US-051, US-052

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
