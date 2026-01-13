---
modules: [GEOWEB]
epic: other
---

# RF-145: Medição de Distância

Este requisito estabelece que o sistema deve fornecer ferramenta interativa de medição de distância permitindo que usuários calculem comprimentos de trajetórias ou distâncias entre pontos diretamente no mapa sem necessidade de criar features permanentes, onde medição é utilidade auxiliar para análise e planejamento. A interface deve permitir que usuário ative modo de medição e realize cliques sequenciais no mapa para marcar pontos de interesse, onde cada clique adiciona vértice à linha de medição e sistema calcula automaticamente distância acumulada do trajeto formado conectando todos os pontos na ordem clicada. O sistema deve exibir distância calculada em unidades apropriadas automaticamente selecionadas conforme magnitude, onde distâncias curtas são apresentadas em metros e longas em quilômetros, com conversão automática ao ultrapassar threshold tipicamente 1000 metros, garantindo legibilidade sem valores excessivamente grandes ou pequenos. A ferramenta deve fornecer funcionalidade de limpeza permitindo que usuário remova medição atual e inicie nova sem sair do modo de medição, através de botão ou atalho de teclado que reseta pontos marcados. A distância deve ser calculada considerando geometria geodésica da Terra para precisão em escalas maiores, utilizando funções como ST_Distance com geografia ao invés de geometria plana. A visualização deve incluir linha conectando pontos marcadores nos vértices e label flutuante ou fixo mostrando distância. A funcionalidade é implementada exclusivamente no módulo GEOWEB através de controle de mapa.

---

**Última atualização:** 2025-12-30