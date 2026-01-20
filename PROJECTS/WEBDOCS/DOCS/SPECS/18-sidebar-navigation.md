# Navegação do Sidebar

Especificação completa da estrutura de navegação do sidebar do WEBDOCS, definindo hierarquia, labels e badges para cada seção.

## Estrutura Completa

```json
{
  "sidebar": [
    {
      "label": "Guia do Usuário",
      "items": [
        { "label": "Bem-vindo", "slug": "guia/bem-vindo" },
        { "label": "Primeiros Passos", "slug": "guia/primeiros-passos" },
        { "label": "Conceitos Básicos", "slug": "guia/conceitos" },
        { "label": "Glossário", "slug": "guia/glossario" },
        { "label": "FAQ", "slug": "guia/faq" }
      ],
      "collapsed": false,
      "roles": ["user", "field-agent", "analyst", "admin", "super-admin", "dev"]
    },
    {
      "label": "O Sistema CARF",
      "items": [
        { "label": "Visão Geral", "slug": "sistema/visao-geral" },
        { "label": "Lei 13.465/2017", "slug": "sistema/lei-reurb" },
        { "label": "Fluxo de Trabalho", "slug": "sistema/fluxo" },
        { "label": "Papéis e Permissões", "slug": "sistema/papeis" },
        { "label": "Entidades", "slug": "sistema/entidades" }
      ],
      "collapsed": false,
      "roles": ["analyst", "admin", "super-admin", "dev"]
    },
    {
      "label": "Manuais",
      "items": [
        {
          "label": "GeoWeb",
          "collapsed": true,
          "items": [
            { "label": "Introdução", "slug": "manuais/geoweb/introducao" },
            { "label": "Navegação no Mapa", "slug": "manuais/geoweb/mapa" },
            { "label": "Cadastro de Unidades", "slug": "manuais/geoweb/unidades" },
            { "label": "Gestão de Titulares", "slug": "manuais/geoweb/titulares" },
            { "label": "Análise e Aprovação", "slug": "manuais/geoweb/analise" },
            { "label": "Relatórios", "slug": "manuais/geoweb/relatorios" }
          ]
        },
        {
          "label": "REURBCAD",
          "collapsed": true,
          "items": [
            { "label": "Introdução", "slug": "manuais/reurbcad/introducao" },
            { "label": "Coleta Offline", "slug": "manuais/reurbcad/coleta" },
            { "label": "Desenho de Geometrias", "slug": "manuais/reurbcad/geometrias" },
            { "label": "Fotografias", "slug": "manuais/reurbcad/fotos" },
            { "label": "Sincronização", "slug": "manuais/reurbcad/sync" }
          ]
        },
        {
          "label": "Admin",
          "collapsed": true,
          "items": [
            { "label": "Introdução", "slug": "manuais/admin/introducao" },
            { "label": "Gestão de Usuários", "slug": "manuais/admin/usuarios" },
            { "label": "Gestão de Equipes", "slug": "manuais/admin/equipes" },
            { "label": "Configurações", "slug": "manuais/admin/config" },
            { "label": "Relatórios", "slug": "manuais/admin/relatorios" }
          ]
        }
      ],
      "roles": ["field-agent", "analyst", "admin", "super-admin", "dev"]
    },
    {
      "label": "API",
      "badge": { "text": "Dev", "variant": "caution" },
      "items": [
        { "label": "Visão Geral", "slug": "api/visao-geral" },
        { "label": "Autenticação", "slug": "api/autenticacao" },
        { "label": "Recursos", "slug": "api/recursos" },
        { "label": "Erros", "slug": "api/erros" },
        { "label": "Swagger", "slug": "api/swagger" }
      ],
      "collapsed": false,
      "roles": ["super-admin", "dev"]
    },
    {
      "label": "Desenvolvedores",
      "badge": { "text": "Dev", "variant": "caution" },
      "items": [
        { "label": "Getting Started", "slug": "dev/getting-started" },
        { "label": "Arquitetura", "slug": "dev/arquitetura" },
        { "label": "Bibliotecas", "slug": "dev/bibliotecas" },
        {
          "label": "Componentes UI",
          "collapsed": true,
          "items": [
            { "label": "Visão Geral", "slug": "dev/components" },
            { "label": "Design Tokens", "slug": "dev/components/tokens" },
            {
              "label": "Ações",
              "items": [
                { "label": "Button", "slug": "dev/components/button" },
                { "label": "IconButton", "slug": "dev/components/icon-button" }
              ]
            },
            {
              "label": "Inputs",
              "items": [
                { "label": "Input", "slug": "dev/components/input" },
                { "label": "Select", "slug": "dev/components/select" },
                { "label": "Checkbox", "slug": "dev/components/checkbox" },
                { "label": "Switch", "slug": "dev/components/switch" }
              ]
            },
            {
              "label": "Feedback",
              "items": [
                { "label": "Toast", "slug": "dev/components/toast" },
                { "label": "Alert", "slug": "dev/components/alert" },
                { "label": "Progress", "slug": "dev/components/progress" }
              ]
            },
            {
              "label": "Overlays",
              "items": [
                { "label": "Dialog", "slug": "dev/components/dialog" },
                { "label": "Popover", "slug": "dev/components/popover" },
                { "label": "Tooltip", "slug": "dev/components/tooltip" }
              ]
            },
            {
              "label": "Layout",
              "items": [
                { "label": "Card", "slug": "dev/components/card" },
                { "label": "Accordion", "slug": "dev/components/accordion" }
              ]
            },
            {
              "label": "Data Display",
              "items": [
                { "label": "Table", "slug": "dev/components/table" },
                { "label": "Badge", "slug": "dev/components/badge" },
                { "label": "Avatar", "slug": "dev/components/avatar" }
              ]
            }
          ]
        },
        { "label": "Contribuindo", "slug": "dev/contribuindo" },
        { "label": "Debug", "slug": "dev/debug" }
      ],
      "collapsed": false,
      "roles": ["dev"]
    },
    {
      "label": "Status",
      "items": [
        { "label": "Status dos Serviços", "slug": "status" }
      ],
      "roles": ["admin", "super-admin", "dev"]
    },
    {
      "label": "Changelog",
      "items": [
        { "label": "Histórico de Versões", "slug": "changelog" }
      ],
      "roles": ["admin", "super-admin", "dev"]
    }
  ]
}
```

## Configuração Starlight

A estrutura acima é convertida para formato Starlight em astro.config.mjs.

```json
{
  "starlight_format": {
    "static": "Array de items definido no config",
    "dynamic": "Filtrado por role no middleware (não implementado por Starlight)",
    "workaround": "Componente customizado SidebarNav que filtra por Astro.locals.user.roles"
  }
}
```

## Badges

```json
{
  "badge_variants": {
    "note": {
      "color": "blue",
      "usage": "Informação adicional"
    },
    "tip": {
      "color": "green",
      "usage": "Dicas e melhores práticas"
    },
    "caution": {
      "color": "yellow",
      "usage": "Seções restritas (Dev, Beta)"
    },
    "danger": {
      "color": "red",
      "usage": "Conteúdo sensível ou destrutivo"
    },
    "success": {
      "color": "green",
      "usage": "Features novas"
    }
  },
  "common_badges": {
    "Novo": { "variant": "success", "usage": "Feature recém-lançada" },
    "Beta": { "variant": "caution", "usage": "Feature em teste" },
    "Dev": { "variant": "caution", "usage": "Seção para desenvolvedores" }
  }
}
```

## Ordem e Agrupamento

```json
{
  "ordering_rules": {
    "sections": [
      "Guia (entrada, todos usuários)",
      "Sistema (conceitual)",
      "Manuais (operacional)",
      "API (técnico)",
      "Dev (técnico avançado)",
      "Status (operações)",
      "Changelog (histórico)"
    ],
    "within_section": "order field no frontmatter ou posição no array",
    "auto_generated": "Starlight gera baseado em filesystem se não especificado"
  }
}
```

## Collapse Behavior

```json
{
  "collapse_rules": {
    "top_level": "Geralmente expanded (collapsed: false)",
    "subsections": "Collapsed por padrão exceto seção ativa",
    "current_page": "Expande automaticamente para mostrar página atual",
    "persistence": "Starlight persiste estado em localStorage"
  }
}
```

## Filtragem por Role

O sidebar padrão do Starlight não suporta filtragem por role. Para implementar, usar componente customizado que:

```json
{
  "role_filtering": {
    "method": "Override do componente Sidebar do Starlight",
    "logic": [
      "Ler Astro.locals.user.roles",
      "Filtrar items onde user tem pelo menos uma role permitida",
      "Renderizar sidebar filtrado"
    ],
    "fallback": "Se não autenticado, mostrar apenas seções públicas",
    "note": "Seção 'guia' é visível para todos usuários autenticados"
  }
}
```

## Responsividade

```json
{
  "responsive_behavior": {
    "desktop": "Sidebar fixo à esquerda, sempre visível",
    "tablet": "Sidebar colapsável, toggle button no header",
    "mobile": "Sidebar como drawer overlay, hamburger menu"
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
