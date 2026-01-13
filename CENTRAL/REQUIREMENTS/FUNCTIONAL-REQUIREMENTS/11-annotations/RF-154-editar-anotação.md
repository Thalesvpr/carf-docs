---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# RF-154: Editar Anotação

Este requisito especifica que usuários devem poder editar tanto conteúdo textual quanto posição geográfica de anotações existentes permitindo correção e atualização de notas sem necessidade de recriar, onde interface oferece edição inline para texto e movimentação de marcador para ajuste de localização. O sistema deve permitir edição inline do texto da anotação diretamente no popup ou painel de detalhes onde usuário clica no campo de texto para ativá-lo digita modificações e confirma através de blur automático ao clicar fora ou botão de salvar, garantindo processo rápido sem abertura de modais ou formulários pesados. Para ajuste de posição, o sistema deve permitir movimentação do marcador de anotação através de modo de edição onde usuário ativa edição e pode arrastar ícone da anotação para nova localização no mapa, onde nova coordenada é atualizada ao soltar marcador e mudança é persistida imediatamente ou após confirmação conforme design de interação. Todas as alterações realizadas em anotação devem gerar entradas no log de alterações vinculado à anotação registrando usuário responsável timestamp campos modificados e valores anteriores versus novos, garantindo auditoria de evolução da anotação particularmente importante quando múltiplos usuários colaboram em documentação de campo. O sistema deve validar que texto editado não seja vazio e coordenadas permaneçam dentro de bounds válidos. A funcionalidade deve estar disponível nos módulos GEOWEB e GEOAPI.

---

**Última atualização:** 2025-12-30