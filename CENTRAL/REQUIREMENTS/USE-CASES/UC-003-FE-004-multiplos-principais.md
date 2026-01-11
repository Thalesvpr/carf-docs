---
modules: [GEOWEB]
epic: maintainability
---

# UC-003-FE-004: Múltiplos Titulares Principais

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo na validação quando usuário marca checkbox is_primary=true mas já existe outro titular marcado como principal na mesma unidade violando regra de negócio RN-003 que permite apenas um principal por unidade, onde validação executa query `SELECT h.name, uh.id FROM unit_holders uh JOIN holders h ON h.id = uh.holder_id WHERE uh.unit_id = $1 AND uh.is_primary = true AND uh.deleted_at IS NULL` retornando dados do titular principal atual se existir. Sistema ao detectar conflito exibe modal de confirmação com título "Titular Principal Já Existe" apresentando nome do atual principal e perguntando "Desmarcar Nome do Titular Atual como principal e marcar Nome do Novo?" explicando implicação que apenas um pode ser principal para fins de documentação oficial certidões e relatórios, e oferece ações: Confirmar e Desmarcar Atual executando transação que atualiza titular existente setando is_primary=false e cria novo vínculo com is_primary=true garantindo atomicidade, Manter Atual e Não Marcar Novo criando vínculo normalmente mas com is_primary=false mantendo principal inalterado, ou Cancelar abortando operação completa retornando para formulário permitindo revisar decisão. Após confirmação sistema registra na timeline ambas mudanças "Titular X desmarcado como principal" e "Titular Y marcado como principal" para auditoria completa.

**Ponto de Desvio:** Validação quando checkbox is_primary=true e já existe outro principal

**Detecção de Conflito:**

Query SQL executa SELECT com colunas h.id AS holder_id h.name AS holder_name uh.id AS link_id fazendo FROM unit_holders uh JOIN holders h ON h.id igual uh.holder_id WHERE uh.unit_id igual parâmetro um AND uh.is_primary igual true AND uh.deleted_at IS NULL retornando dados do titular principal atual se existir com ID do titular nome completo e ID do registro de vínculo para posterior atualização em transação atômica.

**Modal de Confirmação:**

Modal exibe ícone warning laranja com título "Titular Principal Já Existe" seguido por parágrafo interpolado "Nome do Titular Atual já está marcado como titular principal desta unidade." com pergunta "Deseja desmarcar Nome do Atual e marcar Nome do Novo como principal?" explicando regra de negócio em destaque "Apenas um titular pode ser principal por unidade" com ícone warning, finalizando com três botões de ação sendo Confirmar e Desmarcar Atual executando transação atômica descrita abaixo, Manter Atual criando novo vínculo com is_primary false sem alterar existente, e Cancelar abortando operação completa.

**Transação Atômica:**

Backend executa await db.transaction recebendo callback async com parâmetro trx executando três operações sequenciais sendo primeiro await trx com tabela unit_holders aplicando where com unit_id igual unitId e is_primary igual true executando update com is_primary igual false e updated_at igual new Date() desmarcando titular atual, segundo await trx com tabela unit_holders executando insert com objeto contendo unit_id igual unitId holder_id igual newHolderId relationship_type igual formData.relationship_type ownership_percentage igual formData.ownership_percentage e is_primary igual true criando novo vínculo como principal, terceiro await trx com tabela unit_timeline executando insert com array contendo dois objetos sendo primeiro com unit_id igual unitId event igual PRIMARY_UNMARKED e holder_id igual currentPrimaryId registrando desmarcação e segundo com event igual PRIMARY_MARKED e holder_id igual newHolderId registrando nova marcação garantindo atomicidade completa com rollback automático se qualquer operação falhar.

**Retorno:** Titular vinculado com ajuste de principal, ou operação cancelada

---

**Última atualização:** 2025-12-30
