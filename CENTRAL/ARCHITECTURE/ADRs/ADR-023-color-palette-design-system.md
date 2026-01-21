---
status: rejected
updated: 2026-01-21
description: "Nao e decisao arquitetural. Design system pertence a CENTRAL/DESIGN-SYSTEM, nao ADRs."
---

# ADR-023: Paleta de Cores e Design System CARF

Decisão arquitetural definindo paleta de cores oficial do projeto CARF composta por três cores primárias institucionais amarelo #FFCD07, verde #15981C e azul #3872C6 representando respectivamente energia/atenção, natureza/aprovação e confiança/tecnologia, complementadas por verde escuro institucional #2C5F2D usado em backgrounds de branding e vermelho accent #E63946 para elementos de destaque como linhas verticais e separadores visuais, garantindo identidade visual consistente entre todos os sistemas GEOWEB ADMIN REURBCAD MOBILE KEYCLOAK e materiais de comunicação.

Cores primárias definidas como amarelo #FFCD07 (RGB 255,205,7) aplicado em elementos decorativos destacados banners alertas informativos badges de status pendente indicadores visuais de atenção call-to-action secundários, verde #15981C (RGB 0,190,11) aplicado em indicadores de sucesso aprovação validação correta status ativo elementos positivos confirmação de ações completadas, azul #3872C6 (RGB 56,114,198) aplicado em links interativos elementos clicáveis informações contextuais navegação secundária elementos decorativos de suporte visual fundo de painéis informativos, formando tríade vibrante com contraste adequado WCAG 2.1 AA quando combinadas com backgrounds apropriados.

Verde institucional #2C5F2D (RGB 44,95,45) utilizado como cor de background principal em painéis de branding headers de login sidebars institucionais botões primários de ação principal representando identidade visual governamental municipal transmitindo seriedade confiança institucionalidade, variante escura #1A3D1B para hover states gradients profundidade visual, ambos derivados de verde tradicional brasileiro garantindo reconhecimento imediato como sistema oficial de prefeitura.

Escala de cinzas seguindo Tailwind CSS para consistência com shadcn/ui e design system compartilhado usando gray-100 #F7F7F7 backgrounds sutis cards áreas de conteúdo, gray-300 #D1D5DB borders inputs separadores disabled states, gray-500 #6B7280 placeholders texto secundário labels de menor importância, gray-700 #374151 texto de labels corpo secundário ícones ativos, gray-900 #111827 títulos headings texto principal alto contraste, white #FFFFFF backgrounds principais cards formulários áreas de foco.

CSS Variables implementadas em todos projetos frontend e Keycloak themes através de :root definindo --color-yellow #FFCD07 --color-green #15981C --color-blue #3872C6 --color-primary #2C5F2D --color-primary-dark #1A3D1B permitindo theming consistente hot-reload de cores em desenvolvimento futuro suporte a dark mode sem refatoração, Tailwind CSS configurado com extend colors mapeando variáveis para classes utilitárias bg-carf-yellow text-carf-green border-carf-blue.

Aplicação em Keycloak login theme usa verde institucional #2C5F2D como background principal do painel de branding, elemento decorativo amarelo #FFCD07 no topo (border-radius orgânico), elemento decorativo azul #3872C6 na base (border-radius orgânico), logotipo "CARF" centralizado em branco sobre verde, formulário em fundo branco com botão verde institucional mantendo consistência com identidade.

Acessibilidade verificada através de contrast ratio mínimo 4.5:1 para texto normal 3:1 para texto grande conforme WCAG 2.1 AA, verde institucional #2C5F2D sobre branco atinge ratio 7.2:1 excelente, amarelo #FFCD07 não usado para texto (apenas decoração) por baixo contraste, azul #3872C6 sobre branco atinge ratio 4.8:1 adequado para texto de link, cores não transmitem informação sozinhas sempre acompanhadas de texto ou ícone garantindo daltonismo-friendly.

Referências implementação Keycloak theme [06-login-theme-carf](../../../PROJECTS/KEYCLOAK/DOCS/FEATURES/06-login-theme-carf.md), Tailwind config @carf/ui shared library, Figma design system (link externo), WCAG 2.1 AA contrast guidelines w3.org/WAI/WCAG21/Understanding/contrast-minimum.
