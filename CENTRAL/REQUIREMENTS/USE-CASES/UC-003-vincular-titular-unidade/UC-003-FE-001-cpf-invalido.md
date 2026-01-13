---
modules: [GEOWEB, REURBCAD]
epic: holders
---

# UC-003-FE-001: CPF/CNPJ Inválido

Fluxo de exceção do UC-003 Vincular Titular a Unidade ocorrendo no passo de criação de novo titular quando usuário informa CPF ou CNPJ com dígitos verificadores incorretos sequência repetida ou formato inválido, onde validação executa em tempo real durante digitação após preencher 11 dígitos para CPF ou 14 para CNPJ disparando função de validação que remove formatação (pontos hífens barras), verifica comprimento exato, detecta sequências repetidas inválidas (00000000000 11111111111 até 99999999999 para CPF, 00000000000000 até 99999999999999 para CNPJ), calcula dígitos verificadores usando algoritmo oficial da Receita Federal comparando com dígitos informados, e retorna boolean válido/inválido com mensagem de erro específica. Sistema ao detectar inválido exibe ícone vermelho de alerta ao lado do campo input com tooltip explicativo "CPF inválido: dígitos verificadores incorretos" ou "CPF inválido: sequência repetida não permitida", adiciona borda vermelha no campo destacando visualmente erro, e desabilita botão Criar Titular ou Vincular impedindo prosseguimento até correção. Usuário lê mensagem de erro compreendendo problema, corrige dígitos digitando CPF/CNPJ válido diferente ou consultando documento original se estava transcrevendo, e ao digitar corretamente sistema re-valida em tempo real removendo ícone vermelho substituindo por verde checkmark, remove borda vermelha retornando para estado normal, e habilita botão permitindo prosseguir com criação do titular e vínculo.

**Ponto de Desvio:** Criação de novo titular ao preencher CPF/CNPJ

**Algoritmo de Validação CPF:**

Função validateCpf recebe string cpf retornando objeto com valid boolean e error opcional string, primeiro remove não-dígitos usando replace com regex /\D/g armazenando em digits, verifica se comprimento exato onze retornando valid false error CPF deve ter 11 dígitos se diferente, verifica sequência repetida usando regex /^(\d)\1{10}$/ retornando valid false error Sequência repetida inválida se match, calcula primeiro dígito verificador iterando primeiros nove dígitos somando cada dígito multiplicado por dez menos índice armazenando em sum, calculando check1 como onze menos resto divisão sum por onze ajustando para zero se maior igual dez, calcula segundo dígito verificador iterando primeiros dez dígitos multiplicando por onze menos índice calculando check2 similar check1, compara check1 com nono dígito e check2 com décimo dígito retornando valid false error Dígitos verificadores incorretos se diferentes, finalmente retorna valid true se todas validações passaram confirmando CPF válido conforme algoritmo oficial Receita Federal.

**Retorno:** Usuário corrige CPF/CNPJ e volta ao fluxo de criação de titular

---

**Última atualização:** 2025-12-30
