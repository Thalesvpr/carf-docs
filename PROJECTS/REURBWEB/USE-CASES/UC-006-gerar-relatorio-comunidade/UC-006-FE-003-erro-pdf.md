---
id: UC-006-FE-003
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-006-FE-003: Erro ao Gerar PDF

Fluxo de excecao do UC-006 quando conversao para PDF falha.

## Condicao

Durante conversao de HTML para PDF do UC-006, sistema encontra erro de renderizacao.

## Fluxo

1. Sistema tenta converter HTML para PDF
2. Sistema detecta falha na conversao
3. Sistema tenta retry com configuracoes otimizadas
4. Se retry falha, sistema salva versao HTML como fallback
5. Sistema notifica usuario sobre formato alternativo
6. Sistema oferece opcao de retentar PDF

## Causas Comuns

- Timeout de renderizacao com pagina complexa
- Fontes nao encontradas no servidor
- Memoria insuficiente para processar imagens grandes

## Fallback HTML

- Mantem fidelidade visual completa
- Graficos interativos funcionais
- Pode ser visualizado no navegador

## Retorno

HTML salvo como alternativa. Usuario pode baixar HTML ou retentar geracao PDF.

## Pos-condicoes

- Relatorio disponivel em formato HTML
- Opcao de nova tentativa em PDF oferecida
