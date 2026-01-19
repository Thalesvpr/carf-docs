# Validação de Acessibilidade

Testes automatizados verificam conformidade WCAG 2.1 nível AA usando axe-core integrado ao pipeline de CI.

Ferramenta @axe-core/playwright executa análise de acessibilidade em páginas renderizadas durante testes e2e. Verifica contraste de cores, texto alternativo em imagens, estrutura de headings, labels em formulários, e outros critérios WCAG.

Configuração em playwright.config.ts habilita axe para todas páginas testadas. Regras customizadas podem desabilitar checks específicos quando falso positivo é confirmado. Comentário documenta justificativa para cada regra desabilitada.

Níveis de severidade incluem critical para violações graves que impedem uso (botões sem texto acessível), serious para problemas significativos (contraste insuficiente), moderate para issues que afetam alguns usuários, e minor para melhorias recomendadas.

Threshold de CI falha build em violações critical e serious. Violações moderate e minor são reportadas como warnings sem falhar build permitindo correção gradual. Objetivo é zero violações em todos níveis.

Páginas testadas incluem home, todas seções principais (guia, sistema, manuais, api), e páginas com componentes interativos (busca, navegação). Sample de páginas específicas de cada seção para cobertura representativa.

Relatório gerado em formato HTML mostra violações agrupadas por regra com screenshots e elementos afetados. Link para documentação axe explica cada regra e como corrigir. Relatório armazenado como artifact do CI para review.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
