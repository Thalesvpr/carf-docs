---
title: "Decisoes Arquiteturais - @carf/geoapi-client"
description: "Registro de decisoes arquiteturais para o cliente HTTP"
status: review
updated: 2026-01-20
source: "interno"
---

# Decisoes Arquiteturais - @carf/geoapi-client

Registro de decisoes arquiteturais que fundamentam o cliente HTTP.

## Decisoes Principais

### Axios como Cliente HTTP Base

**Decisao:** Usar Axios como cliente HTTP.

**Alternativas Consideradas:**
1. Fetch API nativa - Rejeitado por falta de interceptors nativos
2. ky - Rejeitado por menor adocao e ecossistema
3. got - Rejeitado por foco em Node.js (nao browser)

**Justificativa:**
- Interceptors robustos para auth e error handling
- Suporte a upload/download com progress
- Amplo ecossistema de plugins (axios-retry, etc.)
- Familiar para maioria dos desenvolvedores

### Retry com Exponential Backoff

**Decisao:** Implementar retry automatico com exponential backoff via axios-retry.

**Justificativa:**
- Resiliencia a falhas transientes (5xx, network errors)
- Rate limiting (429) respeitado automaticamente
- Nao sobrecarrega servidor em falhas

**Configuracao:**
- Maximo 3 tentativas por padrao
- Delay exponencial: 1s, 2s, 4s
- Retry apenas em erros idempontentes

### Circuit Breaker Pattern

**Decisao:** Implementar circuit breaker para prevenir cascading failures.

**Justificativa:**
- Fail fast quando servico esta indisponivel
- Permite recuperacao gradual (half-open state)
- Reduz carga em servidores com problemas

**Configuracao:**
- Abre apos 5 falhas consecutivas
- Permanece aberto por 30s
- Tenta half-open antes de fechar

### Erros Tipados

**Decisao:** Criar hierarquia de classes de erro tipadas.

**Justificativa:**
- TypeScript type guards funcionam (`error instanceof ValidationError`)
- Tratamento especifico por tipo de erro
- Informacoes estruturadas (status, code, details)

**Hierarquia:**
```
ApiError (base)
├── ValidationError (400)
├── UnauthorizedError (401)
├── ForbiddenError (403)
├── NotFoundError (404)
├── ConflictError (409)
└── ServerError (5xx)
```

### Integracao com @carf/tscore

**Decisao:** Dependencia direta de @carf/tscore para types e auth.

**Justificativa:**
- Types sincronizados com backend
- Autenticacao Keycloak reutilizada
- Evita duplicacao de codigo

**Consequencias:**
- Versoes devem ser sincronizadas
- Breaking changes em tscore afetam geoapi-client

### APIs como Submodulos

**Decisao:** Organizar endpoints em classes separadas por dominio.

```typescript
api.units.list()
api.holders.create(data)
api.communities.getStatistics(id)
```

**Justificativa:**
- Organizacao clara por dominio
- Autocomplete intuitivo no IDE
- Facilita manutencao e extensao

## Links Relacionados

- CENTRAL/LIBRARIES/02-geoapi-client.md - Documentacao CENTRAL
- ARCHITECTURE/01-client-architecture.md - Arquitetura do Cliente

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
