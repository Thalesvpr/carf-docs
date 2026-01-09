---
modules: [GEOWEB]
epic: holders
---

# UC-003-FE-002: Titular Já Vinculado

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo no passo de validação antes de criar vínculo quando sistema detecta que titular selecionado ou criado já possui vínculo ativo com mesma unidade, onde validação executa query `SELECT id FROM unit_holders WHERE unit_id = $1 AND holder_id = $2 AND deleted_at IS NULL` retornando registro existente se houver duplicação. Sistema ao detectar duplicação retorna HTTP 409 Conflict com body JSON contendo erro e dados do vínculo existente incluindo relationship_type ownership_percentage is_primary created_at, frontend intercepta erro exibindo toast vermelho com mensagem "Titular Nome já está vinculado a esta unidade como Proprietário (50%)" mostrando tipo e percentual atuais para contexto, e oferece duas ações: Editar Vínculo Existente abrindo modal pré-preenchido com dados atuais permitindo alterar tipo percentual ou flag principal atualizando registro existente ao invés de criar duplicado, ou Cancelar fechando modal e retornando para lista de titulares sem alterações.

**Ponto de Desvio:** Validação antes de criar vínculo (após preencher tipo e percentual)

**Detecção de Duplicação:**
```sql
SELECT
  uh.id,
  h.name,
  uh.relationship_type,
  uh.ownership_percentage,
  uh.is_primary,
  uh.created_at
FROM unit_holders uh
JOIN holders h ON h.id = uh.holder_id
WHERE uh.unit_id = $1
  AND uh.holder_id = $2
  AND uh.deleted_at IS NULL;
```

**Modal de Erro:**
```
⚠️ Titular Já Vinculado

João Silva Santos (CPF 123.456.789-00) já está vinculado a esta unidade:
- Tipo: Proprietário
- Percentual: 50%
- Principal: Sim
- Vinculado em: 15/12/2025

[Editar Vínculo Existente] [Cancelar]
```

**Retorno:** Se Editar, abre modal de edição; se Cancelar, volta para lista de titulares

---

**Última atualização:** 2025-12-30
