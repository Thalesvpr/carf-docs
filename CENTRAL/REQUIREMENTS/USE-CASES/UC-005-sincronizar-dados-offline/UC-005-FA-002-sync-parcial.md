---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# UC-005-FA-002: Sincronização Parcial (Apenas Fotos)

Fluxo alternativo do UC-005 Sincronizar Dados Offline desviando na tela de sincronização onde ao invés de sincronizar tudo (unidades titulares fotos), FIELD_AGENT clica opção Sincronizar Apenas Fotos economizando tempo quando dados cadastrais ainda sendo editados mas deseja liberar espaço de armazenamento enviando fotos grandes ao servidor, onde app exibe modal de confirmação mostrando estatísticas "45 fotos (23 MB) serão enviadas. Continuar?" com botões Sim e Cancelar, se FIELD_AGENT confirma app executa apenas fase PUSH do UC-005 filtrando query SELECT * FROM photos WHERE needs_sync=true AND synced_at IS NULL excluindo unidades e titulares do batch, comprime cada foto usando react-native-image-resizer redimensionando max 2048px quality 80% JPEG reduzindo tamanho típico ~80%, serializa metadados JSON incluindo photo_id unit_id filename client_timestamp e envia POST /api/sync/photos com Content-Type multipart/form-data respeitando timeout 5 minutos, servidor valida cada foto verificando unit_id exists e extension permitida (JPEG PNG) rejeitando outros formatos, salva binário em blob storage (AWS S3 Azure Blob) retornando server_photo_id e public_url, app recebe response processando results atualizando tabela photos local com server_id e url retornados marcando synced_at=NOW() e needs_sync=false para sucessos, deleta arquivo local da pasta cache após confirmação de upload bem-sucedido liberando storage imediatamente, exibe toast "45 fotos sincronizadas (23 MB liberados)" com ícone verde, e mantém unidades e titulares pendentes com needs_sync=true aguardando sincronização completa posterior permitindo FIELD_AGENT continuar editando sem bloquear workflow enquanto libera espaço crítico de dispositivo.

**Ponto de Desvio:** Tela de sincronização (opção específica ao invés de sincronização completa)

**Retorno:** Apenas fotos sincronizadas e deletadas localmente, dados cadastrais permanecem pendentes

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
