---
type: readme
status: approved
updated: 2026-01-25
---

# Modo Offline e Sincronizacao

Requisitos funcionais para operacao offline-first do aplicativo mobile REURBCAD e sincronizacao de dados com backend GEOAPI. Arquitetura projetada para trabalho em comunidades remotas sem conectividade, permitindo coleta completa de dados em campo com sincronizacao posterior.

Os requisitos [RF-182](./RF-182-modo-offline-mobile.md) a [RF-186](./RF-186-tirar-fotos-offline.md) cobrem capacidades offline do aplicativo mobile incluindo download inicial de dados do tenant, criacao e edicao de unidades, e captura de fotos utilizando SQLite/WatermelonDB como banco local. Os requisitos [RF-187](./RF-187-sincronização-manual.md) a [RF-191](./RF-191-resolução-de-conflitos.md) tratam mecanismos de sincronizacao manual e automatica, delta sync incremental e resolucao de conflitos. Os requisitos [RF-192](./RF-192-endpoint-de-pull.md) a [RF-196](./RF-196-log-de-sincronização.md) especificam endpoints da GEOAPI para pull/push de dados e recursos de gestao local.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (15)

| Documento | Status |
|-----------|--------|
| [RF-182: Modo Offline Mobile](./RF-182-modo-offline-mobile.md) | ⚠ |
| [RF-183: Download Inicial de Dados](./RF-183-download-inicial-de-dados.md) | ⚠ |
| [RF-184: Criar Unidade Offline](./RF-184-criar-unidade-offline.md) | ⚠ |
| [RF-185: Editar Unidade Offline](./RF-185-editar-unidade-offline.md) | ⚠ |
| [RF-186: Tirar Fotos Offline](./RF-186-tirar-fotos-offline.md) | ⚠ |
| [RF-187: Sincronizacao Manual](./RF-187-sincronização-manual.md) | ⚠ |
| [RF-188: Sincronizacao Automatica](./RF-188-sincronização-automática.md) | ⚠ |
| [RF-189: Delta Sync Incremental](./RF-189-delta-sync-sincronização-incremental.md) | ⚠ |
| [RF-190: Deteccao de Conflitos](./RF-190-detecção-de-conflitos.md) | ⚠ |
| [RF-191: Resolucao de Conflitos](./RF-191-resolução-de-conflitos.md) | ⚠ |
| [RF-192: Endpoint de Pull](./RF-192-endpoint-de-pull.md) | ⚠ |
| [RF-193: Endpoint de Push](./RF-193-endpoint-de-push.md) | ⚠ |
| [RF-194: Limpeza de Dados Locais](./RF-194-limpeza-de-dados-locais.md) | ⚠ |
| [RF-195: Indicador de Pendencias](./RF-195-indicador-de-pendências.md) | ⚠ |
| [RF-196: Log de Sincronizacao](./RF-196-log-de-sincronização.md) | ⚠ |

<!-- CARF-INDEX-END -->
