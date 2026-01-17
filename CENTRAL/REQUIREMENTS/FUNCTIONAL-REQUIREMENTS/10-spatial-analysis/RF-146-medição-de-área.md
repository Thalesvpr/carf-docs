---
modules: [GEOWEB]
epic: units
---

# RF-146: Medição de Área

Este requisito especifica que o sistema deve fornecer ferramenta interativa de medição de área permitindo que usuários calculem superfície de polígonos desenhados diretamente no mapa para análise de extensões territoriais sem criar features permanentes, onde medição é funcionalidade auxiliar para planejamento e avaliação. A interface deve permitir que usuário ative modo de medição de área e desenhe polígono através de cliques sequenciais no mapa marcando vértices do perímetro, onde último clique fecha polígono automaticamente conectando ao ponto inicial ou através de double-click, e sistema calcula imediatamente área da superfície delimitada. O sistema deve calcular área em metros quadrados m² como unidade base e opcionalmente converter para hectares quando área excede threshold configurado tipicamente 10000 m², fornecendo representação em unidade mais apropriada conforme magnitude para facilitar interpretação por usuários acostumados com medidas de propriedades rurais ou urbanas. A exibição deve ser formatada com separadores de milhares e casas decimais adequadas garantindo legibilidade de valores grandes e precisão suficiente para valores pequenos. A ferramenta deve incluir opção de limpeza para remover polígono atual e iniciar nova medição sem desativar modo de medição. O cálculo deve considerar geometria geodésica da Terra para precisão utilizando funções como ST_Area com tipo geography do PostGIS ou cálculos equivalentes no cliente. A funcionalidade é implementada exclusivamente no módulo GEOWEB através de controle interativo do mapa.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
