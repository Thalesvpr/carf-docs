---
modules: [GEOWEB, REURBCAD]
epic: units
---

# US-049: Trabalhar Sem GPS

Como agente de campo, quero cadastrar unidades sem sinal GPS disponível para que o trabalho continue mesmo em condições adversas de sinal, onde a funcionalidade deve permitir desenho manual de geometrias diretamente no mapa através de toques ou traçado com dedo, garantindo exibição clara de alerta "Sem GPS" para consciência do agente sobre qualidade reduzida dos dados, permitindo que geometrias aproximadas sejam aceitas pelo sistema com marcação adequada para posterior refinamento. Esta funcionalidade é implementada pelo módulo GEOWEB na interface mobile com ferramentas alternativas de desenho quando GPS indisponível, integrada ao UC-004 (Cadastrar Unidade no Campo) para garantir continuidade operacional. Os critérios de aceitação incluem detecção automática de indisponibilidade ou baixa qualidade de sinal GPS (precisão maior que 20 metros ou sem sinal), exibição de alerta visual destacado "Trabalhando sem GPS - Geometria aproximada" quando em modo degradado, disponibilização de ferramenta de desenho manual permitindo criar polígono através de toques sequenciais no mapa para marcar vértices, ferramenta alternativa de traçado livre permitindo desenhar perímetro com dedo sobre o mapa, validação básica de geometrias desenhadas manualmente (mínimo 3 pontos sem auto-interseção área mínima 4m²), marcação automática de unidades cadastradas sem GPS com flag gps_accuracy=NULL ou similar, indicação visual diferenciada no mapa para unidades com geometria aproximada versus GPS preciso, e possibilidade de refinar geometria posteriormente quando GPS de melhor qualidade estiver disponível. A rastreabilidade conecta esta user story ao UC-004 (Cadastrar Unidade no Campo), garantindo capacidade de trabalho mesmo em condições ambientais ou técnicas adversas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
