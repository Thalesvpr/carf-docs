---
type: readme
status: review
updated: 2026-01-23
---

# UC-005: Sincronizar Dados Offline

Caso de uso para sincronizacao bidirecional de dados entre app mobile e servidor. O fluxo envolve envio de dados coletados offline (PUSH) e recebimento de atualizacoes do servidor (PULL), com resolucao de conflitos quando necessario.

O [fluxo principal](./UC-005-sincronizar-dados-offline.md) documenta a sincronizacao completa. Os fluxos alternativos cobrem sincronizacao automatica em background (FA-001) e sincronizacao parcial apenas de fotos (FA-002). Os fluxos de excecao tratam perda de conexao (FE-001), erro de validacao (FE-002), token expirado (FE-003) e espaco insuficiente (FE-004).


<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (7)

| Documento | Status |
|-----------|--------|
| [UC-005-FA-001: Sincronização Automática em Background](./UC-005-FA-001-sync-automatico.md) | ⚠ |
| [UC-005-FA-002: Sincronização Parcial (Apenas Fotos)](./UC-005-FA-002-sync-parcial.md) | ⚠ |
| [UC-005-FE-001: Perda de Conexão Durante Sync](./UC-005-FE-001-perda-conexao.md) | ⚠ |
| [UC-005-FE-002: Erro de Validação no Servidor](./UC-005-FE-002-erro-validacao.md) | ⚠ |
| [UC-005-FE-003: Token Expirado](./UC-005-FE-003-token-expirado.md) | ⚠ |
| [UC-005-FE-004: Espaço Insuficiente (Pull)](./UC-005-FE-004-espaco-insuficiente.md) | ⚠ |
| [UC-005: Sincronizar Dados Offline](./UC-005-sincronizar-dados-offline.md) | ⚠ |

<!-- CARF-INDEX-END -->
