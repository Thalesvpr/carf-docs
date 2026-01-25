---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-021: Rate Limiting

## Descricao

Limitacao de taxa de requisicoes previne abuso, DoS e forca bruta. Politicas diferenciadas por tipo de endpoint. Middleware baseado em Redis para ambiente multi-instancia.

## Metricas

- Endpoints gerais: 100 req/min por IP
- Autenticacao: 10 req/min por IP
- Upload: 20 req/min por usuario
- Exportacao: 5 req/min por usuario

## Criterios de Aceitacao

1. HTTP 429 com headers X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After
2. Contadores distribuidos em Redis para multiplas instancias
3. Limites configuraveis via variaveis de ambiente
