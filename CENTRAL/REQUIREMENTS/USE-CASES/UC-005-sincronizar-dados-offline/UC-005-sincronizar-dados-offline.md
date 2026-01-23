---
id: UC-005
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-005: Sincronizar Dados Offline

## Atores

- Primario: FIELD_AGENT
- Secundario: Servidor GEOAPI

## Pre-condicoes

- Dados pendentes marcados para sincronizacao
- Conexao com internet disponivel
- Token de autenticacao valido

## Fluxo Principal

1. App detecta conexao disponivel ou FIELD_AGENT clica Sincronizar
2. Sistema exibe tela de sincronizacao com progresso
3. Sistema executa fase PULL (baixar atualizacoes do servidor)
4. Sistema aplica alteracoes remotas no banco local
5. Sistema detecta conflitos se mesma entidade editada local e remotamente
6. Sistema executa fase PUSH (enviar dados locais)
7. Sistema comprime fotos antes do envio
8. Sistema envia dados em lote para servidor
9. Servidor valida e processa cada item
10. Sistema atualiza registros locais com IDs do servidor
11. Sistema executa fase de resolucao de conflitos se necessario
12. Sistema atualiza timestamp de ultima sincronizacao
13. Sistema exibe resumo com estatisticas

## Fluxos Alternativos

- FA-001: Sincronizacao automatica em background
- FA-002: Sincronizacao parcial (apenas fotos)

## Fluxos de Excecao

- FE-001: Perda de conexao durante sync
- FE-002: Erro de validacao no servidor
- FE-003: Token expirado
- FE-004: Espaco insuficiente (pull)

## Pos-condicoes

- Dados locais sincronizados com servidor
- Registros marcados como sincronizados
- Conflitos resolvidos ou pendentes para resolucao manual
