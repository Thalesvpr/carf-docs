---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-102: Obter Status de Exportação

Como analista executando exportação de dados volumosos, quero verificar progresso de exportação em andamento para que saber quando arquivo estará pronto para download, evitando espera indefinida na interface e permitindo continuar outras atividades enquanto processamento ocorre em background. A funcionalidade deve fornecer endpoint de consulta de status de job de exportação retornando informações detalhadas incluindo porcentagem de conclusão do processamento, quantidade de registros já exportados versus total a exportar, tempo decorrido desde início da operação, estimativa de tempo restante baseada em taxa de processamento observada, e status atual da operação (PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED). O sistema deve atualizar status em tempo real ou com latência máxima de poucos segundos permitindo polling eficiente pela interface, incluindo informações de erro detalhadas quando exportação falha indicando causa raiz (timeout, limite de memória, erro de validação, disco cheio) e recomendações de ação corretiva. Quando exportação completa com sucesso, response deve incluir URL de download do arquivo gerado, tamanho do arquivo em bytes, hash de integridade para validação, e timestamp de expiração indicando até quando arquivo estará disponível para download. Os critérios de aceitação incluem endpoint implementado retornando objeto JSON com campos status, progress_percent, records_processed, total_records, elapsed_time, estimated_remaining_time e download_url quando aplicável, validação de permissões garantindo que usuário só possa consultar status de suas próprias exportações ou de seu tenant conforme role, tratamento adequado de erros incluindo export_id não encontrado ou expirado, documentação OpenAPI com descrição de todos os estados possíveis e transições, e testes unitários e de integração validando ciclo completo de vida de exportação. Esta User Story está relacionada ao RF-197 e é implementada através do endpoint GET /api/exports/{id} no backend GEOAPI com sistema de jobs assíncronos, e componente de monitoramento no frontend GEOWEB com auto-refresh, pertencendo ao Epic 10: Relatórios e Exportação. O status atual é proposed, com funcionalidade existente mas documentação formal criada posteriormente.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
