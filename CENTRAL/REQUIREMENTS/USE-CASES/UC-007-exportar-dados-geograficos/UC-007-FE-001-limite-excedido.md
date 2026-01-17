---
modules: [GEOGIS]
epic: scalability
---

# UC-007-FE-001: Limite de Registros Excedido

Fluxo de exceção do UC-007 Exportar Dados Geográficos ocorrendo no passo 8 durante validação quando sistema verifica quantidade de registros a exportar executando COUNT query SELECT COUNT(*) FROM units WHERE <filtros> retornando count > 10000 excedendo limite técnico configurado para prevenir timeout de processamento (exportação de 50k unidades pode levar 20+ minutos travando worker), tamanho excessivo de arquivo (Shapefile com 100k registros gera ZIP de 500MB+ dificultando download e corrompendo em conexões instáveis), e sobrecarga de memória no worker Node.js que pode crashar com heap overflow ao tentar carregar dataset gigante em RAM simultaneamente, sistema detecta violação comparando count com threshold MAX_EXPORT_RECORDS=10000 definido em config, aborta criação de job antes de enfileirar evitando consumir recursos processando requisição fadada a falhar, exibe modal vermelho erro com ícone de alerta título "Limite Excedido" mensagem específica mostrando números exatos "Sua seleção contém 23.450 unidades. O limite é 10.000 registros por exportação. Refine os filtros para reduzir a quantidade" orientando usuário sobre ação corretiva necessária, oferece sugestões clicáveis inline como Filtrar por Comunidade abrindo dropdown de comunidade pré-selecionando primeira para reduzir escopo geograficamente, Filtrar por Período abrindo date picker sugerindo últimos 6 meses ao invés de all time reduzindo volume temporal, Filtrar por Status pré-marcando apenas APPROVED excluindo DRAFT e PENDING tipicamente maioria dos registros em processo, ou Exportar em Lotes orientando dividir manualmente em múltiplas exportações sequenciais aplicando filtros complementares mutuamente exclusivos (ex: primeiro comunidade A depois comunidade B), usuário ajusta filtros refinando critérios e clica Exportar novamente sistema re-executa COUNT verificando agora 8.500 registros abaixo do limite prossegue normalmente, alternativamente para casos onde usuário realmente precisa exportar dataset completo gigante sistema pode oferecer opção Solicitar Exportação Especial abrindo ticket para equipe técnica que processa manualmente em servidor dedicado com recursos maiores gerando arquivo em partes ou formato otimizado diferente (ex: GeoPackage ao invés de Shapefile suportando milhões de features) entregando via link alternativo, garantindo sistema permanece responsivo e confiável para maioria de casos de uso típicos enquanto ainda permitindo exceções justificadas com supervisão técnica.

**Ponto de Desvio:** Passo 8 do UC-007 (validação antes de criar job)

**Retorno:** Exportação bloqueada, usuário refina filtros até respeitar limite

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
