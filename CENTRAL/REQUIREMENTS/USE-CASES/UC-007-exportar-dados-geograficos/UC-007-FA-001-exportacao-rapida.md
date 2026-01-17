---
modules: [REURBCAD, GEOGIS]
epic: performance
---

# UC-007-FA-001: Exportação Rápida (Poucos Dados)

Fluxo alternativo do UC-007 Exportar Dados Geográficos desviando no passo 9 onde ao invés de criar job assíncrono em BullMQ, sistema detecta que resultados filtrados contém menos de 100 registros verificando count retornado pela query inicial indicando volume pequeno processável sincronamente sem bloquear request HTTP, executa geração completa do arquivo inline no mesmo thread executando busca reprojeção formatação e serialização em sequência com tempo total estimado ≤5 segundos considerando processamento típico de geometrias simples pontos ou polígonos pequenos, mantém conexão HTTP aberta com timeout elevado 10 segundos aguardando conclusão, retorna arquivo gerado diretamente no response com headers Content-Type application/zip ou application/geo+json dependendo de formato selecionado e Content-Disposition attachment; filename="exportacao.zip" forçando download imediato no navegador do usuário, pula passos 9-12 do fluxo principal eliminando criação de job notificação assíncrona armazenamento em object storage e URL presigned economizando latência de round-trip ao storage e recursos de infraestrutura evitando overhead de BullMQ Redis serialização, usuário recebe arquivo instantaneamente após clicar Exportar vendo barra de progresso do navegador completar rapidamente e dialog de salvar arquivo abrindo automaticamente sem precisar aguardar notificação nem navegar para página de downloads, permitindo workflow ágil para casos comuns de exportações pequenas exploratórias onde ANALYST exporta subset de 10-50 unidades para validação rápida em QGIS antes de exportar dataset completo maior, melhorando experiência reduzindo fricção e acelerando iterações de análise espacial típicas de trabalho técnico diário.

**Ponto de Desvio:** Passo 9 do UC-007 (verificação de volume antes de decisão sync/async)

**Retorno:** Arquivo retornado diretamente em response, download inicia imediatamente

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
