---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: scalability
---

# UC-001-FE-003: Perda de Conexão (Mobile)

Fluxo de exceção do UC-001 Cadastrar Unidade Habitacional ocorrendo no passo 10 (salvamento no servidor) quando app mobile React Native detecta falta de conexão de rede impedindo comunicação HTTP com backend GEOAPI, onde detecção de conectividade utiliza listener de NetInfo monitorando eventos de mudança de estado de rede (connected disconnected) e verificando isConnected antes de cada requisição HTTP, ao detectar offline durante tentativa de POST /api/units para criar unidade sistema intercepta erro de rede (Network Request Failed ou Timeout) antes de exibir mensagem de falha genérica ao usuário, aplica estratégia offline-first salvando dados localmente em banco SQLite do WatermelonDB criando registro na tabela units_local com todos campos preenchidos no formulário (código endereço geometria tipo observações) mais metadados de sincronização (needs_sync=true sync_status=PENDING created_offline=true local_id=UUID tentativas=0 last_attempt=null), exibe toast notification amigável "Sem conexão. Unidade salva localmente" com ícone laranja de alerta e badge visual "Pendente de Sincronização" sobreposto no card da unidade em listagens, permite usuário continuar operando offline visualizando editando e criando mais unidades localmente sem bloqueio de funcionalidades críticas, e registra operação pendente em fila de sincronização gerenciada por SyncService background worker. Quando conexão de rede retornar (detectada por listener NetInfo.addEventListener('connectionChange') disparando callback com isConnected=true) SyncService ativa automaticamente disparando processo de sincronização incremental que itera sobre registros com needs_sync=true ordenados por created_at, para cada unidade pendente executa POST /api/units enviando payload completo com campos locais mais metadado local_id para rastreamento, aguarda resposta 201 Created com server_id retornado, atualiza registro local substituindo local_id por server_id retornado, marca needs_sync=false e sync_status=SYNCED, remove badge "Pendente", e em caso de erro HTTP (409 Conflict duplicação 400 Bad Request validação falhou 401 Unauthorized token expirado) incrementa contador tentativas adiciona timestamp last_attempt e agenda retry com exponential backoff (1min 5min 15min 1h máximo 5 tentativas) exibindo notificação persistente "N unidades falharam ao sincronizar. Toque para revisar" que abre tela de resolução manual listando erros específicos permitindo editar dados locais e re-tentar ou descartar unidade local se for duplicata confirmada.

**Ponto de Desvio:** Passo 10 do UC-001 (salvamento no servidor)

**Detecção de Offline:**
- NetInfo listener monitora mudanças de conectividade
- Verificação isConnected antes de requisição HTTP
- Interceptação de erros Network Request Failed ou Timeout

**Persistência Local:**

Schema WatermelonDB define model units_local decorado com @model contendo campos @field local_id tipo string UUID gerado localmente, @field server_id tipo string nullable recebendo ID retornado após sincronização bem-sucedida, @field code tipo string armazenando código unidade, @json address com sanitizer sanitizeAddress tipo Address objeto endereço completo, @json geometry com sanitizer sanitizeGeometry tipo GeoJSON polígono desenhado, @field type tipo UnitType enumeração casa apartamento comercial, @field needs_sync tipo boolean flag indicando sincronização pendente, @field sync_status tipo union PENDING SYNCED FAILED rastreando estado sincronização, @field created_offline tipo boolean identificando criação offline, @field tentativas tipo number contador falhas sincronização, @date last_attempt tipo Date nullable timestamp última tentativa sincronização permitindo retry logic exponential backoff.

**Processo de Sincronização:**
1. Listener detecta conexão retornou (isConnected=true)
2. SyncService busca registros WHERE needs_sync=true ORDER BY created_at
3. Para cada registro:
   - POST /api/units com payload + local_id
   - Se 201 Created: atualiza server_id, needs_sync=false, sync_status=SYNCED
   - Se erro: incrementa tentativas, agenda retry com backoff
4. Exibe notificação de sucesso ou falha

**Tratamento de Erros:**
- 409 Conflict (código duplicado): Permite editar código local e re-tentar
- 400 Bad Request (validação falhou): Exibe erros, permite editar campos
- 401 Unauthorized (token expirado): Força re-login e re-tenta
- 500 Server Error: Retry automático com backoff

**Retorno:** Sincronização assíncrona em background, usuário pode continuar operando

---

**Última atualização:** 2025-12-30
