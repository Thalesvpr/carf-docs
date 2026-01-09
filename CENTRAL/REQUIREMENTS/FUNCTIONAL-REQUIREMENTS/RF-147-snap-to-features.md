---
modules: [GEOWEB]
epic: other
---

# RF-147: Snap to Features

Este requisito estabelece que durante edição ou criação de features o sistema deve oferecer funcionalidade de snap permitindo que vértices desenhados colem automaticamente em features existentes quando cursor se aproxima facilitando criação de topologia precisa e conectividade entre elementos geográficos, onde snap garante alinhamento perfeito sem necessidade de precisão manual pixel-perfect. O sistema deve implementar tolerância de snap configurável especificando distância em pixels dentro da qual snap é ativado, onde valor típico entre 10 e 20 pixels permite snap confortável sem ser excessivamente agressivo capturando features não intencionadas, e configuração pode ser ajustada conforme densidade de features e preferências do usuário. A interface deve fornecer indicação visual clara de snap ativado mostrando feedback imediato quando cursor entra em zona de tolerância de feature existente, onde indicação pode incluir mudança de cor do cursor highlight do vértice alvo ou linha guia conectando cursor ao ponto de snap, garantindo que usuário compreende que próximo clique resultará em snap. O sistema deve permitir ativação e desativação da funcionalidade através de toggle checkbox ou tecla modificadora como Ctrl permitindo que usuário controle quando snap está ativo, útil quando desenho intencional próximo mas não conectado a features existentes é necessário. O snap deve funcionar com vértices edges e possivelmente centroides de features existentes. A funcionalidade é implementada exclusivamente no módulo GEOWEB através de lógica de desenho interativo.

---

**Última atualização:** 2025-12-30