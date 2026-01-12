# Cpf

Value object imutável herdando de BaseValueObject representando CPF (Cadastro de Pessoa Física) brasileiro com validação completa de formato e dígitos verificadores, garantindo que apenas CPFs válidos existam no domínio. Validações incluem verificação de exatamente 11 dígitos numéricos, rejeição de sequências repetidas (000.000.000-00, 111.111.111-11, etc), e cálculo correto dos dois dígitos verificadores através do algoritmo oficial da Receita Federal.

Métodos principais incluem construtor que recebe string com ou sem formatação (aceita "12345678900" ou "123.456.789-00") validando e armazenando apenas números, ToString() retornando formato legível "123.456.789-00", ToUnformatted() retornando apenas dígitos "12345678900" para persistência, e operadores de igualdade (== e !=) comparando por valor dos dígitos.

Usado em Holder como identificador único dentro do tenant (um titular = um CPF), em consultas de validação externa via APIs da Receita Federal, e em relatórios e certidões onde CPF formatado é obrigatório, garantindo que nenhum titular com CPF inválido seja persistido no sistema.

---

**Última atualização:** 2026-01-12
