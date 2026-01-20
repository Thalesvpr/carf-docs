---
status: review
updated: 2026-01-17
---

# Embed de Vídeo

Guia para incluir vídeos do YouTube em páginas de documentação.

Fazer upload do vídeo para canal YouTube do projeto ou canal pessoal autorizado. Configurar visibilidade como público ou não listado conforme necessidade. Copiar ID do vídeo da URL (parte após v= ou youtu.be/).

Usar componente YouTubeEmbed em arquivo MDX para embed responsivo. Importar componente no topo do arquivo e usar com props videoId contendo ID do vídeo e title descrevendo conteúdo para acessibilidade.

Alternativa em Markdown puro usa sintaxe de imagem com URL de thumbnail linkando para vídeo. Menos elegante que componente mas funciona em arquivos .md sem necessidade de MDX.

Adicionar transcrição abaixo do vídeo para acessibilidade. Usuários com deficiência auditiva ou em ambientes sem áudio se beneficiam de texto alternativo. Transcrição também melhora SEO pois conteúdo é indexável.

Considerar timestamps para vídeos longos listando seções com links diretos para pontos específicos. Formato de link inclui parâmetro t com segundos (ex: ?t=120 para 2 minutos).

Testar embed localmente verificando que vídeo carrega, player é responsivo em diferentes tamanhos de tela, e atributo title está presente no iframe para screen readers.

Performance considerada com lazy loading habilitado por padrão no componente. Vídeo só carrega quando usuário scrolla até elemento reduzindo tempo de carregamento inicial da página.
