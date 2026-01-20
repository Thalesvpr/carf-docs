---
status: review
updated: 2026-01-17
---

# Status Page

Página /status/ exibe disponibilidade em tempo real dos serviços CARF permitindo usuários verificarem se sistema está operacional antes de reportar problemas. Implementação combina checks server-side durante SSR com polling opcional client-side.

Layout apresenta card para cada serviço com indicador visual de status (verde para healthy, amarelo para degraded, vermelho para unhealthy, cinza para unknown), nome do serviço, latência do último check, e timestamp da verificação. Seção inferior mostra histórico de incidentes recentes ordenados por data.

Serviços monitorados são configurados em src/config/services.ts definindo nome, URL do health endpoint, e timeout. Configuração permite adicionar novos serviços sem modificar componente. Serviços em ambientes diferentes (dev, staging, prod) usam URLs distintas via variáveis de ambiente.

Health check executa durante SSR garantindo que página carrega com dados atuais. Componente StatusGrid.astro itera sobre serviços configurados executando fetch paralelo com Promise.allSettled para não bloquear em caso de timeout. Resultados são passados para componentes visuais.

Histórico de incidentes mantido em collection do Decap CMS permite equipe de operações documentar manutenções programadas e falhas passadas via interface visual. Frontmatter inclui data, serviços afetados, descrição, e status (investigating, identified, monitoring, resolved).

Polling client-side habilitado via checkbox "atualização automática" executa fetch a cada 30 segundos atualizando indicadores sem reload. Implementado com setInterval e fetch para endpoint API interno que retorna JSON com status atual de todos serviços.
