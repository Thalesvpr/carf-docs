---
type: leaf
status: review
updated: 2026-02-08
---

# Email

Value object imutavel representando endereco de email validado. Utilizado na entidade Holder (coluna email varchar(200), nullable) como meio de contato opcional do titular.

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| Formato | Deve seguir padrao RFC 5322 (usuario@dominio). |
| Tamanho | Maximo 200 caracteres conforme coluna do banco. |
| Normalizacao | Convertido para minusculas antes de armazenar. |
| Dominio valido | Dominio deve conter ao menos um ponto. |

## Formato

Armazenado sempre em minusculas sem espacos. Igualdade por valor: dois Emails com mesmo texto normalizado sao considerados iguais independente da instancia.
