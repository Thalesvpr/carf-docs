---
modules: [GEOWEB, GEOGIS]
epic: scalability
---

# UC-007-FE-002: Geometrias Inválidas

Fluxo de exceção do UC-007 Exportar Dados Geográficos ocorrendo no passo 11.3 durante formatação de dados quando worker processa cada registro iterando array de unidades e tenta serializar geometria para formato destino mas detecta geometria inválida usando PostGIS ST_IsValid retornando false indicando problemas topológicos como auto-interseções (polígono cruzando a si próprio formando laço), anéis não fechados (último vértice diferente do primeiro), geometrias degeneradas (polígono com área zero colapsado em linha), ou coordenadas NaN/Infinity corrompidas por bug em cadastro ou importação anterior, tipicamente causado por desenho manual incorreto no mapa onde usuário clicou vértices duplicados ou muito próximos gerando polígono mal formado, ou importação de Shapefile externo com topologia corrupta não validada previamente, sistema ao detectar invalidade via ST_IsValid loga warning em sistema de logging incluindo unit_id geometry_wkt e motivo específico retornado por ST_IsValidReason (ex: "Self-intersection at point (123.45 -67.89)") para debug posterior, incrementa contador de registros ignorados skipped_count inicializado em zero no início do job, pula registro atual não incluindo na exportação evitando corromper arquivo final com geometria quebrada que falharia ao abrir em QGIS ou causaria crash em ArcGIS, continua processando próximos registros do array normalmente sem abortar job completo permitindo exportar unidades válidas ao invés de falhar tudo por alguns registros problemáticos, ao finalizar job verifica if (skipped_count > 0) adiciona propriedade warnings ao resultado do job armazenando array de mensagens descritivas, notificação enviada ao usuário inclui ícone amarelo warning e mensagem adicional "Atenção: 12 registros ignorados por geometria inválida. Consulte o log de exportação para detalhes" com link Ver Detalhes abrindo modal listando unit_ids afetados com código e endereço permitindo ANALYST identificar unidades problemáticas, ANALYST pode então acessar cada unidade listada no warning abrir formulário de edição redesenhar geometria corretamente garantindo ST_IsValid=true ao salvar via trigger de validação, e re-exportar dataset completo agora com todas unidades incluídas, garantindo robustez do processo de exportação que não trava por dados ruins herdados de migrações ou cadastros antigos enquanto fornece feedback transparente sobre qualidade de dados permitindo limpeza gradual do dataset.

**Ponto de Desvio:** Passo 11.3 do UC-007 (durante iteração de formatação)

**Retorno:** Registros inválidos ignorados, exportação continua, warning incluído na notificação

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
