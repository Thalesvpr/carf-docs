# GEOGRAPHIC

Validações geográficas do CARF. coordinates-validation.md valida latitude -90 a +90, longitude -180 a +180, coordenadas dentro bounds Brasil verificando se ponto está contido no polígono de fronteira do Brasil. polygon-validation.md valida topologia geométrica (sem auto-interseção, buracos válidos, anel externo sentido horário), cálculo de área > 20m² (área mínima), cálculo de área < 250m² para REURB-S ou < 500m² para REURB-E. overlap-detection.md valida detecção de sobreposição espacial entre polígonos retornando conflitos, permitindo tolerância para pequenos gaps < 0.5m². topology-validation.md verifica gaps entre unidades adjacentes na mesma comunidade, slivers (polígonos muito finos), dangles (arestas não conectadas). Implementadas via funções espaciais do banco de dados chamadas de serviços de domínio ou restrições de banco.

---

**Última atualização:** 2025-01-05
**Status do arquivo**: Review
