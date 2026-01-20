---
status: review
updated: 2026-01-17
---

# Sidebar e Navegação

Configuração de navegação define estrutura do sidebar, ordem de seções, labels customizados, e ícones para melhor orientação do usuário.

Configuração em astro.config.mjs dentro de starlight.sidebar define array de grupos e links. Cada grupo tem label visível, items com páginas, e opcionalmente collapsed para iniciar recolhido.

Ordem de seções no sidebar reflete jornada típica do usuário: Guia primeiro para orientação inicial, Sistema para contexto, Manuais para uso prático, API para integrações, Status para verificar disponibilidade, e Changelog para novidades. Seção Dev aparece apenas para usuários autenticados com role.

Labels usam português brasileiro com terminologia familiar aos usuários. Evitar abreviações ou termos técnicos no menu. Label pode diferir do title do documento quando versão mais curta melhora navegação.

Ícones opcionais antes do label usando Starlight icon syntax melhoram escaneabilidade. Usar ícones consistentes: livro para guia, engrenagem para sistema, mãos para manuais, plug para API, coração para status, lista para changelog.

Badges indicam conteúdo especial: "Novo" para funcionalidades recentes por 30 dias, "Beta" para features em teste, e "Dev" para seções protegidas. Badge definido no frontmatter da página.

Autogenerate em grupos gera links automaticamente de estrutura de pastas. Útil para seções com muitas páginas como manuais. Ordem controlada por campo order no frontmatter de cada página.

Responsividade mantém sidebar visível em desktop e transforma em menu hamburger em mobile. Breadcrumbs acima do conteúdo orientam localização atual na hierarquia.
