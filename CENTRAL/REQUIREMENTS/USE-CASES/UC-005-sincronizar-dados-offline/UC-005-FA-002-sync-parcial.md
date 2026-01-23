---
id: UC-005-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-005-FA-002: Sincronizacao Parcial (Apenas Fotos)

Fluxo alternativo do UC-005 para sincronizar apenas fotos liberando espaco de armazenamento.

## Condicao

Na tela de sincronizacao, FIELD_AGENT deseja enviar apenas fotos mantendo dados cadastrais para edicao posterior.

## Fluxo

1. FIELD_AGENT clica em Sincronizar Apenas Fotos
2. Sistema exibe confirmacao com estatisticas (quantidade e tamanho)
3. FIELD_AGENT confirma operacao
4. Sistema comprime e envia fotos para servidor
5. Servidor valida e armazena fotos
6. Sistema deleta fotos locais apos confirmacao
7. Sistema exibe resumo com espaco liberado

## Dados Sincronizados

- Fotos pendentes de todas unidades

## Dados Nao Sincronizados

- Unidades
- Titulares
- Vinculos

## Retorno

Fotos sincronizadas e removidas localmente. Dados cadastrais permanecem pendentes.

## Pos-condicoes

- Espaco de armazenamento liberado
- Unidades e titulares aguardando sincronizacao completa
