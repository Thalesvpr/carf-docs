---
modules: [REURBCAD]
epic: reliability
---

# RF-168: Validar Fechamento de Poligonal

O sistema implementa algoritmos para cálculo de erro de fechamento de poligonais topográficas, verificando a precisão do levantamento através da análise da discrepância entre as coordenadas inicial e final quando se percorre todos os vértices da figura fechada, conforme princípios fundamentais de topografia. O cálculo abrange tanto o erro linear, determinado pela distância euclidiana entre o ponto de partida teórico e o ponto de chegada efetivo após aplicação de todas as medições, quanto o erro angular, obtido pela diferença entre a soma dos ângulos internos medidos e o valor teórico esperado para o polígono, permitindo identificação de inconsistências sistemáticas ou aleatórias no levantamento. O sistema gera relatório detalhado de precisão contendo valores absolutos e relativos de erro, comparação com tolerâncias estabelecidas por normas técnicas brasileiras como NBR 13133 e classificação da qualidade do levantamento em categorias de precisão, fornecendo subsídios técnicos para decisão sobre aceitação ou necessidade de retrabalho em campo. Esta validação é essencial para garantir confiabilidade dos limites territoriais cadastrados, evitando disputas futuras decorrentes de imprecisões no levantamento e assegurando conformidade com requisitos técnicos exigidos por cartórios de registro de imóveis para georreferenciamento de propriedades rurais e urbanas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
