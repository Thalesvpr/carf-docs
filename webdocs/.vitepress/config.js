import { defineConfig } from 'vitepress'

export default defineConfig({
  base: "/carf-webdocs/",
  title: 'CARF - Documentação',
  description: 'Sistema de Regularização Fundiária Urbana conforme Lei 13.465/2017',
  ignoreDeadLinks: true,

  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      {
        text: '📋 Product/Business',
        link: '/docs/',
        activeMatch: '/docs/'
      },
      {
        text: '💻 Desenvolvedores',
        link: '/dev/',
        activeMatch: '/dev/'
      }
    ],

    sidebar: {
      // Sidebar para área Product/Business (/docs/)
      '/docs/': [
        {
          text: '📋 Product & Business',
          items: [
            { text: 'Visão Geral', link: '/docs/' }
          ]
        },
        {
          text: 'Requisitos',
          collapsed: false,
          items: [
            { text: 'Requisitos Funcionais', link: '/docs/requisitos/' }
          ]
        },
        {
          text: 'Funcionalidades',
          collapsed: false,
          items: [
            { text: 'Casos de Uso', link: '/docs/funcionalidades/' }
          ]
        },
        {
          text: 'Planejamento',
          collapsed: false,
          items: [
            { text: 'Roadmap', link: '/docs/roadmap/' },
            { text: 'Processos REURB', link: '/docs/processos/' }
          ]
        },
        {
          text: 'Links Úteis',
          items: [
            { text: '💻 Ver Docs Técnicas', link: '/dev/' },
            { text: '🏠 Voltar ao Início', link: '/' }
          ]
        }
      ],

      // Sidebar para área Desenvolvedores (/dev/)
      '/dev/': [
        {
          text: '💻 Desenvolvedores',
          items: [
            { text: 'Visão Geral', link: '/dev/' }
          ]
        },
        {
          text: 'Getting Started',
          collapsed: false,
          items: [
            { text: 'Setup Inicial', link: '/dev/setup/' }
          ]
        },
        {
          text: 'Arquitetura',
          collapsed: false,
          items: [
            { text: 'Visão Geral', link: '/dev/arquitetura/' }
          ]
        },
        {
          text: 'API',
          collapsed: false,
          items: [
            { text: 'API Reference', link: '/dev/api/' }
          ]
        },
        {
          text: 'Database',
          collapsed: false,
          items: [
            { text: 'Schema & Migrations', link: '/dev/database/' }
          ]
        },
        {
          text: 'Guias',
          collapsed: false,
          items: [
            { text: 'Guias Técnicos', link: '/dev/guias/' }
          ]
        },
        {
          text: 'Links Úteis',
          items: [
            { text: '📋 Ver Requisitos', link: '/docs/requisitos/' },
            { text: '🏠 Voltar ao Início', link: '/' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Thalesvpr/carf-docs' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      message: 'Sistema CARF - Regularização Fundiária Urbana',
      copyright: 'Copyright © 2026 - Uso Restrito'
    }
  },

  markdown: {
    lineNumbers: true
  }
})
