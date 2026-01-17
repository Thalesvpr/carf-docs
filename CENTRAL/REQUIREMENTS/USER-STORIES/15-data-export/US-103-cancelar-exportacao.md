---
modules: [GEOAPI, GEOWEB]
epic: maintainability
---

# US-103: Cancelar Exportação

Como analista que iniciou exportação por engano ou com parâmetros incorretos, quero cancelar exportação em andamento para que liberar recursos do servidor seja possível, evitando processamento desnecessário que consome CPU, memória e disco, e permitindo reiniciar exportação com configurações corretas. A funcionalidade deve disponibilizar endpoint de cancelamento de job de exportação que interrompe processamento em background de forma segura garantindo cleanup adequado de recursos temporários, incluindo remoção de arquivos parciais gerados, liberação de conexões de banco de dados mantidas pelo job, e atualização de status do registro de exportação para CANCELLED com timestamp e usuário que solicitou cancelamento. O sistema deve implementar cancelamento gracioso permitindo que iteração atual de processamento seja concluída antes de interrupção total, evitando corrupção de estado ou inconsistência de dados, mas garantindo resposta ao pedido de cancelamento em tempo razoável (máximo 30 segundos). A operação de cancelamento deve ser registrada em audit log incluindo identificação do usuário solicitante, timestamp da solicitação, e export_id afetado, permitindo rastreabilidade e análise de padrões de uso. O sistema deve validar permissões garantindo que apenas o usuário que criou a exportação ou administradores possam cancelá-la, impedindo interferência não autorizada em operações de outros usuários. Os critérios de aceitação incluem endpoint implementado aceitando POST /api/exports/{id}/cancel que retorna confirmação de cancelamento ou erro se operação já foi concluída, validação de permissões verificando ownership do job ou role administrativo, tratamento adequado de erros incluindo export_id não encontrado, exportação já finalizada ou já cancelada, documentação OpenAPI descrevendo condições de sucesso e falha, e testes unitários e de integração validando interrupção segura de processamento e cleanup de recursos. Esta User Story está relacionada ao RF-197 e é implementada através do endpoint POST /api/exports/{id}/cancel no backend GEOAPI com controle de ciclo de vida de jobs assíncronos, e botão de ação no frontend GEOWEB em interface de monitoramento, pertencendo ao Epic 10: Relatórios e Exportação. O status atual é proposed, com funcionalidade implementada mas documentação formal criada após desenvolvimento inicial.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
