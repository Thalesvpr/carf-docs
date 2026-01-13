---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: maintainability
---

# RF-112: Ordenar Fotos

Este requisito especifica que usuários devem poder reordenar fotos em galerias através de interface drag and drop intuitiva, onde o sistema mantém ordem personalizada definida pelo usuário ao invés de ordenação fixa por data ou nome. O modelo de dados deve incluir campo display_order numérico inteiro em cada registro de foto, permitindo ordenação explícita onde valores menores aparecem primeiro, garantindo que a sequência seja preservada de forma determinística e consistente. A interface deve implementar funcionalidade drag and drop permitindo que usuários cliquem e arrastem miniaturas para reposicioná-las, onde o sistema recalcula automaticamente os valores de display_order das fotos afetadas após cada movimento, atualizando múltiplos registros se necessário para manter sequência contígua. A persistência da ordem deve ser imediata, salvando alterações no backend assim que usuário solta a foto na nova posição, com feedback visual confirmando que a mudança foi salva com sucesso. Esta funcionalidade é particularmente útil para organizar documentação fotográfica em sequência lógica de apresentação ou análise, independente da ordem cronológica de captura. O módulo GEOWEB deve fornecer interface drag and drop nas telas de galeria com validações adequadas.

---

**Última atualização:** 2025-12-30