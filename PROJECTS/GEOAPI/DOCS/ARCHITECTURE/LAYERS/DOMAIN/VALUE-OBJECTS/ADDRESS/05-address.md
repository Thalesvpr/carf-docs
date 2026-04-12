---
type: leaf
status: review
updated: 2026-02-08
---

# Address

Value object imutavel herdando de BaseValueObject que representa endereco completo brasileiro com todos os componentes necessarios para localizacao fisica e geracao de documentos oficiais de regularizacao fundiaria. No banco de dados, o endereco e desnormalizado na tabela units em colunas separadas: address_street (varchar(200)), address_number (varchar(20)), address_complement (varchar(100)), address_neighborhood (varchar(100)), address_city (varchar(100)), address_state (varchar(2)) e address_zip_code (varchar(9)).

A desnormalizacao facilita buscas textuais sem joins, permitindo filtros rapidos por logradouro, bairro ou cidade diretamente na tabela de unidades.

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Logradouro obrigatorio | Tipo e nome da rua nao podem ser vazios. |
| Numero obrigatorio | String permitindo S/N para enderecos sem numero. |
| Bairro obrigatorio | Nao pode ser vazio. |
| Cidade obrigatoria | Nao pode ser vazio. |
| CEP formato | Quando informado, deve ter exatamente 8 digitos (armazenado sem formatacao). |
| Estado formato | Sigla UF de 2 letras maiusculas quando informado. |

## Campos

| Campo | Tipo | Obrigatorio | Descricao |
| --- | --- | --- | --- |
| Street | string | sim | Logradouro (tipo + nome). |
| Number | string | sim | Numero ou S/N. |
| Complement | string | nao | Apartamento, bloco, sala. |
| Neighborhood | string | sim | Bairro. |
| City | string | sim | Cidade. |
| State | string | nao | Sigla UF (2 letras). |
| ZipCode | string | nao | CEP sem formatacao (8 digitos). |

## Formato

| Aspecto | Especificacao |
| --- | --- |
| ToString() | Rua das Flores, 123 - Apto 4 - Centro, Rio de Janeiro/RJ, 20000-000. |
| ToShortString() | Rua das Flores, 123 - Centro. |

Usado em Unit para endereco oficial da propriedade, coexistindo com geometria GeoPolygon (endereco textual + perimetro espacial), e aparece em certidoes e memoriais descritivos de legitimacao fundiaria.
