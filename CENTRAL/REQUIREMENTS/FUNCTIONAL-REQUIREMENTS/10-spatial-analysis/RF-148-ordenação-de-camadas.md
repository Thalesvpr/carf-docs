---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# RF-148: Ordenação de Camadas

Este requisito especifica que usuários devem poder reordenar camadas no painel de controle de layers modificando ordem de empilhamento que afeta Z-index de renderização no mapa, onde camadas no topo da lista são renderizadas sobre camadas inferiores permitindo controle sobre visibilidade e sobreposição de informações espaciais. A interface deve implementar funcionalidade drag and drop no painel de camadas permitindo que usuário clique e arraste layer para nova posição na lista, onde durante arrasto sistema fornece feedback visual mostrando posição de inserção atual através de linha indicadora ou highlight da posição alvo. O modelo de dados deve incluir campo display_order numérico inteiro em cada camada armazenando ordem de exibição explícita, onde valores menores indicam camadas base que devem ser renderizadas primeiro e valores maiores representam overlays renderizados por cima, garantindo ordem determinística e persistente. Quando usuário reordena camada através de drag and drop, o sistema deve recalcular automaticamente valores de display_order das camadas afetadas pela mudança incrementando ou decrementando conforme necessário para manter sequência contígua sem gaps ou duplicatas. A atualização de renderização no mapa deve ocorrer imediatamente após reordenação mostrando nova disposição de camadas sem necessidade de refresh manual, onde engine de renderização respeita ordem configurada. A funcionalidade deve estar disponível nos módulos GEOWEB através de painel interativo de camadas e GEOAPI persistindo ordem no backend.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
