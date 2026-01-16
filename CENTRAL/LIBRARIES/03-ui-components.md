# @carf/ui

Biblioteca de componentes React reutilizáveis baseada em shadcn/ui com Tailwind CSS, oferecendo UI consistente e acessível para todas as aplicações frontend CARF.

## Conteúdo

Componentes shadcn/ui customizados incluem primitivos como Button, Input, Select, Dialog, Toast, Table e Form com tema CARF aplicado, variantes de cor e tamanho padronizadas, e comportamentos consistentes de loading e disabled states.

Componentes específicos CARF implementam UnitCard exibindo dados de unidade habitacional com status visual e ações contextuais, HolderCard mostrando informações de titular com foto e documentos vinculados, MapView renderizando mapa interativo Leaflet com layers de unidades e comunidades, CommunitySelector para busca e seleção de comunidades com autocomplete, e StatusBadge indicando visualmente estados de workflow com cores semânticas.

Dark mode support implementa alternância automática baseada em preferência do sistema ou manual via toggle, com todas as cores adaptando-se corretamente incluindo mapas e gráficos. Acessibilidade WCAG 2.1 AA garante contraste mínimo de 4.5:1, navegação completa por teclado, labels apropriados para screen readers e focus indicators visíveis.

Storybook documentation apresenta cada componente isoladamente com controles interativos para props, exemplos de uso em diferentes estados e documentação de API inline.

## Instalação

Executar comando bun add @carf/ui @carf/tscore instalando biblioteca de componentes com dependência core, configurando tailwind.config.js para importar preset CARF e adicionando provider de tema no root da aplicação.

## Documentação Técnica

Documentação de implementação disponível em PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/ contendo catálogo de componentes, guia de theming e Storybook.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
