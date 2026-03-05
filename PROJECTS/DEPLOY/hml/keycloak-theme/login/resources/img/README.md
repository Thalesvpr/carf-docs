# CARF Theme - Image Assets

Este diretório contém os assets visuais do tema Keycloak CARF.

## Arquivos Necessários

### 1. logo.svg (OBRIGATÓRIO)
**Arquivo atual**: Placeholder SVG
**Substituir por**: Logo oficial CARF

**Especificações recomendadas:**
- Formato: SVG (vetorial, escala infinita)
- Largura máxima: 200-300px
- Altura máxima: 80-100px
- Cores: Verde institucional (#2C5F2D), Verde claro (#97BC62)
- Fundo: Transparente
- Otimizado para web (< 50KB)

**Onde é usado:**
- Topo da página de login
- Topo da página de registro
- Topo de todas as páginas de autenticação

### 2. favicon.ico (RECOMENDADO)
**Arquivo atual**: NÃO EXISTE - precisa ser criado
**Criar**: Favicon do CARF

**Especificações:**
- Formato: ICO multi-size (16x16, 32x32, 48x48)
- Cores: Verde institucional CARF
- Ícone simples e reconhecível
- Pode usar apenas a inicial "C" ou símbolo da casa

**Como criar:**
```bash
# Opção 1: Usando ImageMagick
convert logo.svg -resize 16x16 -depth 8 -colors 256 -alpha on favicon-16.png
convert logo.svg -resize 32x32 -depth 8 -colors 256 -alpha on favicon-32.png
convert logo.svg -resize 48x48 -depth 8 -colors 256 -alpha on favicon-48.png
convert favicon-16.png favicon-32.png favicon-48.png favicon.ico

# Opção 2: Usando ferramenta online
# https://favicon.io/favicon-converter/
# https://realfavicongenerator.net/
```

**Onde é usado:**
- Aba do navegador
- Bookmarks
- Histórico do navegador

### 3. background.jpg (OPCIONAL)
**Arquivo atual**: NÃO EXISTE - opcional
**Adicionar se desejar**: Imagem de fundo para desktop

**Especificações:**
- Formato: JPG ou WebP
- Tamanho: 1920x1080px (Full HD) ou maior
- Otimizado: < 500KB
- Tema: Relacionado a cidades, urbanização, mapas, ou abstrato verde
- Estilo: Sutil, não deve interferir na legibilidade

**Sugestões de tema:**
- Vista aérea de cidade/bairro (relacionado a regularização fundiária)
- Mapa topográfico estilizado
- Padrão geométrico abstrato com tons de verde
- Foto de comunidade urbana (desfocada)

**Onde é usado:**
- Fundo da página de login em resoluções desktop (>1024px)
- Aplicado com overlay semi-transparente verde (#2C5F2D com 85% opacidade)

**CSS:**
```css
@media (min-width: 1024px) {
  body {
    background-image: url('../img/background.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
  }
}
```

### 4. background-mobile.jpg (OPCIONAL)
**Arquivo atual**: NÃO EXISTE - opcional
**Adicionar se desejar**: Versão otimizada para mobile

**Especificações:**
- Formato: JPG ou WebP
- Tamanho: 1080x1920px (vertical)
- Otimizado: < 200KB
- Mesmo tema que background.jpg

## Estrutura de Diretório

```
resources/img/
├── README.md                    # Este arquivo
├── logo.svg                     # ✅ Logo principal (PLACEHOLDER - substituir)
├── favicon.ico                  # ❌ Favicon (CRIAR)
├── background.jpg               # ❌ Background desktop (OPCIONAL)
├── background-mobile.jpg        # ❌ Background mobile (OPCIONAL)
└── social/                      # (futuro) Ícones de provedores sociais
    ├── google.svg
    ├── facebook.svg
    └── microsoft.svg
```

## Como Substituir os Assets

### Passo 1: Preparar os arquivos
```bash
# Navegar até o diretório
cd C:\DEV\CARF\PROJECTS\KEYCLOAK\SRC-CODE\carf-keycloak\themes\carf\login\resources\img

# Backup do placeholder (opcional)
mv logo.svg logo-placeholder.svg

# Copiar logo real
cp /caminho/para/logo-carf-oficial.svg logo.svg
```

### Passo 2: Validar SVG
```bash
# Verificar se SVG é válido
xmllint --noout logo.svg

# Otimizar SVG (remover metadados desnecessários)
svgo logo.svg --output logo.svg
```

### Passo 3: Testar no navegador
```bash
# Iniciar Keycloak com tema
docker-compose -f docker-compose.dev.yml up

# Acessar: http://localhost:8080/realms/carf/account
# Verificar se logo aparece corretamente
# Testar em diferentes resoluções
```

### Passo 4: Validar acessibilidade
- Logo deve ter alt text apropriado (configurado em messages_pt_BR.properties)
- Contraste adequado com background
- Visível em modo claro e escuro (se aplicável)
- Não deve pixelar em telas de alta resolução

## Otimização de Assets

### SVG
```bash
# Instalar SVGO
npm install -g svgo

# Otimizar
svgo logo.svg -o logo-optimized.svg
```

### JPG
```bash
# Instalar ImageMagick
# Windows: https://imagemagick.org/script/download.php

# Otimizar
convert background.jpg -quality 85 -resize 1920x1080 background-optimized.jpg
```

### WebP (formato moderno)
```bash
# Converter JPG para WebP (melhor compressão)
cwebp -q 80 background.jpg -o background.webp
```

## Diretrizes de Design

### Cores CARF
- **Verde Primário**: #2C5F2D
- **Verde Claro**: #97BC62
- **Amarelo Destaque**: #FFB300
- **Cinza Fundo**: #F5F5F5
- **Texto**: #333333

### Tipografia
- Fonte: Sans-serif (Arial, Helvetica, Segoe UI)
- Logo: Pode usar fonte customizada se parte do SVG

### Estilo Visual
- Clean e profissional
- Minimalista
- Acessível (WCAG 2.1 AA)
- Responsivo

## Checklist de Assets

- [ ] logo.svg substituído por versão oficial
- [ ] favicon.ico criado e testado
- [ ] background.jpg adicionado (se desejado)
- [ ] Assets otimizados (< 50KB cada, exceto background)
- [ ] Testado em Chrome, Firefox, Edge, Safari
- [ ] Testado em resoluções mobile, tablet, desktop
- [ ] Alt text configurado corretamente
- [ ] Contraste adequado validado

## Recursos Úteis

**Geradores de Favicon:**
- https://favicon.io/
- https://realfavicongenerator.net/

**Otimizadores de Imagem:**
- https://tinypng.com/ (PNG/JPG)
- https://jakearchibald.github.io/svgomg/ (SVG online)

**Bancos de Imagens:**
- https://unsplash.com/ (fotos gratuitas)
- https://www.pexels.com/ (fotos gratuitas)

**Validadores:**
- https://validator.w3.org/ (validar SVG)
- https://webaim.org/resources/contrastchecker/ (contraste de cores)

## Contato

Para dúvidas sobre assets visuais, entre em contato com a equipe de design ou o administrador do sistema.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (62) antes do rodapé - considerar converter para parágrafo denso; Contém code blocks - considerar converter para prosa.

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
