---
type: leaf
status: review
updated: 2026-02-07
---

# Padroes de Componentes

Especificacao dos padroes para criacao de componentes Astro no WEBDOCS, incluindo estrutura, props, estilos e hidratacao.

## Estrutura de Componente Astro

Todo componente Astro segue estrutura com tres secoes. Frontmatter no bloco --- no topo contem TypeScript com interface Props, imports, logica server-side, e destructuring de Astro.props. Template apos frontmatter usa HTML com expressoes JSX, referenciando props, slots para conteudo filho, e class:list para classes condicionais. Estilos em tag style no final sao scoped por padrao.

## Interface Props e Naming

Todo componente deve definir interface Props para tipagem. Nome da interface e sempre Props (nunca IProps ou ComponentProps). Props comuns incluem class (string opcional) e id (string opcional).

| Tipo | Padrao | Exemplos |
|------|--------|----------|
| Componentes | PascalCase | StatusGrid, UserMenu |
| Classes CSS | kebab-case | status-grid, service-card |
| Variaveis CSS | --carf-{categoria}-{nome} | --carf-color-primary |

## Slots e Classes Condicionais

Slots permitem conteudo filho. Slot padrao recebe conteudo principal. Slots nomeados usam atributo name para areas especificas. Fallback define conteudo quando nenhum filho passado.

Usar class:list para classes condicionais aceitando array com strings estaticas, objetos condicionais, variaveis dinamicas, e arrays aninhados.

Diretivas de hidratacao, uso de React, e acessibilidade estao em 08-padroes-componentes-avancado.md.
