---
type: leaf
status: review
updated: 2026-01-24
---

# StatusBadge

Componente que renderiza badge colorido baseado em status de workflow CARF.

## Props

Prop status aceita UnitStatus ou LegitimationStatus de @carf/tscore. Prop size aceita sm ou default controlando dimensoes. Prop showLabel boolean controla exibicao de texto, padrao true.

## Mapeamento de Cores

DRAFT exibe cinza para rascunho em edicao. PENDING_ANALYSIS exibe amarelo para aguardando acao. IN_REVIEW exibe azul para em processamento. APPROVED exibe verde para conclusao positiva. REJECTED exibe vermelho para rejeicao. REQUIRES_CHANGES exibe laranja para pendencia.

## Labels

Cada status mapeia para label em portugues. DRAFT exibe Rascunho. PENDING_ANALYSIS exibe Aguardando Analise. IN_REVIEW exibe Em Revisao. Prop showLabel false oculta texto mostrando apenas cor, util em espacos compactos.

## Acessibilidade

AccessibilityLabel inclui status completo mesmo quando label oculto. Cor nao e unica forma de comunicar estado. Icone opcional reforça significado visualmente. Contraste de texto sobre fundo garante legibilidade.

## LegitimationStatus

Status de legitimacao fundiaria usa mesma logica de cores. Onze estados mapeados para cores semanticas. Estados finais CERTIFICATE_ISSUED e ARCHIVED usam cores distintivas. Transicoes de workflow refletem visualmente.

## Uso em Cards

StatusBadge tipicamente posicionado no canto superior de UnitCard. Alinhamento consistente entre cards em listas. Tamanho sm para listas compactas. Tamanho default para detalhes e formularios.
