---
type: readme
status: active
updated: 2026-02-09
---

# How-To Guides - @carf/geoapi-client

Guias praticos para uso da biblioteca @carf/geoapi-client.

## Guias Disponiveis

| Guia | Descricao |
|:-----|:----------|
| 01-getting-started | Instalacao, geracao via orval e uso basico |
| 02-error-handling | Tratamento de erros da API |
| 03-file-upload | Upload de arquivos com progresso |

## Fluxo de Geracao

O client e auto-gerado via orval a partir do swagger.json da GEOAPI. Para regenerar:

1. `bun run swagger:fetch` — baixa swagger.json atualizado (API rodando em localhost:5127)
2. `bun run generate` — gera tipos e hooks em src/generated/

## Topicos Abordados

- Instalacao e configuracao com callbacks de auth
- Geracao automatica via orval
- Uso de hooks React Query (GEOWEB)
- Uso de funcoes vanilla (qualquer app)
- Tratamento de erros HTTP tipados
- Upload de arquivos com progresso

<!-- CARF-INDEX-START -->
> Indice gerado automaticamente. Nao edite manualmente.

## Documentos (3)

| Documento | Status |
|:----------|:-------|
| [Getting Started](./01-getting-started.md) | active |
| [Error Handling - Guia Pratico](./02-error-handling.md) | review |
| [File Upload - Guia Pratico](./03-file-upload.md) | review |

<!-- CARF-INDEX-END -->
