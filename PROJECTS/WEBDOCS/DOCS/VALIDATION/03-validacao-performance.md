---
status: review
updated: 2026-01-21
---

# Validação de Performance

Lighthouse CI mede performance de páginas chave garantindo que site permanece rápido conforme conteúdo cresce.

Métricas monitoradas incluem Performance Score (target 90+), First Contentful Paint abaixo de 1.5s, Largest Contentful Paint abaixo de 2.5s, Time to Interactive abaixo de 3.5s, Cumulative Layout Shift abaixo de 0.1, e Total Blocking Time abaixo de 200ms.

Configuração em lighthouserc.js define URLs a testar, thresholds por métrica, número de runs para média (3), e device simulado (mobile 4G). Configuração de throttling simula condições reais de usuários em conexões médias.

Páginas testadas incluem home (mais visitada), página de manual típica (representa maioria do conteúdo), página com diagramas Mermaid (potencial peso), e página de busca (componente interativo). Sample representativo sem testar todas páginas.

Assertions definem comportamento de CI: preset desktop para garantir performance em desktop, preset mobile com thresholds mais tolerantes reconhecendo limitações de dispositivos móveis. Falha em assertions críticas bloqueia deploy.

Budget de recursos define limites para assets: total JavaScript abaixo de 200KB, total CSS abaixo de 50KB, total de imagens por página abaixo de 500KB. Exceder budgets gera warning para investigação.

Relatório de tendência armazenado em servidor Lighthouse CI (ou GitHub Gist) permite visualizar performance ao longo do tempo. Regressões significativas disparam alerta para investigação de causa (novo componente, imagem grande, etc).
