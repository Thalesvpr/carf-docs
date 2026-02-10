---
type: leaf
status: review
updated: 2026-02-07
---

# Template de Guia - Estrutura de Conteudo

Detalhes da estrutura de conteudo para paginas de guia. Documento complementar a 01-template-guia.md.

## Imports e Titulo

Imports de componentes Starlight no topo: Aside, Steps, Card, CardGrid, Tabs, TabItem conforme necessidade. Titulo h1 repete title do frontmatter. Introducao em 3-4 linhas explica valor para o leitor.

## Secoes Principais

Secoes usam h2 para conceito principal, aplicacao pratica, e proximos passos. Subsecoes usam h3. Steps component numera passos sequenciais. Tabelas documentam campos e status.

Aside com tipo note para informacao adicional, tip para dica pratica, caution para situacoes de cuidado.

## Secoes Finais

Secao de proximos passos usa CardGrid com Cards linkando para guias e manuais relacionados. Secao Ver Tambem lista links como lista markdown para paginas complementares e aprofundamento.

## Exemplo de Frontmatter

Para pagina sobre aprovacao: title seria Fluxo de Aprovacao de Unidades, description seria Entenda como funciona o processo de aprovacao de unidades habitacionais no CARF desde a coleta ate a validacao final, source seria CENTRAL/WORKFLOWS/04-analyst-validation-workflow.md, sidebar com order 4 e label Aprovacao, draft false.
