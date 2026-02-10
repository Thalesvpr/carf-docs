---
type: leaf
status: review
updated: 2026-02-08
---

# Cpf

Value object imutavel herdando de BaseValueObject que representa o CPF (Cadastro de Pessoa Fisica) brasileiro com validacao completa de formato e digitos verificadores. Garante que apenas CPFs validos existam no dominio, sendo utilizado principalmente na entidade Holder como identificador unico de titular dentro de cada tenant. O campo correspondente no banco e holders.cpf (varchar(11)), armazenado sem formatacao.

O construtor aceita string com ou sem formatacao (tanto 12345678900 quanto 123.456.789-00) e normaliza internamente para apenas digitos. Caso a validacao falhe, uma ValidationException e lancada impedindo a criacao do objeto.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Exatamente 11 digitos | Apos remocao de caracteres nao numericos, deve conter exatamente 11 digitos. |
| Rejeicao de sequencias repetidas | Sequencias como 000.000.000-00 ou 111.111.111-11 sao rejeitadas. |
| Primeiro digito verificador | Calculado via algoritmo Mod11 com pesos de 10 a 2 sobre os 9 primeiros digitos. |
| Segundo digito verificador | Calculado via algoritmo Mod11 com pesos de 11 a 2 sobre os 10 primeiros digitos. |

## Formato

| Aspecto | Especificacao |
| --- | --- |
| Armazenamento | Apenas digitos: 12345678900 (varchar(11) no banco). |
| Exibicao (ToString) | Formato legivel: 123.456.789-00. |
| ToUnformatted() | Retorna apenas digitos para persistencia e comparacao. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| ToString() | string | Retorna CPF formatado 123.456.789-00. |
| ToUnformatted() | string | Retorna apenas digitos 12345678900 para persistencia. |
| Equals / == / \!= | bool | Compara por valor dos digitos. |

Usado em Holder como identificador natural (UNIQUE em tenant_id, cpf), em consultas de validacao, em relatorios e certidoes de legitimacao onde CPF formatado e obrigatorio, e na tabela unit_holders para vincular titulares a unidades.
