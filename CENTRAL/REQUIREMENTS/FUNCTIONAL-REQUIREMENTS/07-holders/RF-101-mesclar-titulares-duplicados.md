---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# RF-101: Mesclar Titulares Duplicados

O sistema deve permitir que administradores (perfil ADMIN) mesclem registros duplicados de titulares consolidando informações em único registro correto, onde interface oferece seleção de múltiplos titulares suspeitos de serem duplicatas através de checkboxes em listagem ou ferramenta dedicada de detecção de duplicatas baseada em similaridade de nome e CPF. Após seleção dos titulares a mesclar, wizard apresenta comparação lado-a-lado dos dados permitindo que administrador escolha para cada campo qual valor deve ser mantido no registro consolidado (selecionando melhor informação de entre os duplicados) ou editar manualmente campo específico compondo valor ótimo. Todas as vinculações com unidades (unit_holders) dos titulares duplicados são automaticamente transferidas para titular consolidado garantindo que nenhuma relação seja perdida durante mesclagem, onde vinculações redundantes (mesmo titular duplicado vinculado múltiplas vezes à mesma unidade) são deduplicadas mantendo apenas um vínculo. Os registros duplicados originais são inativados (soft delete) ao invés de excluídos permanentemente preservando rastreabilidade da operação de mesclagem e possibilitando eventual reversão se mesclagem foi realizada incorretamente, onde log de auditoria registra detalhadamente quais titulares foram mesclados em qual resultado. Implementado nos módulos GEOWEB e GEOAPI com prioridade Could-have, este recurso é essencial para limpeza e qualidade de cadastros que naturalmente acumulam duplicatas ao longo do tempo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
