---
modules: [GEOAPI]
epic: performance
---

# RNF-001: Tempo de Resposta - Endpoints de Leitura

Os endpoints de consulta que utilizam o método GET devem responder em até 500 milissegundos no percentil 95, garantindo uma experiência de usuário fluida e responsiva durante operações de leitura de dados. Este requisito aplica-se especificamente ao módulo GEOAPI, onde os principais endpoints de consulta incluem GET /api/units para recuperação de unidades habitacionais, GET /api/holders para consulta de possuidores e GET /api/communities para listagem de comunidades, sendo que cada um desses endpoints deve manter o tempo de resposta no percentil 95 abaixo ou igual a 500ms mesmo sob carga normal de operação. A validação deste requisito deve ser realizada através de testes de carga utilizando ferramentas especializadas como k6 ou Artillery, permitindo simular cenários realistas de uso e medir com precisão os tempos de resposta em diferentes percentis. A métrica principal de aceitação é que o percentil 95 do tempo de resposta permaneça igual ou inferior a 500 milissegundos, significando que 95% de todas as requisições devem ser completadas dentro deste limite temporal. Este requisito é classificado como Must-have devido ao seu impacto direto na percepção de performance do sistema pelos usuários finais, onde tempos de resposta superiores a 500ms podem causar frustração e reduzir a produtividade em operações de consulta frequentes. A implementação deve considerar otimizações como uso adequado de índices no banco de dados, cache de resultados para consultas frequentes, paginação eficiente de resultados e minimização de operações de I/O durante o processamento das requisições.
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
