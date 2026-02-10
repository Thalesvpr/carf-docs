---
type: leaf
status: review
updated: 2026-02-07
---

# Adicionar Pagina

Guia para criar novo documento no WEBDOCS com frontmatter correto e estrutura adequada para a secao destino.

## Estrutura de Pastas

| Pasta | Conteudo | Publico |
|---|---|---|
| src/content/docs/guia/ | Conceitos e workflows | Todos usuarios |
| src/content/docs/sistema/ | Visao geral do CARF | Analistas+ |
| src/content/docs/manuais/geoweb/ | Manual do GeoWeb | Analistas |
| src/content/docs/manuais/reurbcad/ | Manual do REURBCAD | Agentes de campo |
| src/content/docs/manuais/admin/ | Manual Admin | Administradores |
| src/content/docs/api/ | Documentacao da API | Desenvolvedores |
| src/content/docs/status/ | Pagina de status | Todos |

Identificar secao destino e navegar para pasta correspondente. Criar arquivo com nome em kebab-case e extensao .md para Markdown puro ou .mdx se precisar de componentes Astro.

## Frontmatter Obrigatorio

| Campo | Tipo | Descricao |
|---|---|---|
| title | string | Nome da pagina em Title Case portugues |
| source | string | Caminho exato no carf-docs (ex: CENTRAL/WORKFLOWS/02-field-data-collection-workflow.md) |
| sidebar.order | number | Posicao na navegacao lateral |
| sidebar.label | string | Label curto para sidebar (opcional) |
| sidebar.badge | string | Badge como "Novo" ou "Atualizado" (opcional) |
| draft | boolean | Se true, pagina nao aparece em producao (opcional) |

## Escrita do Conteudo

Escrever conteudo seguindo content guidelines. Introducao contextualiza tema, corpo desenvolve com headings hierarquicos, conclusao sugere proximos passos. Usar callouts para destacar informacoes importantes.

Para paginas MDX, importar componentes Astro Starlight como Aside, Steps, Card e CardGrid no topo do arquivo. Componentes permitem callouts tipados, passos numerados, e grids de cards com icones.

Adicionar screenshots se necessario salvando em public/images/ na subpasta correspondente a secao. Referencias de imagem usam path relativo a public/ sem a pasta public no caminho.

## Validacao e Publicacao

Validar localmente executando bun run astro check para verificar frontmatter contra schema Zod, e bun run build para validar links internos. Executar bun run validate:sources para validar campos source.

Criar pull request com nova pagina para review. Preview deployment automatico permite validar aparencia antes de merge. Solicitar review de membro da equipe de documentacao.
