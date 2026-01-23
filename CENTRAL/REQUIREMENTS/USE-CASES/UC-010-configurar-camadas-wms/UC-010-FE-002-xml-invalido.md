---
id: UC-010-FE-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-010-FE-002: XML Invalido

Fluxo de excecao do UC-010 quando resposta do servidor nao e XML valido.

## Condicao

No passo 8 do UC-010, sistema recebe resposta mas nao consegue parsear como XML.

## Fluxo

1. Sistema recebe resposta do servidor
2. Sistema tenta parsear como XML
3. Sistema detecta erro de sintaxe
4. Sistema loga resposta para debug
5. Sistema exibe modal com preview da resposta
6. ADMIN analisa conteudo retornado
7. ADMIN verifica se URL e realmente de servico WMS

## Causas Comuns

- Servidor retornou HTML de erro
- Endpoint retorna JSON ao inves de XML
- XML malformado com tags nao fechadas
- Encoding incorreto corrompendo caracteres

## Retorno

Erro exibido com preview da resposta. ADMIN verifica URL correta do servico WMS.
