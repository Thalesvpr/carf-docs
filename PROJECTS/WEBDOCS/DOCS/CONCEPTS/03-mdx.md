---
status: review
updated: 2026-01-21
---

# MDX

MDX é extensão do Markdown que permite usar componentes JSX dentro do conteúdo. Arquivos .mdx são processados combinando sintaxe familiar do Markdown com poder de componentes React ou Astro para criar documentação interativa sem sacrificar simplicidade de autoria.

Import de componentes no topo do arquivo MDX disponibiliza para uso no conteúdo. Componentes Astro (.astro) ou React (.tsx) podem ser importados e usados inline com props como qualquer JSX. Útil para elementos reutilizáveis como callouts, code tabs, ou embeds interativos.

Componentes globais configurados em astro.config.mjs ficam disponíveis em todos arquivos MDX sem necessidade de import explícito. WEBDOCS define componentes globais Callout para notas e avisos, CodeTabs para exemplos em múltiplas linguagens, Mermaid para diagramas, e YouTubeEmbed para vídeos.

Expressões JavaScript entre chaves permitem lógica dinâmica no conteúdo. Variáveis definidas no frontmatter ou importadas podem ser interpoladas no texto. Útil para valores que mudam frequentemente como versões ou datas.

Limitações incluem necessidade de conhecimento básico de JSX para usar componentes customizados, build time maior que Markdown puro devido a processamento adicional, e compatibilidade reduzida com editores que não suportam syntax highlighting de MDX.
