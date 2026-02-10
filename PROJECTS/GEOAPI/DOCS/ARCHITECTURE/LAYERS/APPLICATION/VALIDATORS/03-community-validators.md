---
type: leaf
status: review
updated: 2026-02-08
---

# Community Validators

Os validators de comunidades utilizam FluentValidation para validar requests de criacao e atualizacao de comunidades.

## CreateCommunityRequestValidator

Valida o request de criacao de comunidade com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| Code | Obrigatorio, maximo 50 caracteres, alfanumerico com hifen | Codigo invalido |
| Name | Obrigatorio, maximo 200 caracteres | Nome obrigatorio |
| CommunityType | Obrigatorio, enum URBANA, RURAL, QUILOMBOLA, RIBEIRINHA | Tipo de comunidade invalido |
| Municipality | Obrigatorio, maximo 100 caracteres | Municipio obrigatorio |
| State | Obrigatorio, regex duas letras maiusculas | Estado deve ter 2 letras maiusculas |
| District | Opcional, maximo 100 caracteres quando presente | Distrito invalido |
| Neighborhood | Opcional, maximo 100 caracteres quando presente | Bairro invalido |
| Boundary | Opcional, delegado ao GeometryValidator quando presente | Boundary invalido |

## UpdateCommunityRequestValidator

Valida o request de atualizacao parcial. Campos Name, District, Neighborhood e Reference sao opcionais e validados quanto a tamanho maximo quando presentes. O campo Boundary quando presente e delegado ao GeometryValidator. Campos Code e CommunityType nao sao aceitos no update pois sao imutaveis apos criacao.

## Validacao Espacial

A validacao do boundary no handler vai alem do FluentValidation. Apos conversao para geometria NetTopologySuite, o handler executa ST_IsValid via PostGIS para garantir que o poligono e topologicamente valido, fechado e sem auto-interseccao. Esta validacao de segundo nivel captura erros geometricos que nao sao detectaveis apenas pela estrutura do GeoJSON.
