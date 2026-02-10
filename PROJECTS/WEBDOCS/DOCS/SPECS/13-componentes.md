---
type: leaf
status: review
updated: 2026-02-07
---

# Componentes Customizados

Componentes Astro customizados usados no WEBDOCS alem do Starlight.

## StatusGrid e ServiceCard

StatusGrid em src/components/status/StatusGrid.astro exibe grid de cards com status dos servicos. Prop services (Service array obrigatorio). Service possui name, url, timeout (default 5000ms) e critical. SSR com Promise.allSettled, polling a cada 30s via client:idle.

| Estado | Cor | Label |
|--------|-----|-------|
| online | verde | Operacional |
| offline | vermelho | Indisponivel |
| degraded | amarelo | Degradado |
| unknown | cinza | Desconhecido |

ServiceCard renderiza card individual com props name, status, latency, lastCheck e critical (badge Critico se true e offline).

## Banner e YouTubeEmbed

Banner em src/components/content/Banner.astro para notificacao global. Props: type (info/warning/error), message, dismissible (default true), id (localStorage com TTL 24h). Cores: info azul, warning amarelo, error vermelho.

YouTubeEmbed para video responsivo 16:9. Props: videoId (11 chars), title (acessibilidade), startTime opcional. Lazy loading com thumbnail, usa youtube-nocookie.com.

## SwaggerUI

Em src/components/content/SwaggerUI.astro. Prop specUrl obrigatoria, defaultExpand (none/list/full default list). SSR fetch com cache 5min, injeta Authorization do usuario, hidratacao client:visible.

## Auth Components

LoginButton em src/components/auth/LoginButton.astro com prop returnUrl. Redirect para /auth/login.

UserMenu em src/components/auth/UserMenu.astro com prop user (name, email, roles). Avatar com iniciais, dropdown Perfil/Configuracoes/Logout, hidratacao client:idle.

ProtectedContent wrapper com requiredRoles (array) e fallback opcional. Verifica Astro.locals.user.roles, precisa pelo menos uma role.

## Integracao @carf/ui

Toast, Dialog e DropdownMenu da @carf/ui usados via Astro React com hidratacao client:idle. Componentes pesados usam client:visible.
