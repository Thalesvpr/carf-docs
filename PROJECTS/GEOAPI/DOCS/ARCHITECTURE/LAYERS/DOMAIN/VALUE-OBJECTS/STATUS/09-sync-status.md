# SyncStatus

Value object enum representando estado de sincronização de operações offline do aplicativo mobile REURBCAD com servidor GEOAPI, permitindo rastreamento e resolução de conflitos em cenários de conectividade intermitente. Valores possíveis são PENDING (operação enviada pelo dispositivo aguardando processamento no servidor), SUCCESS (sincronização completada com sucesso e dados persistidos), CONFLICT (conflito detectado quando BaseVersion do dispositivo difere do RowVersion atual no servidor) e FAILED (falha no processamento por erro de validação, constraint violada ou exception).

Métodos incluem IsResolved() verificando se está em estado final (SUCCESS ou resolvido manualmente após CONFLICT), RequiresUserIntervention() determinando se CONFLICT precisa resolução manual quando campos iguais foram alterados diferentemente, CanRetry() verificando se FAILED pode ser reenviado após correção, e ToDisplayString() retornando mensagem amigável para mostrar ao usuário no app.

Usado em SyncLog.Status para rastrear cada operação CREATE/UPDATE/DELETE enviada pelo mobile, dispara SyncConflictEvent quando detecta BaseVersion diferente do RowVersion permitindo estratégia de merge automático para campos distintos ou apresentação de UI de resolução manual ao técnico de campo, garantindo que nenhum dado seja perdido em cenários de trabalho offline prolongado.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
