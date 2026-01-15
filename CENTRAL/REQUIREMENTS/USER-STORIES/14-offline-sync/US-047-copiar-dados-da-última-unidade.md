---
modules: [GEOWEB, REURBCAD]
epic: reliability
---

# US-047: Copiar Dados da Última Unidade

Como agente de campo, quero copiar dados da última unidade cadastrada para que o preenchimento de formulários seja rápido ao cadastrar múltiplas unidades em sequência na mesma área, onde a funcionalidade deve fornecer um botão "Copiar última" que replique automaticamente campos comuns como community_id e block_id da unidade anterior, garantindo que o código da unidade seja auto-incrementado inteligentemente para manter sequência lógica, permitindo que o agente acelere significativamente o processo de cadastro em situações onde múltiplas unidades compartilham atributos comuns. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com lógica de cópia seletiva de campos, integrada ao UC-004 (Cadastrar Unidade no Campo) para otimização do fluxo de cadastro. Os critérios de aceitação incluem disponibilidade de botão "Copiar última unidade" visível na tela de criação de nova unidade, cópia automática de campos contextuais (community_id block_id type_id land_use) da unidade mais recentemente cadastrada pelo agente, auto-incremento inteligente do campo code mantendo padrão de numeração (exemplo: se última foi "A-001" nova será "A-002"), limpeza automática de campos específicos da unidade anterior que não devem ser copiados (geometry photos titular_id observações), feedback visual indicando quais campos foram pré-preenchidos por cópia versus campos em branco, opção de desfazer cópia retornando formulário ao estado vazio, funcionalidade disponível apenas se houver pelo menos uma unidade já cadastrada localmente, e preservação de validações normais de campos mesmo para dados copiados. A rastreabilidade conecta esta user story ao UC-004 (Cadastrar Unidade no Campo), garantindo eficiência no processo de cadastro em massa de unidades com características similares.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
