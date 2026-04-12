---
type: leaf
status: review
updated: 2026-02-08
---

# CPF (Cadastro de Pessoa Fisica)

Value object imutavel representando CPF brasileiro validado, garantindo que apenas numeros validos pelo algoritmo Mod11 da Receita Federal sao aceitos no sistema. Utilizado como identificador natural de Holder dentro de cada tenant, com constraint UNIQUE em (tenant_id, cpf) na tabela holders.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Tamanho | Exatamente 11 digitos apos remover formatacao. |
| Sequencia repetida | Rejeita CPFs com todos digitos iguais (00000000000 a 99999999999). |
| Digito verificador 1 | Decimo digito calculado com pesos 10 a 2 sobre primeiros 9 digitos, modulo 11. |
| Digito verificador 2 | Decimo primeiro digito calculado com pesos 11 a 2 sobre primeiros 10 digitos, modulo 11. |
| Validacao na criacao | Exception lancada se CPF invalido, impedindo criacao de instancia malformada. |

## Formato

| Operacao | Formato | Exemplo |
|----------|---------|---------|
| Armazenamento | 11 digitos sem formatacao | 12345678901 |
| Exibicao | ###.###.###-## | 123.456.789-01 |
| Mascarado (LGPD) | ###.***.**#-## | 123.***.***-01 |

## Regras de Negocio

CPF deve ser unico por Holder dentro do tenant. E campo sensivel LGPD exigindo criptografia em repouso, logs de acesso e consentimento para uso. Validacao ocorre tanto em frontend para feedback imediato quanto em backend para seguranca.
