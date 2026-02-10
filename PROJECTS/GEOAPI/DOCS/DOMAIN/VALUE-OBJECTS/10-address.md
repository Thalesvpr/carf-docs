---
type: leaf
status: review
updated: 2026-02-08
---

# Address

Value object imutavel representando endereco brasileiro completo, desnormalizado em colunas separadas na tabela units para facilitar buscas textuais sem joins. Cada componente e uma coluna nullable independente.

## Componentes

| Componente | Coluna | Tipo | Descricao |
|------------|--------|------|-----------|
| Street | address_street | varchar(200) | Logradouro. |
| Number | address_number | varchar(20) | Numero. String para comportar S/N e complementos. |
| Complement | address_complement | varchar(100) | Complemento (apto, bloco, lote). |
| Neighborhood | address_neighborhood | varchar(100) | Bairro. |
| City | address_city | varchar(100) | Cidade. |
| State | address_state | varchar(2) | UF em maiusculas (SP, RJ, MG). |
| ZipCode | address_zip_code | varchar(9) | CEP sem formatacao (8 digitos). |

## Regras de Validacao

| Regra | Descricao |
|-------|-----------|
| State | Deve ser UF valida brasileira (2 letras maiusculas). |
| ZipCode | 8 digitos numericos quando preenchido. |
| Todos nullable | Todos os campos sao opcionais. Ocupacoes informais podem nao ter endereco formal. |

Address e desnormalizado ao inves de tabela separada para evitar joins em listagens de unidades e permitir busca textual direta.
