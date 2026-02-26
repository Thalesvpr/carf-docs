---
type: readme
title: "Documentacao @carf/geoapi-client"
description: "Cliente HTTP auto-gerado via orval a partir do swagger.json da GEOAPI"
status: active
updated: 2026-02-09
source: "interno"
---

# Documentacao @carf/geoapi-client

Cliente HTTP auto-gerado via orval a partir do swagger.json da GEOAPI. Gera tipos TypeScript e hooks React Query automaticamente, evoluindo junto com a API.

## Secoes

| Secao | Descricao |
|:------|:----------|
| [SPECS/](./SPECS/README.md) | Especificacoes tecnicas (package.json, client config) |
| [ADRs/](./ADRs/README.md) | Decisoes arquiteturais |
| [ARCHITECTURE/](./ARCHITECTURE/README.md) | Arquitetura do cliente |
| [CONCEPTS/](./CONCEPTS/README.md) | Custom axios instance, mutator pattern |
| [API/](./API/README.md) | Referencia de APIs (design reference) |
| [HOW-TO/](./HOW-TO/README.md) | Guias praticos |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Guia de contribuicao |

## Geracao

O client e auto-gerado a partir do swagger.json da GEOAPI:

```bash
# Baixar swagger atualizado (API rodando em localhost:5127)
bun run swagger:fetch

# Gerar tipos e hooks
bun run generate
```

## Uso Rapido

```typescript
import { createApiClient } from '@carf/geoapi-client';

const api = createApiClient({
  baseURL: 'http://localhost:5127',
  getToken: async () => keycloakClient.getAccessToken(),
  getTenantId: () => currentUser.tenantId,
});
```

Hooks React Query (REURBWEB):

```typescript
import { useGetApiUnits } from '@carf/geoapi-client';

const { data } = useGetApiUnits({ communityId, page: 1, pageSize: 20 });
```

Funcoes vanilla (qualquer app):

```typescript
import { getApiUnits } from '@carf/geoapi-client';

const units = await getApiUnits({ communityId });
```

## Status de Especificacao

| Secao | Arquivos | Status |
|:------|:---------|:-------|
| SPECS | 2 | Atualizado |
| ADRs | 1 | Aceito |
| ARCHITECTURE | 3 | Atualizado |
| CONCEPTS | 1 | Atualizado |
| API | 22 | Referencia de design |
| HOW-TO | 3 | Atualizado |

<!-- CARF-INDEX-START -->
> **Indice gerado automaticamente.** Nao edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (6)

| Pasta | Descrição |
|-------|-----------|
| [ADRs](./ADRs/README.md) | ... |
| [API](./API/README.md) | ... |
| [ARCHITECTURE](./ARCHITECTURE/README.md) | ... |
| [CONCEPTS](./CONCEPTS/README.md) | ... |
| [HOW-TO](./HOW-TO/README.md) | ... |
| [SPECS](./SPECS/README.md) | ... |

## Documentos (1)

| Documento | Status |
|-----------|--------|
| [Contributing to @carf/geoapi-client](./CONTRIBUTING.md) | review |

<!-- CARF-INDEX-END -->
