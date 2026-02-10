---
type: leaf
status: review
updated: 2026-02-07
---

# Template de Guia

Template para paginas da secao /guia/ que explicam como usar a documentacao e conceitos do sistema CARF.

Frontmatter obrigatorio define title, description para SEO, source apontando para arquivo CENTRAL correspondente, sidebar com order e label, e draft false.

Introducao no primeiro paragrafo contextualiza o conteudo explicando o que leitor aprendera. Maximo 3-4 linhas focando no beneficio para o leitor.

Corpo divide conteudo em secoes h2 para topicos principais e h3 para subtopicos. Callouts (Aside) destacam informacoes com tipos note, tip, e caution.

Conclusao sugere proximos passos com links usando CardGrid e Card do Starlight.

## Estrutura do Frontmatter

| Campo | Obrigatorio | Descricao | Exemplo |
|-------|-------------|-----------|---------|
| title | Sim | Nome descritivo | Fluxo de Aprovacao de Unidades |
| description | Sim | Resumo 1-2 linhas SEO | Entenda o processo de aprovacao |
| source | Sim | Path doc fonte CENTRAL | CENTRAL/WORKFLOWS/04-analyst-validation-workflow.md |
| sidebar.order | Sim | Posicao navegacao | 4 |
| sidebar.label | Sim | Label curto | Aprovacao |
| draft | Sim | false para publicar | false |

Detalhes da estrutura de conteudo em 01-template-guia-conteudo.md.
