---
type: leaf
status: review
updated: 2026-02-07
---

# Template de Manual

Template para paginas da secao /manuais/ que documentam uso das aplicacoes GEOWEB, REURBCAD e ADMIN.

Frontmatter obrigatorio define title com nome da funcionalidade ou fluxo documentado, description com resumo de 1-2 linhas, source apontando para doc de feature no PROJECTS correspondente, sidebar com order e label, e draft false.

## Estrutura do Frontmatter

| Campo | Obrigatorio | Descricao | Exemplo |
|-------|-------------|-----------|---------|
| title | Sim | Nome da funcionalidade | Cadastrar Unidade Habitacional |
| description | Sim | Resumo 1-2 linhas | Passo a passo para registrar unidade no GeoWeb |
| source | Sim | Path doc feature em PROJECTS | PROJECTS/GEOWEB/DOCS/FEATURES/02-unit-crud.md |
| sidebar.order | Sim | Posicao na navegacao | 3 |
| sidebar.label | Sim | Label curto | Cadastrar Unidade |
| draft | Sim | false para publicar | false |

## Estrutura do Conteudo

Introducao explica o que funcionalidade faz e quando usar. Pre-requisitos listados como checklist com permissoes necessarias, dados anteriores, e condicoes previas. Aside tipo note para orientacoes sobre permissoes.

Passo a passo usa componente Steps com etapas numeradas. Cada passo descreve acao com resultado esperado. Imagens inline ilustram onde clicar (sintaxe markdown para imagens em /images/manuais/). Tabelas documentam campos do formulario com colunas Campo, Obrigatorio, e Descricao. Aside tipo tip para atalhos e dicas, caution para acoes irreversiveis.

Secao de opcoes avancadas usa componente Tabs com TabItem para alternativas (por exemplo, mover vertices versus adicionar vertices).

Secao de solucao de problemas usa h3 para cada problema em formato pergunta. Cada entrada tem Causa em bold seguida de explicacao, e Solucao em bold seguida de passos numerados ou orientacao. Linkar para pagina de status se problema persistir.

Secao Ver Tambem usa CardGrid com Cards linkando para funcionalidades relacionadas e guias conceituais complementares.

## Exemplo de Frontmatter

Para manual de cadastro de unidade: title seria Cadastrar Unidade Habitacional, description seria Passo a passo completo para cadastrar nova unidade habitacional no GeoWeb com desenho de geometria e preenchimento de dados, source seria PROJECTS/GEOWEB/DOCS/FEATURES/02-unit-crud.md, sidebar com order 3 e label Cadastrar Unidade, draft false.
