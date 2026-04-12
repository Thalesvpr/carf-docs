---
type: leaf
status: review
updated: 2026-02-07
---

# Template de API

Template para paginas da secao /api/ que documentam conceitos e uso da API GEOAPI de forma nao-tecnica complementando Swagger. Secao api e publica diferente de Swagger interativo que requer role dev.

## Estrutura do Frontmatter

| Campo | Obrigatorio | Descricao | Exemplo |
|-------|-------------|-----------|---------|
| title | Sim | Nome do recurso | Unidades Habitacionais |
| description | Sim | Termos de negocio (50-160 chars) | Entenda unidades habitacionais no CARF |
| source | Sim | Path doc API | PROJECTS/GEOAPI/DOCS/API/units.md |
| sidebar.order | Sim | Posicao navegacao | 3 |
| sidebar.label | Sim | Label curto | Unidades |
| draft | Sim | false para publicar | false |

## Estrutura do Conteudo

Introducao explica recurso no contexto de negocio, nao tecnicamente. Imports limitados a Aside, Card, CardGrid.

Secao conceitual (h2 O que sao {Recursos}?) descreve recurso em linguagem acessivel. Secao de campos usa tabela Campo, Descricao, Exemplo. Secao de operacoes lista acoes como h3 com Quando usar e Quem pode.

Detalhes de permissoes, exemplos e ver tambem em 03-template-api-secoes.md.
