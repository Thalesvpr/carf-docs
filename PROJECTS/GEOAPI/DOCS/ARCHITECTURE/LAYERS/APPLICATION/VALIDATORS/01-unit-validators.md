---
type: leaf
status: active
updated: 2026-02-07
---

# Unit Validators

Os validators da GEOAPI utilizam FluentValidation para validar requests de entrada e commands do MediatR. Cada validator herda de AbstractValidator e define regras declarativas.

## CreateUnitRequestValidator

Valida o request de criacao de unidade. O campo Address e obrigatorio e delegado ao AddressValidator. O campo Geometry e obrigatorio e delegado ao GeometryValidator. O campo Photos, quando presente, tem cada item validado pelo PhotoValidator.

## AddressValidator

Valida o DTO de endereco com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| Street | Obrigatorio, maximo 200 caracteres | Rua e obrigatoria |
| Number | Obrigatorio, maximo 20 caracteres | Numero e obrigatorio |
| Neighborhood | Obrigatorio, maximo 100 caracteres | Bairro e obrigatorio |
| City | Obrigatorio, maximo 100 caracteres | Cidade e obrigatoria |
| State | Obrigatorio, regex duas letras maiusculas | Estado deve ter 2 letras maiusculas |
| ZipCode | Obrigatorio, regex 5 digitos hifen 3 digitos | CEP invalido |

## GeometryValidator

Valida o DTO de geometria GeoJSON. O campo Type deve ser igual a "Polygon". O campo Coordinates e obrigatorio e deve satisfazer duas regras customizadas: BeValidPolygon verifica que o anel externo tem ao menos 4 pontos e que o primeiro ponto e igual ao ultimo (poligono fechado). NotBeSelfIntersecting cria o poligono via GeometryFactory e verifica que a propriedade IsValid e verdadeira.

## UpdateUnitRequestValidator

Valida o request de atualizacao de unidade. Ambos os campos Address e Geometry sao opcionais. Quando presentes, sao delegados aos respectivos validators (AddressValidator e GeometryValidator) via clausula condicional When.
