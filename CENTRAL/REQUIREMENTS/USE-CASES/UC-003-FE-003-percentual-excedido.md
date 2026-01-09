---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# UC-003-FE-003: Soma de Percentuais > 100%

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo na validação quando soma de ownership_percentage de todos titulares da unidade incluindo novo vínculo ultrapassa 100%, onde validação calcula `SELECT SUM(ownership_percentage) FROM unit_holders WHERE unit_id = $1 AND deleted_at IS NULL` adicionando percentual informado no formulário verificando se total > 100. Sistema ao detectar excedente retorna HTTP 400 Bad Request com body contendo soma atual (ex: 85%), percentual tentando adicionar (ex: 30%), total resultante (115%), e sugestão de percentual máximo permitido (15% = 100% - 85%), frontend exibe modal de warning com título "Percentuais Ultrapassam 100%" apresentando cálculo visual "85% (titulares atuais) + 30% (novo) = 115% > 100%" destacando excedente em vermelho, lista titulares atuais com percentuais mostrando quem já possui quanto facilitando decisão de ajuste, e oferece ações: Ajustar Automaticamente calculando percentual máximo permitido (100% - soma_atual) preenchendo automaticamente campo com valor seguro, Editar Manualmente mantendo modal aberto com campo percentual focado permitindo usuário digitar valor correto entre 0-15%, ou Redistribuir Percentuais abrindo tela avançada mostrando todos titulares com sliders permitindo ajustar proporcionalmente mantendo soma = 100%.

**Ponto de Desvio:** Validação antes de criar vínculo (soma ultrapassa 100%)

**Cálculo de Excedente:**
```typescript
const currentSum = await db('unit_holders')
  .where({ unit_id: unitId, deleted_at: null })
  .sum('ownership_percentage as total')
  .first();

const newPercentage = parseFloat(formData.ownership_percentage);
const totalAfter = (currentSum?.total || 0) + newPercentage;

if (totalAfter > 100) {
  const maxAllowed = 100 - (currentSum?.total || 0);
  throw new ValidationError({
    field: 'ownership_percentage',
    message: `Soma ultrapassa 100%. Máximo permitido: ${maxAllowed}%`,
    details: {
      current_sum: currentSum?.total || 0,
      attempting_to_add: newPercentage,
      total_after: totalAfter,
      max_allowed: maxAllowed
    }
  });
}
```

**Modal de Warning:**
```
⚠️ Percentuais Ultrapassam 100%

Titulares atuais: 85%
  • João Silva: 50% (Proprietário)
  • Maria Souza: 35% (Cônjuge)

Tentando adicionar: 30%
Total: 115% ❌

Máximo permitido: 15%

[Ajustar para 15%] [Editar Manualmente] [Redistribuir Todos] [Cancelar]
```

**Retorno:** Usuário ajusta percentual e tenta novamente, ou cancela operação

---

**Última atualização:** 2025-12-30
