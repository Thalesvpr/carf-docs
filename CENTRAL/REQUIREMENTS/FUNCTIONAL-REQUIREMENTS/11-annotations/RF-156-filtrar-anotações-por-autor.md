---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# RF-156: Filtrar Anotações por Autor

Este requisito especifica que o sistema deve permitir filtrar visualização de anotações no mapa e listagens baseado em autoria permitindo que usuários vejam apenas suas próprias anotações ou todas as anotações de todos os usuários conforme preferência ou necessidade de análise, onde filtro controla escopo de anotações exibidas sem afetar dados subjacentes. A interface deve fornecer toggle switch ou selector com opções Minhas anotações e Todas permitindo alternar rapidamente entre modos de visualização, onde Minhas anotações filtra para exibir apenas anotações criadas pelo usuário atualmente logado identificado por user_id e Todas exibe anotações de todos os usuários do tenant ou comunidade conforme escopo de dados. O sistema deve implementar filtro por user_id no backend através de query parameter ou filtro de sessão comparando campo author_id ou created_by_user_id de cada anotação com identificador do usuário logado, onde query retorna apenas registros correspondentes ao critério de autoria selecionado garantindo que dados filtrados não vazem para cliente. A exibição condicional deve aplicar filtro tanto na renderização de marcadores no mapa quanto em listagens de anotações em painéis ou tabelas, mantendo consistência entre diferentes visualizações e garantindo que usuário veja conjunto coerente de dados independente de interface. O estado do filtro deve ser persistido na sessão do usuário mantendo preferência entre navegações. A funcionalidade deve estar disponível nos módulos GEOWEB e GEOAPI.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
