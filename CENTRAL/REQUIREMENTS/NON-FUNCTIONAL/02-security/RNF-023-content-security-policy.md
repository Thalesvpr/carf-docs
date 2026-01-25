---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-023: Content Security Policy

## Descricao

GEOWEB deve implementar CSP via headers HTTP para prevenir XSS, clickjacking e injecao de codigo. Camada adicional de defesa alem da sanitizacao de inputs.

## Metricas

- Header: Content-Security-Policy configurado
- Scripts: apenas do proprio dominio e CDNs autorizados
- Frames: frame-ancestors restritivo contra clickjacking

## Criterios de Aceitacao

1. Scripts inline bloqueados (sem unsafe-inline) ou via nonces
2. connect-src restrito a GEOAPI e servicos de mapas
3. frame-ancestors configurado como 'none' ou lista especifica
