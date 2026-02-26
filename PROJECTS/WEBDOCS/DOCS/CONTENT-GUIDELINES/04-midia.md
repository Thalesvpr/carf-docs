---
type: leaf
status: review
updated: 2026-01-21
---

# Mídia

Diretrizes para uso de fotos, vídeos e diagramas no conteúdo do WEBDOCS garantindo qualidade, performance e acessibilidade.

Screenshots são armazenados em public/images/ do repositório organizados por seção (manuais/reurbweb/, manuais/reurbcad/, etc). Formato PNG para interfaces com texto, JPEG para fotos. Resolução 2x para displays retina com width/height explícitos evitando layout shift.

Captura de screenshots deve mostrar apenas área relevante sem elementos pessoais ou dados sensíveis. Dados de exemplo usam informações fictícias óbvias (João da Silva, CPF 000.000.000-00). Destacar elementos importantes com anotações ou setas adicionadas via ferramenta de edição.

Vídeos são hospedados no YouTube e embutidos via componente YouTubeEmbed. Não armazenar vídeos no repositório devido ao tamanho. Vídeos devem ter thumbnail atraente, título descritivo, e descrição com timestamps para seções.

Componente YouTubeEmbed aceita videoId e title como props. Renderiza iframe responsivo com lazy loading. Atributo title é obrigatório para acessibilidade. Considerar adicionar transcrição abaixo do vídeo para acessibilidade e SEO.

Diagramas são criados com Mermaid sempre que possível por serem texto pesquisável e atualizável facilmente. Diagramas complexos podem usar imagens SVG exportadas de ferramentas como Excalidraw ou Figma armazenadas em public/images/diagrams/.

Otimização de imagens acontece automaticamente via @astrojs/image durante build. Imagens são convertidas para formatos modernos (WebP, AVIF) e redimensionadas conforme configuração. Imagens em public/ não são processadas então devem ser otimizadas antes do commit.
