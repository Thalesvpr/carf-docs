---
modules: [GEOAPI, GEOWEB]
epic: scalability
---

# US-037: Aprovar em Lote

Como gestor, quero aprovar múltiplas unidades de uma vez para que processo seja rápido, onde o sistema permite execução de aprovações em massa reduzindo tempo necessário para processar grandes volumes de unidades que atendem critérios de qualidade, garantindo eficiência operacional sem comprometer rastreabilidade individual de cada aprovação. O cenário principal de uso ocorre quando gestor tem conjunto de unidades validadas e prontas para aprovação, permitindo selecioná-las através de checkboxes na listagem e executar ação de aprovação em lote que processa todas as unidades selecionadas em única operação. Os critérios de aceitação incluem funcionalidade de seleção múltipla através de checkboxes ao lado de cada unidade na listagem permitindo marcar individualmente ou selecionar todas visíveis, botão "Aprovar selecionadas" que fica habilitado apenas quando há unidades marcadas e executa aprovação em massa, processamento assíncrono quando operação envolve mais de 50 units onde job é enviado para fila de processamento em background evitando timeout de requisição, e notificação de conclusão enviada ao gestor quando processamento assíncrono termina informando quantidade de unidades aprovadas com sucesso e eventuais falhas. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/units/bulk-approve recebendo array de IDs e processando com workers assíncronos se necessário) e GEOWEB (controles de seleção múltipla na listagem e feedback de progresso durante processamento), garantindo rastreabilidade com UC-002 (Caso de Uso de Workflow de Aprovação), onde cada unidade aprovada em lote recebe entrada individual no audit log registrando aprovação, operação é transacional garantindo consistência, e relatório final detalha sucessos e falhas permitindo ação corretiva em casos problemáticos.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
