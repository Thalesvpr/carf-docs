---
modules: [GEOWEB, REURBCAD]
epic: units
---

# RF-152: Seleção Múltipla de Features

Este requisito especifica que o sistema deve permitir seleção de múltiplas features simultaneamente através de métodos de interação intuitivos facilitando operações em lote e análises comparativas, onde usuários podem selecionar conjunto de features através de shift+click para adicionar features individualmente à seleção ou desenho de retângulo de seleção bbox que captura todas as features cujas geometrias intersectam área delimitada. A interface deve fornecer ferramenta de seleção por retângulo onde usuário arrasta cursor sobre mapa desenhando área retangular e ao soltar todas as features visíveis que intersectam bbox são adicionadas à seleção, método eficiente para capturar múltiplos elementos em região compacta sem necessidade de cliques individuais repetitivos. O sistema deve fornecer highlight visual diferenciado para features selecionadas aplicando cor borda ou opacidade distintas que permite distinguir claramente elementos selecionados de não selecionados, onde destaque permanece visível enquanto seleção está ativa e é removido ao desselecionar. O sistema deve habilitar ações em lote sobre features selecionadas incluindo exclusão múltipla que remove todas as features selecionadas após confirmação única, e edição de atributos em massa que permite modificar valor de campo específico em todas as features simultaneamente, operações úteis para manutenção e correção de dados em escala. A interface deve mostrar contador indicando quantidade de features atualmente selecionadas e botão para limpar seleção. A funcionalidade é implementada exclusivamente no módulo GEOWEB através de controles interativos de seleção.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
