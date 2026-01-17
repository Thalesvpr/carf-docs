---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: compatibility
---

# US-054: Resolver Conflitos de Dados

Como agente de campo, quero ser alertado quando houver conflitos de sincronização entre minha versão local e a versão do servidor para que eu possa decidir conscientemente qual versão manter ou se devo mesclar as informações, onde a funcionalidade deve detectar conflitos comparando timestamps updated_at do servidor versus local, garantindo exibição clara de interface mostrando diferenças (diff) entre versão local e servidor destacando campos modificados, permitindo que o agente escolha entre três estratégias de resolução (MANTER_LOCAL USAR_SERVIDOR MESCLAR) com padrão configurável server wins para casos não críticos. Esta funcionalidade é implementada pelo módulo GEOWEB com UI de resolução de conflitos coordenando com GEOAPI através do endpoint POST /api/sync/push que retorna conflitos detectados, integrada ao UC-005 (Sincronizar Dados Offline) para garantir integridade de dados. Os critérios de aceitação incluem detecção automática de conflito quando updated_at do servidor é posterior ao updated_at local do mesmo registro, interrupção de sincronização automática apresentando modal de conflito ao agente, exibição lado a lado de versão local versus versão servidor com destaque visual em campos diferentes, três opções claras de resolução sendo "Manter minha versão local" "Usar versão do servidor" e "Mesclar campos manualmente", interface de mesclagem permitindo selecionar campo por campo qual versão usar quando opção mesclar é escolhida, comportamento padrão server wins aplicado automaticamente se agente não responder dentro de timeout configurável ou em modo batch, logging completo de resolução de conflitos incluindo escolha feita e timestamp para auditoria, e possibilidade de desfazer resolução e tentar novamente caso agente mude de ideia imediatamente após escolha. A rastreabilidade conecta esta user story ao RF-190 (Resolução de Conflitos de Sincronização) e ao UC-005 (Sincronizar Dados Offline), garantindo controle do agente sobre integridade de dados em cenários de edição concorrente.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
