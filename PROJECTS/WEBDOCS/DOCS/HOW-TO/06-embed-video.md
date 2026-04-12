---
type: leaf
status: review
updated: 2026-02-07
---

# Embed de Video

Guia para incluir videos do YouTube em paginas de documentacao.

## Preparacao do Video

Fazer upload do video para canal YouTube do projeto ou canal pessoal autorizado. Configurar visibilidade como publico ou nao listado conforme necessidade. Copiar ID do video da URL (parte apos v= ou youtu.be/).

## Componente MDX

Em arquivos .mdx, importar o componente YouTubeEmbed de components/content/YouTubeEmbed.astro no topo do arquivo. Utilizar o componente passando propriedade videoId com o ID do video e propriedade title descrevendo conteudo para acessibilidade. Para iniciar em ponto especifico, adicionar propriedade startTime com valor em segundos.

## Alternativa Markdown Puro

Para arquivos .md sem suporte a MDX, usar sintaxe de imagem Markdown com URL de thumbnail do YouTube linkando para o video. A URL de thumbnail segue formato img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg e o link aponta para youtube.com/watch?v=VIDEO_ID. Menos elegante que componente mas funciona sem dependencia de MDX.

## Transcricao

Adicionar transcricao abaixo do video para acessibilidade. Usuarios com deficiencia auditiva ou em ambientes sem audio se beneficiam de texto alternativo. Transcricao tambem melhora SEO pois conteudo e indexavel. Usar elemento details com summary para transcricao colapsavel, listando timestamps com descricao de cada secao do video.

## Timestamps Clicaveis

Para videos longos, listar secoes com links diretos para pontos especificos. Formato de link inclui parametro t com valor em segundos na URL do YouTube (ex: parametro t=120 para 2 minutos).

## Performance e Teste

Lazy loading habilitado por padrao no componente. Video so carrega quando usuario scrolla ate elemento reduzindo tempo de carregamento inicial. Testar embed localmente verificando que video carrega, player e responsivo em diferentes tamanhos de tela, e atributo title esta presente no iframe para screen readers.
