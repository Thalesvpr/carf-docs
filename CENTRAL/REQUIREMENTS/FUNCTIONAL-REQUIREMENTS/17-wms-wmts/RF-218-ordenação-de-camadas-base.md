---
status: rejected
description: "Formato inconsistente. RFs e RNFs misturados, duplicacao com BUSINESS-RULES. Stub de 9 linhas - incompleto."
updated: 2025-12-30
---

# RF-218: Ordenação de Camadas Base

O sistema oferece interface administrativa de ordenação de camadas base que define ordem de renderização (z-index) controlando quais camadas aparecem acima ou abaixo de outras quando múltiplas camadas estão ativas simultaneamente no mapa, aspecto crítico para garantir legibilidade e hierarquia visual apropriada onde features importantes não sejam ocultadas por camadas de contexto menos relevantes. A interface implementa funcionalidade drag-and-drop intuitiva que permite administradores reordenarem camadas simplesmente arrastando itens para cima ou para baixo em lista vertical, proporcionando experiência de usuário natural e visual que não requer conhecimento técnico de conceitos como z-index ou depth order. Ao alterar ordem visualmente através de drag-and-drop, o sistema atualiza automaticamente campo display_order em registros de banco de dados atribuindo valores numéricos sequenciais que codificam ordem estabelecida, garantindo persistência da configuração e aplicação consistente em todas as sessões de usuário independentemente de dispositivo ou navegador utilizado. As mudanças de ordenação são refletidas imediatamente no mapa de todos os usuários ativos através de mecanismo de sincronização em tempo real, onde camadas são automaticamente reorganizadas conforme nova ordem sem necessidade de recarregar página ou perder contexto de visualização atual, demonstrando ao administrador efeito imediato de suas configurações e permitindo ajustes iterativos até alcançar hierarquia visual ideal para contexto específico do projeto cadastral.
