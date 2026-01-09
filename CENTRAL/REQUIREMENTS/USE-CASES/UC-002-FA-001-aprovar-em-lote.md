---
modules: [GEOWEB, REURBCAD]
epic: performance
---

# UC-002-FA-001: Aprovar em Lote

Fluxo alternativo do UC-002 Aprovar Unidade Habitacional desviando no passo 3 (seleção de unidade individual) quando MANAGER deseja aprovar múltiplas unidades simultaneamente economizando tempo em cenário de volume alto de unidades pendentes simples sem complexidades que exijam revisão detalhada individual, onde ao invés de selecionar unidade única para revisar MANAGER marca checkbox ao lado de múltiplas linhas na lista de pendentes (máximo 50 unidades por lote para evitar timeout de transação), sistema exibe contador dinâmico "X unidades selecionadas" no topo da lista e habilita botão Aprovar Selecionadas que estava disabled quando nenhuma seleção, MANAGER opcionalmente aplica filtros adicionais antes de selecionar como mesmo criador mesma comunidade mesmo período de criação permitindo seleção inteligente de unidades similares, clica em Aprovar Selecionadas disparando modal de confirmação com mensagem "Você está prestes a aprovar X unidades. Esta ação não pode ser desfeita. Deseja continuar?" mostrando lista resumida de códigos das unidades selecionadas com scroll se muitas e campo textarea opcional para comentário único aplicado a todas unidades do lote. MANAGER revisa lista rapidamente confirmando que selecionou unidades corretas sem incluir acidentalmente unidade problemática, adiciona comentário opcional genérico como "Aprovação em lote - unidades conformes com padrão municipal" se desejar documentar critério usado, confirma clicando Aprovar Todas no modal e sistema executa processamento em batch iniciando transação de banco de dados ou loop com mini-transações individuais dependendo de configuração de resilience (preferência por mini-transações para evitar rollback completo se uma falhar), para cada unidade selecionada tenta executar mesma lógica de aprovação individual (atualizar status registrar timestamp approved_by adicionar comentário disparar evento criar auditoria), coleta resultados de sucesso e falha em arrays separados tratando erros individuais como concurrent modification (outra pessoa aprovou entre seleção e execução) validação falhou (dados mudaram e não passam mais em validações) ou constraint violation (regra de negócio customizada específica do tenant), e após processar todas exibe modal de resumo com estatísticas "X de Y unidades aprovadas com sucesso" listando sucessos com ícone verde checkmark e falhas com ícone vermelho X e mensagem de erro específica permitindo MANAGER tentar novamente as falhadas individualmente se desejar investigar problema. Sistema atualiza lista de pendentes removendo unidades aprovadas com sucesso e mantendo falhadas visíveis, envia notificações em lote agrupando por criador (se mesmo usuário criou múltiplas unidades recebe um email consolidado "N unidades suas foram aprovadas" ao invés de N emails separados), e registra auditoria em batch insert otimizado para performance.

**Ponto de Desvio:** Passo 3 do UC-002 (seleção de unidade para revisar)

**Limites:**
- Máximo 50 unidades por lote (configurável via tenant settings)
- Timeout de processamento: 60 segundos (exibe warning se ultrapassar)
- Notificações agrupadas por criador (max 100 unidades por email)

**Processamento em Batch:**
```typescript
const results = {
  success: [],
  failed: []
};

for (const unitId of selectedUnits) {
  try {
    await approveUnit(unitId, managerId, comment);
    results.success.push(unitId);
  } catch (error) {
    results.failed.push({ unitId, error: error.message });
  }
}

return {
  total: selectedUnits.length,
  approved: results.success.length,
  failed: results.failed.length,
  details: results.failed
};
```

**Modal de Resumo:**
```
✅ 47 de 50 unidades aprovadas com sucesso

❌ Falhas (3):
- UH-123: Unidade já foi aprovada por João Silva
- UH-456: Dados de validação falharam (geometria inválida)
- UH-789: Titular principal não vinculado
```

**Retorno:** Atualiza lista removendo sucessos, mantém falhas para retry individual

---

**Última atualização:** 2025-12-30
