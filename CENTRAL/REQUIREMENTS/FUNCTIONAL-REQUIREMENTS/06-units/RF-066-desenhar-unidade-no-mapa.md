---
modules: [GEOWEB]
epic: compatibility
---

# RF-066: Desenhar Unidade no Mapa

O sistema deve permitir que usuários desenhem polígonos representando unidades habitacionais diretamente no mapa interativo da interface GEOWEB e REURBCAD, onde ferramentas de desenho incluem criação de polígonos por clique sequencial de vértices e retângulos por arrastar diagonal, facilitando representação de diferentes formas de edificação. A funcionalidade oferece opção de snap-to-grid alinhando automaticamente vértices a uma grade configurável quando ativada, auxiliando criação de polígonos regulares e geometrias alinhadas especialmente útil em contextos de parcelamento planejado. Durante e após o desenho, usuários podem editar vértices individualmente arrastando pontos existentes, adicionando novos vértices ao clicar em segmentos de linha, ou removendo vértices selecionados, garantindo ajuste preciso da geometria às características reais da edificação. O sistema valida automaticamente a geometria desenhada verificando problemas como auto-interseção (polígono que cruza a si mesmo), apresentando alertas visuais e bloqueando salvamento até que geometria seja corrigida, garantindo integridade geométrica e compatibilidade com operações espaciais subsequentes como cálculo de área e detecção de sobreposições.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
