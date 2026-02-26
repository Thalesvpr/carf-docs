---
id: UC-010-FE-003
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-010-FE-003: Layer Nao Encontrado

Fluxo de excecao do UC-010 quando servidor WMS nao retorna layers disponiveis.

## Condicao

No passo 9 do UC-010, sistema parseia XML mas lista de layers esta vazia.

## Fluxo

1. Sistema parseia XML do GetCapabilities
2. Sistema busca elementos Layer
3. Sistema detecta lista vazia
4. Sistema exibe modal informando ausencia
5. Sistema sugere verificacoes
6. ADMIN consulta administrador do servidor externo

## Causas Comuns

- Servidor sem dados publicados
- Layers requerem autenticacao
- Permissoes restritivas no servidor
- URL aponta para servico diferente

## Retorno

Warning exibido. ADMIN verifica configuracao do servidor externo ou solicita liberacao.
