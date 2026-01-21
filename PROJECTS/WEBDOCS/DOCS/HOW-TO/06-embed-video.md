---
status: review
updated: 2026-01-21
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

## Sintaxe do Componente MDX

```mdx
---
title: "Página com Vídeo"
---

import { YouTubeEmbed } from '../../components/content/YouTubeEmbed.astro';

# Tutorial em Vídeo

Assista o vídeo abaixo para entender o processo:

<YouTubeEmbed
  videoId="dQw4w9WgXcQ"
  title="Tutorial de cadastro de unidades"
/>

## Com tempo inicial

<YouTubeEmbed
  videoId="dQw4w9WgXcQ"
  title="Seção sobre validação"
  startTime={120}
/>
```

## Alternativa Markdown Puro

Para arquivos .md sem suporte a MDX:

```markdown
[![Título do Vídeo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

*Clique na imagem para assistir no YouTube*
```

## Exemplo com Transcrição

```mdx
<YouTubeEmbed
  videoId="dQw4w9WgXcQ"
  title="Cadastro de unidades - tutorial completo"
/>

<details>
<summary>Transcrição do vídeo</summary>

**00:00** - Introdução ao cadastro de unidades
**01:30** - Acessando o módulo de cadastro
**03:00** - Preenchendo campos obrigatórios
**05:15** - Desenhando a geometria no mapa
**08:00** - Salvando e enviando para aprovação

</details>
```

## Timestamps Clicáveis

```markdown
### Índice do vídeo

- [0:00 - Introdução](https://www.youtube.com/watch?v=VIDEO_ID&t=0)
- [2:00 - Configuração inicial](https://www.youtube.com/watch?v=VIDEO_ID&t=120)
- [5:30 - Cadastro de dados](https://www.youtube.com/watch?v=VIDEO_ID&t=330)
- [10:00 - Validação e envio](https://www.youtube.com/watch?v=VIDEO_ID&t=600)
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
