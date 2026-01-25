---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-086: OpenAPI Spec

## Descricao

Documentacao via OpenAPI 3.x em arquivo openapi-geoapi.yaml. Swagger UI para exploracao interativa. Geracao de SDKs em TypeScript, Python, Java, C#. Testes de contrato validam conformidade.

## Metricas

- Spec: OpenAPI 3.x valido
- Swagger UI: acessivel em endpoint publico
- SDKs: geracao via OpenAPI Generator

## Criterios de Aceitacao

1. Todos endpoints documentados com schemas completos
2. Testes de contrato verificam conformidade antes de deploy
3. Desenvolvedores podem testar API diretamente no navegador
