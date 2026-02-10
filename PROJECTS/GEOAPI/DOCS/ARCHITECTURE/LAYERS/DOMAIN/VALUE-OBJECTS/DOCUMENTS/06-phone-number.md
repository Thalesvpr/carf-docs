---
type: leaf
status: review
updated: 2026-02-08
---

# PhoneNumber

Value object imutavel herdando de BaseValueObject que representa numero de telefone brasileiro (fixo ou celular) com validacao de formato e DDD. Normaliza diferentes formatos de entrada para armazenamento padrao apenas com digitos. No banco de dados, corresponde ao campo holders.phone (varchar(20), nullable).

O construtor aceita formatos variados como (21)98765-4321 ou 21987654321 e normaliza para apenas digitos. Se a validacao falhar, uma ValidationException e lancada.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Comprimento fixo | 10 digitos para fixo (DDD + 8) ou 11 para celular (DDD + 9 + 8). |
| Celular comeca com 9 | Apos o DDD, celulares devem comecar com digito 9. |
| DDD valido | Codigo de area entre 11 e 99 conforme divisao territorial da Anatel. |
| Normalizacao | Caracteres nao numericos sao removidos antes da validacao. |

## Formato

| Aspecto | Especificacao |
| --- | --- |
| Armazenamento | Apenas digitos: 21987654321 (varchar(20)). |
| Exibicao celular | (21) 98765-4321. |
| Exibicao fixo | (21) 3456-7890. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| ToString() | string | Retorna formato legivel com parenteses e hifen. |
| ToUnformatted() | string | Retorna apenas digitos. |
| IsCellPhone() | bool | Verifica se e celular (11 digitos, terceiro digito 9). |
| DDD() | string | Extrai codigo de area (2 primeiros digitos). |

Usado em Holder para contato do titular, em Account para telefone do usuario, e em integracoes de notificacao via SMS para workflows de aprovacao de processos de legitimacao fundiaria.
