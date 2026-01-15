---
modules: [GEOWEB, GEOGIS]
epic: security
---

# UC-007-FA-002: Exportar Seleção

Fluxo alternativo do UC-007 Exportar Dados Geográficos desviando no passo 3 onde ao invés de exportar todos resultados filtrados, usuário seleciona unidades específicas marcando checkboxes individuais na coluna esquerda do grid ou clicando checkbox do header para selecionar todas da página atual, contador de seleção exibe badge numérico "12 selecionadas" atualizando dinamicamente conforme checkboxes marcados desmarcados, botão Exportar padrão do toolbar superior muda label para Exportar Selecionadas (12) indicando claramente subset será exportado não total filtrado, usuário clica disparando modal de exportação com mesmas opções de formato SRID campos mas exibindo mensagem topo "Exportando 12 unidades selecionadas" confirmando escopo reduzido, ao confirmar exportação sistema aplica filtro WHERE adicional limitando query a IDs selecionados usando clause WHERE id IN (selected_ids) combinada com AND aos filtros originais garantindo apenas subset escolhido processado, útil para cenários onde ANALYST identifica visualmente no mapa ou listagem unidades problemáticas específicas (ex: 5 unidades com geometrias sobrepostas detectadas em análise prévia) e deseja exportar apenas essas para investigação detalhada em QGIS sem exportar milhares de unidades válidas poluindo análise, ou quando MANAGER precisa compartilhar com equipe externa apenas unidades de interesse específico (ex: 20 unidades aprovadas de projeto piloto) sem expor dados completos do tenant por questões de confidencialidade ou LGPD, permitindo controle granular sobre dados exportados reduzindo tamanho de arquivo economizando tempo de download processamento e storage evitando transferir gigabytes quando apenas megabytes necessários, sistema mantém seleção persistente durante navegação entre páginas do grid usando state management armazenando selected_ids em memória permitindo usuário paginar listagem marcando unidades adicionais acumulando seleção até clicar exportar.

**Ponto de Desvio:** Passo 3 do UC-007 (seleção manual ao invés de filtros automáticos)

**Retorno:** Apenas unidades marcadas são exportadas, ignorando restante dos resultados filtrados

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
