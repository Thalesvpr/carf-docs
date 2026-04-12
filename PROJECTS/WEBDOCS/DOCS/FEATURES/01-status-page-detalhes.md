---
type: leaf
status: review
updated: 2026-02-07
---

# Status Page - Detalhes Tecnicos

Interfaces de dados e detalhes de implementacao da status page. Documento complementar a 01-status-page.md.

## Interfaces de Dados

Interface Service define id (string), name (string), description (string), healthEndpoint (string ou null), timeout (number em ms), critical (boolean), checkVia opcional (string), e expectedResponse opcional com status e body.

Interface HealthCheckResult define serviceId (string), status (online, degraded, offline, ou unknown), latency (number ou null), checkedAt (Date), e error opcional (string).

Interface StatusPageData define results (array de HealthCheckResult), overallStatus (operational, degraded, ou major_outage), e lastUpdated (Date).

## Calculo de Status Geral

Status geral e major_outage se qualquer servico critico esta offline. Status e degraded se qualquer servico esta degradado mas nenhum critico offline. Status e operational caso contrario.

## Componente StatusGrid

StatusGrid.astro recebe StatusPageData como prop. Renderiza banner com status geral colorido, grid de cards com resultado por servico, e timestamp da ultima verificacao. Cores do banner mapeiam operational para verde, degraded para amarelo, major_outage para vermelho.

## Historico de Incidentes

Incidentes mantidos em collection do Decap CMS com campos data, servicos afetados, descricao, e status (investigating, identified, monitoring, resolved). Equipe de operacoes documenta manutencoes programadas e falhas via interface visual.

## Polling Client-Side

Habilitado via checkbox de atualizacao automatica. Executa fetch a cada 30 segundos para /api/health retornando JSON com status de todos servicos. StatusGrid hidrata com client:idle e inicializa useState com dados do SSR. Cards atualizam sem reload da pagina.
