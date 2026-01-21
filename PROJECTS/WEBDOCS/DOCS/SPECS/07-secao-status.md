---
status: review
updated: 2026-01-21
---

# Seção Status

Seção /status/ exibe disponibilidade em tempo real dos serviços CARF permitindo usuários verificarem se sistema está operacional. Página única com componente dinâmico.

Estrutura é página única status.astro em src/pages/ (não em content/) pois requer SSR para fetch de health checks em tempo real. Não usa Content Collections pois conteúdo é gerado dinamicamente.

Componentes da página incluem grid de status mostrando cada serviço monitorado com indicador visual (verde/amarelo/vermelho/cinza), nome, latência, e timestamp do último check. Seção de histórico lista incidentes passados ordenados por data. Banner de atualização automática permite polling opcional.

Serviços monitorados são configurados em src/config/services.ts definindo id, nome amigável, URL do health endpoint, e timeout. Adicionar novo serviço requer apenas entrada neste arquivo.

Histórico de incidentes mantido em collection incidents do Decap CMS permite equipe documentar manutenções e falhas. Frontmatter inclui date, status (investigating, identified, monitoring, resolved), services afetados como array, e description em Markdown.

Acesso é público pois transparência sobre disponibilidade é importante para usuários. Não requer autenticação. URLs de health endpoints não são expostas ao cliente, apenas resultados agregados.

Cache de health checks em memória por 30 segundos evita sobrecarga nos serviços monitorados quando múltiplos usuários acessam página simultaneamente.
