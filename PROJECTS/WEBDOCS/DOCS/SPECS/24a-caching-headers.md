---
type: leaf
status: review
updated: 2026-02-07
---

# Caching Strategy - Headers e CDN

Cache do WEBDOCS com TTLs e headers por tipo de recurso. Relacionado com 24b-caching-application.md e 24c-caching-operations.md.

## Camadas

Browser (Cache-Control), CDN (Vercel Edge), Application (in-memory) e Service Worker (opcional). Estrategia: stale-while-revalidate para dinamicos, immutable para assets com hash.

## Por Tipo de Recurso

| Tipo | Pattern | Browser | CDN | Motivo |
|------|---------|---------|-----|--------|
| Assets | /_astro/* | 1 ano, immutable | 1 ano | Hash no nome, nunca muda |
| Estaticas | /guia/*, /manuais/* | 1 hora | 24 horas, stale-while-revalidate | Muda raramente |
| Dinamicas | /status/, /api/swagger/ | 0 | 1 minuto | Tempo real |
| Protegidas | /dev/* | private, no-store | - | Conteudo sensivel |

## API Endpoints

| Endpoint | Cache | Motivo |
|----------|-------|--------|
| /api/health | no-cache | Status real |
| /api/swagger | memory 300s | Spec muda raramente |
| /api/status | no-cache | Health checks frescos |

## vercel.json

Headers configurados por source pattern: /_astro/ com immutable 1 ano, /guia/ e /manuais/ com 1h browser e 24h CDN, /api/ com 1min CDN, /status com 30s CDN, /dev/ com private no-store.

## Referencia de Headers

| Header | Descricao |
|--------|-----------|
| public / private | CDN+browser vs apenas browser |
| max-age / s-maxage | TTL browser vs TTL CDN |
| stale-while-revalidate | CDN serve stale enquanto busca novo |
| immutable | Conteudo nunca muda |
| no-cache / no-store | Revalidar sempre / nunca armazenar |
