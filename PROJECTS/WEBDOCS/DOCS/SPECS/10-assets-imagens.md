---
status: review
updated: 2026-01-17
---

# Assets e Imagens

Organização de screenshots, diagramas e outros assets visuais garantindo consistência e performance.

Estrutura de pastas em public/images/ organiza assets por seção e subsection. Pasta manuais/ subdivide em geoweb/, reurbcad/, e admin/. Pasta sistema/ contém diagramas de fluxo e arquitetura. Pasta changelog/ contém screenshots de novas features por versão.

Nomenclatura de arquivos usa kebab-case descritivo: tela-cadastro-unidade.png, fluxo-aprovacao.svg, botao-salvar-destacado.png. Nome deve indicar conteúdo sem precisar abrir arquivo.

Formatos recomendados: PNG para screenshots de interface com texto legível, JPEG para fotos com compressão adequada, SVG para diagramas e ícones vetoriais. WebP e AVIF gerados automaticamente por @astrojs/image.

Resolução de screenshots em 2x (retina) com width e height explícitos no Markdown evitando layout shift. Tamanho típico: 1600x900px para capturas full-screen, 800x600px para capturas de componente.

Otimização manual necessária para assets em public/ que não são processados automaticamente. Usar ferramentas como ImageOptim, Squoosh ou TinyPNG antes do commit. Target: PNG abaixo de 200KB, JPEG abaixo de 150KB.

Diagramas Mermaid preferidos quando possível pois são texto pesquisável, versionável, e atualizável. Usar imagens SVG exportadas apenas para diagramas complexos que Mermaid não suporta.

Alt text obrigatório em todas imagens descrevendo informação transmitida. Para screenshots, descrever ação ou resultado mostrado: "Tela de cadastro com campos nome e CPF preenchidos" ao invés de "Screenshot da tela".
