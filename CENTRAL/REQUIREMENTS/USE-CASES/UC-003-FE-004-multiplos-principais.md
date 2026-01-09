---
modules: [GEOWEB]
epic: maintainability
---

# UC-003-FE-004: Múltiplos Titulares Principais

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo na validação quando usuário marca checkbox is_primary=true mas já existe outro titular marcado como principal na mesma unidade violando regra de negócio RN-003 que permite apenas um principal por unidade, onde validação executa query `SELECT h.name, uh.id FROM unit_holders uh JOIN holders h ON h.id = uh.holder_id WHERE uh.unit_id = $1 AND uh.is_primary = true AND uh.deleted_at IS NULL` retornando dados do titular principal atual se existir. Sistema ao detectar conflito exibe modal de confirmação com título "Titular Principal Já Existe" apresentando nome do atual principal e perguntando "Desmarcar Nome do Titular Atual como principal e marcar Nome do Novo?" explicando implicação que apenas um pode ser principal para fins de documentação oficial certidões e relatórios, e oferece ações: Confirmar e Desmarcar Atual executando transação que atualiza titular existente setando is_primary=false e cria novo vínculo com is_primary=true garantindo atomicidade, Manter Atual e Não Marcar Novo criando vínculo normalmente mas com is_primary=false mantendo principal inalterado, ou Cancelar abortando operação completa retornando para formulário permitindo revisar decisão. Após confirmação sistema registra na timeline ambas mudanças "Titular X desmarcado como principal" e "Titular Y marcado como principal" para auditoria completa.

**Ponto de Desvio:** Validação quando checkbox is_primary=true e já existe outro principal

**Detecção de Conflito:**
```sql
SELECT
  h.id AS holder_id,
  h.name AS holder_name,
  uh.id AS link_id
FROM unit_holders uh
JOIN holders h ON h.id = uh.holder_id
WHERE uh.unit_id = $1
  AND uh.is_primary = true
  AND uh.deleted_at IS NULL;
```

**Modal de Confirmação:**
```
⚠️ Titular Principal Já Existe

João Silva Santos já está marcado como titular principal desta unidade.

Deseja desmarcar João Silva e marcar Maria Souza Lima como principal?

⚠️ Apenas um titular pode ser principal por unidade.

[Confirmar e Desmarcar Atual] [Manter Atual] [Cancelar]
```

**Transação Atômica:**
```typescript
await db.transaction(async (trx) => {
  // Desmarcar atual principal
  await trx('unit_holders')
    .where({ unit_id: unitId, is_primary: true })
    .update({ is_primary: false, updated_at: new Date() });

  // Criar novo vínculo como principal
  await trx('unit_holders').insert({
    unit_id: unitId,
    holder_id: newHolderId,
    relationship_type: formData.relationship_type,
    ownership_percentage: formData.ownership_percentage,
    is_primary: true
  });

  // Timeline
  await trx('unit_timeline').insert([
    { unit_id: unitId, event: 'PRIMARY_UNMARKED', holder_id: currentPrimaryId },
    { unit_id: unitId, event: 'PRIMARY_MARKED', holder_id: newHolderId }
  ]);
});
```

**Retorno:** Titular vinculado com ajuste de principal, ou operação cancelada

---

**Última atualização:** 2025-12-30
