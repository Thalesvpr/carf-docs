---
title: "Decisoes Arquiteturais - @carf/geoapi-client"
description: "Registro de decisoes arquiteturais para o cliente HTTP"
status: review
updated: 2026-01-21
source: "interno"
---

# Decisoes Arquiteturais - @carf/geoapi-client

Registro de ADRs que fundamentam o cliente HTTP. Decisoes incluem Axios como cliente base (rejeitando Fetch nativo, ky e got), retry com exponential backoff via axios-retry, circuit breaker para prevenir cascading failures, erros tipados em hierarquia (ApiError, ValidationError, UnauthorizedError, etc.), dependencia direta de @carf/tscore para types/auth, e organizacao de endpoints em classes por dominio (api.units, api.holders, etc.).

<!-- GENERATED:START - Nao edite abaixo desta linha -->
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
