---
modules: [GEOWEB, REURBCAD]
epic: performance
---

# UC-006-FA-001: Geração Rápida (Poucos Dados)

Fluxo alternativo do UC-006 Gerar Relatório de Comunidade desviando no passo 8 onde ao invés de iniciar geração assíncrona com job em BullMQ, sistema detecta que comunidade selecionada possui menos de 100 unidades consultando query SELECT COUNT(*) FROM units WHERE community_id = $id retornando count < 100 indicando volume pequeno processável sincronamente sem bloquear interface, sistema executa geração completa inline no mesmo request HTTP processando busca de dados cálculo de estatísticas renderização de template e conversão para PDF/Excel em sequência com tempo total estimado ≤10 segundos considerando hardware típico de servidor (4 vCPU 8GB RAM), aguarda conclusão do processamento mantendo conexão HTTP aberta com timeout elevado 15 segundos, retorna arquivo gerado diretamente no response com Content-Type application/pdf ou application/vnd.openxmlformats-officedocument.spreadsheetml.sheet e Content-Disposition attachment; filename="relatorio.pdf" forçando download imediato no navegador, pula passos 9-12 do fluxo principal eliminando criação de job notificação assíncrona e armazenamento em object storage economizando latência e recursos de infraestrutura, usuário recebe arquivo instantaneamente após clicar Gerar Relatório sem precisar aguardar notificação nem acessar página separada de download, melhorando experiência para casos comuns de comunidades pequenas onde maioria das REURB Brasil envolve assentamentos 20-80 famílias segundo dados MCIDADES permitindo feedback imediato e iteração rápida ao gerar múltiplas versões ajustando parâmetros.

**Ponto de Desvio:** Passo 8 do UC-006 (verificação de tamanho antes de decisão async/sync)

**Retorno:** Arquivo retornado diretamente no response HTTP, download inicia imediatamente

---

**Última atualização:** 2025-12-30
