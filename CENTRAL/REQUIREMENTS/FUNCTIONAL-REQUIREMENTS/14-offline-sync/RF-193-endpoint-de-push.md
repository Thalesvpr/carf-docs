---
modules: [GEOAPI, REURBCAD]
epic: compatibility
---

# RF-193: Endpoint de Push

A GEOAPI disponibiliza endpoint POST /api/sync/push que recebe dados criados ou editados offline pelos aplicativos móveis, aceitando payload contendo array de changes onde cada elemento representa operação de criação, atualização ou deleção a ser aplicada no banco de dados central. O endpoint implementa validação rigorosa de dados recebidos verificando conformidade com schema esperado, presença de campos obrigatórios, validade de tipos de dados e constraints de negócio como unicidade de identificadores e integridade referencial, rejeitando operações inválidas com mensagens de erro descritivas que permitem correção pelo cliente. Durante processamento, o sistema executa detecção de conflitos comparando timestamps de última atualização dos registros recebidos com versões existentes no servidor, identificando casos onde registro foi modificado por outro usuário entre momento da edição offline e momento da sincronização. O endpoint retorna resposta estruturada contendo mapeamento de IDs onde UUIDs gerados localmente pelos dispositivos móveis são associados aos IDs definitivos atribuídos pelo servidor após persistência, permitindo que cliente atualize suas referências locais e estabeleça correspondência entre registros locais temporários e registros permanentes no sistema central, essencial para manter consistência referencial quando registros relacionados foram criados offline.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
