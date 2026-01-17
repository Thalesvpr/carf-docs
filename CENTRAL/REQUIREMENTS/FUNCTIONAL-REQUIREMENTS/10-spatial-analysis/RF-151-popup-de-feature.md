---
modules: [GEOWEB]
epic: compatibility
---

# RF-151: Popup de Feature

Este requisito estabelece que ao clicar em feature renderizada no mapa o sistema deve exibir popup ou tooltip contendo informações detalhadas da feature incluindo atributos e opções de ação permitindo acesso rápido a dados e funcionalidades contextuais sem navegar para outra tela, onde popup é overlay posicionado próximo à feature clicada. O sistema deve exibir popup ao clicar em qualquer feature visível no mapa onde clique pode ser em geometria de ponto linha ou polígono e popup aparece imediatamente adjacente ao local clicado ou ancorado à geometria, permanecendo visível até usuário fechar explicitamente ou clicar em outra feature ou área vazia do mapa. O conteúdo do popup deve incluir atributos formatados da feature apresentando pares chave-valor das properties customizadas em layout organizado e legível, onde formatação pode incluir labels descritivas para campos conversão de valores para formatos amigáveis e agrupamento lógico de informações relacionadas. O popup deve incluir botões de ação contextuais para edição e exclusão quando usuário tem permissões apropriadas, onde botões acionam modais ou modos de edição inline permitindo modificar feature diretamente a partir do popup sem necessidade de localizar feature em listagem separada. A interface do popup deve ser responsiva adaptando tamanho e posicionamento conforme conteúdo e espaço disponível no viewport evitando que informações fiquem cortadas ou inacessíveis. A funcionalidade é implementada exclusivamente no módulo GEOWEB através de event handlers de clique no mapa.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
