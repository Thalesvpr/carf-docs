---
type: leaf
status: review
updated: 2026-02-08
---

# Email

Value object imutavel herdando de BaseValueObject que representa um endereco de email valido com validacao de formato RFC 5322 simplificado. Garante que apenas emails bem-formados sejam armazenados no sistema. No banco de dados, corresponde ao campo holders.email (varchar(200), nullable).

O construtor recebe uma string, valida o formato e normaliza para lowercase para comparacoes case-insensitive. Se o formato for invalido, uma ValidationException e lancada.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Formato basico | Deve seguir padrao local@dominio com exatamente um simbolo @. |
| Local-part | Aceita caracteres alfanumericos, pontos, hifens e underscores. |
| Dominio | Deve conter pelo menos um ponto separando subdominio de TLD. |
| TLD minimo | Top-level domain deve ter minimo de 2 caracteres. |
| Normalizacao | Armazenado em lowercase para comparacoes case-insensitive. |

## Formato

| Aspecto | Especificacao |
| --- | --- |
| Armazenamento | Lowercase normalizado (varchar(200)). |
| ToString() | Retorna valor normalizado em lowercase. |
| Domain() | Extrai parte apos @ para validacoes de dominio corporativo. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| ToString() | string | Retorna email normalizado. |
| Domain() | string | Extrai dominio apos @. |
| Equals / == | bool | Compara valores normalizados. |

Usado em Holder para contato opcional do titular, em Account para email vinculado ao Keycloak garantindo unicidade de login, em envio de notificacoes de aprovacao e rejeicao de processos de legitimacao, e em validacao de dominios permitidos por Tenant.
