---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# UC-003-FE-001: CPF/CNPJ Inválido

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo no passo de criação de novo titular quando usuário informa CPF ou CNPJ com dígitos verificadores incorretos sequência repetida ou formato inválido, onde validação executa em tempo real durante digitação após preencher 11 dígitos para CPF ou 14 para CNPJ disparando função de validação que remove formatação (pontos hífens barras), verifica comprimento exato, detecta sequências repetidas inválidas (00000000000 11111111111 até 99999999999 para CPF, 00000000000000 até 99999999999999 para CNPJ), calcula dígitos verificadores usando algoritmo oficial da Receita Federal comparando com dígitos informados, e retorna boolean válido/inválido com mensagem de erro específica. Sistema ao detectar inválido exibe ícone vermelho de alerta ao lado do campo input com tooltip explicativo "CPF inválido: dígitos verificadores incorretos" ou "CPF inválido: sequência repetida não permitida", adiciona borda vermelha no campo destacando visualmente erro, e desabilita botão Criar Titular ou Vincular impedindo prosseguimento até correção. Usuário lê mensagem de erro compreendendo problema, corrige dígitos digitando CPF/CNPJ válido diferente ou consultando documento original se estava transcrevendo, e ao digitar corretamente sistema re-valida em tempo real removendo ícone vermelho substituindo por verde checkmark, remove borda vermelha retornando para estado normal, e habilita botão permitindo prosseguir com criação do titular e vínculo.

**Ponto de Desvio:** Criação de novo titular ao preencher CPF/CNPJ

**Algoritmo de Validação CPF:**
```typescript
function validateCpf(cpf: string): { valid: boolean; error?: string } {
  const digits = cpf.replace(/\D/g, '');
  if (digits.length !== 11) return { valid: false, error: 'CPF deve ter 11 dígitos' };
  if (/^(\d)\1{10}$/.test(digits)) return { valid: false, error: 'Sequência repetida inválida' };

  let sum = 0;
  for (let i = 0; i < 9; i++) sum += parseInt(digits[i]) * (10 - i);
  let check1 = 11 - (sum % 11);
  if (check1 >= 10) check1 = 0;

  sum = 0;
  for (let i = 0; i < 10; i++) sum += parseInt(digits[i]) * (11 - i);
  let check2 = 11 - (sum % 11);
  if (check2 >= 10) check2 = 0;

  if (check1 !== parseInt(digits[9]) || check2 !== parseInt(digits[10])) {
    return { valid: false, error: 'Dígitos verificadores incorretos' };
  }

  return { valid: true };
}
```

**Retorno:** Usuário corrige CPF/CNPJ e volta ao fluxo de criação de titular

---

**Última atualização:** 2025-12-30
