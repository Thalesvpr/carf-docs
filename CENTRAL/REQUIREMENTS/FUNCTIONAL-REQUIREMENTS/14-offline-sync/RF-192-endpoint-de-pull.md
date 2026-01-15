---
modules: [GEOAPI, REURBCAD]
epic: compatibility
---

# RF-192: Endpoint de Pull

A GEOAPI fornece endpoint especializado GET /api/sync/pull que implementa sincronização incremental eficiente para dispositivos móveis, aceitando parâmetro de query lastPulledAt contendo timestamp ISO 8601 que indica momento da última sincronização bem-sucedida do cliente. O endpoint processa requisição consultando banco de dados para identificar todos os registros (unidades, titulares, fotos, etc.) que foram criados, modificados ou deletados após timestamp fornecido, retornando apenas esse subconjunto de alterações em vez de transmitir base completa de dados. A resposta é estruturada em formato JSON otimizado que agrupa alterações por tipo de operação incluindo arrays created contendo registros novos, updated contendo registros modificados com todos os campos atualizados, e deleted contendo apenas identificadores de registros removidos, permitindo que cliente aplique localmente essas mudanças de forma eficiente sobre sua base local. O payload retornado utiliza formato JSON compacto que omite campos nulos, utiliza nomes de atributos abreviados quando possível e pode aplicar compressão gzip no nível HTTP, minimizando tamanho da transferência especialmente crítico em conexões móveis lentas ou limitadas, garantindo que mesmo sincronizações de grandes volumes de alterações possam ser completadas em tempo razoável.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
