---
type: leaf
status: review
updated: 2026-02-08
---

# ApiKeyValue

Value object imutavel herdando de BaseValueObject que representa uma chave de API para autenticacao de sistemas externos e scripts automatizados. Segue formato especifico com prefixo identificavel e hash criptografico para armazenamento seguro. O valor original nunca e armazenado em banco de dados; apenas o hash SHA-256 e persistido.

O metodo estatico Generate() cria novas chaves aleatorias usando gerador criptografico seguro.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Formato | Prefixo geoapi_sk_ seguido de 32 caracteres alfanumericos aleatorios. |
| Geracao criptografica | Caracteres gerados via RNGCryptoServiceProvider. |
| Armazenamento seguro | Apenas hash SHA-256 e persistido, nunca o valor original. |

## Formato

| Aspecto | Especificacao |
| --- | --- |
| Valor completo | geoapi_sk_ seguido de 32 caracteres alfanumericos. |
| Prefixo | geoapi_sk_ para identificar tipo de chave. |
| Mascarado (ToMasked) | geoapi_sk_abc...xyz para exibicao em UI. |
| Hash armazenado | SHA-256 do valor completo para persistencia segura. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| Generate() | ApiKeyValue | Estatico, gera nova chave aleatoria segura. |
| ToHash() | string | Gera SHA-256 hash para persistencia. |
| Matches(string) | bool | Compara hash armazenado com hash de chave fornecida. |
| ToMasked() | string | Retorna versao parcialmente oculta para exibicao. |

Usado em ApiKey.Value armazenando apenas hash no banco de dados, em autenticacao de requests onde header X-API-Key e validado por comparacao de hashes, e em telas administrativas mostrando versao mascarada por seguranca.
