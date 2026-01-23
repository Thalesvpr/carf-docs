---
type: standard
status: current
updated: 2026-01-22
---

# STD-004: Design de API

## Regra

APIs REST usam substantivos plurais para recursos, verbos HTTP semanticos e status codes apropriados. Nomes de campos em camelCase. Paginacao via query params page e pageSize. Erros retornam objeto com code, message e details. Versionamento via header Accept-Version.

## Justificativa

Convencoes REST consistentes reduzem curva de aprendizado para consumidores da API e permitem tooling padronizado como geracao de clients.

## Aplicacao

Aplica-se a todos endpoints publicos da GEOAPI. Endpoints internos entre servicos podem usar gRPC. OpenAPI spec e gerada automaticamente e deve estar sempre atualizada.
