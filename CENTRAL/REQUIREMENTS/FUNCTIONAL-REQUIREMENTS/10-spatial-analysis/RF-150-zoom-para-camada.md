---
modules: [GEOWEB]
epic: usability
---

# RF-150: Zoom para Camada

Este requisito especifica que usuários devem poder acionar zoom automático para extent completo de uma camada específica permitindo navegação rápida para visualização de todas as features contidas no layer independente de localização atual do mapa, onde funcionalidade calcula bounding box total da camada e ajusta viewport para enquadrar conteúdo. O sistema deve calcular bbox da camada através de query espacial que determina extensão mínima e máxima em longitude e latitude que engloba todas as features não excluídas da layer, utilizando funções PostGIS como ST_Extent ou agregação de ST_Envelope de todas as geometrias para obter retângulo envolvente completo. Após calcular bbox, o sistema deve executar zoom com padding adequado adicionando margem ao redor do extent calculado tipicamente 10% a 20% da dimensão garantindo que features nas bordas não fiquem coladas às extremidades do viewport e visualização tenha espaço respiratório, melhorando estética e usabilidade. A transição de zoom deve incluir animação suave interpolando entre viewport atual e destino durante período curto tipicamente 500ms a 1000ms, onde movimento animado ajuda usuário manter orientação espacial compreendendo deslocamento ao invés de salto abrupto desorientador. A funcionalidade deve ser acionada através de botão ou opção de menu no item da camada no painel de layers. A implementação é exclusiva do módulo GEOWEB através de controles de navegação do mapa.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
