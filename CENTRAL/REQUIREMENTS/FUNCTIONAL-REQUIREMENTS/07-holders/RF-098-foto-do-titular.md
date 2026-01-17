---
modules: [GEOWEB, REURBCAD]
epic: performance
---

# RF-098: Foto do Titular

O sistema deve permitir upload de foto 3x4 de titulares tipo PESSOA_FISICA para identificação visual nos cadastros, onde interface oferece funcionalidade de crop e redimensionamento permitindo que usuário ajuste enquadramento da imagem após upload garantindo formato adequado tipo retrato mesmo quando foto original possui orientação ou proporção diferente. A ferramenta de crop apresenta preview em tempo real mostrando como foto ficará após aplicação do corte e redimensionamento, além de guias visuais indicando área recomendada para enquadramento de rosto garantindo uniformidade visual entre fotos de diferentes titulares. A foto processada é armazenada em resolução otimizada (exemplo 300x400 pixels) balanceando qualidade visual com eficiência de armazenamento e performance de carregamento, gerando automaticamente versões thumbnail menores para uso em listagens e previews onde resolução completa não é necessária. A interface de ficha de titular exibe foto em destaque facilitando identificação visual rápida especialmente útil em contexto de trabalho de campo onde agentes podem precisar reconhecer titulares pessoalmente, além de foto ser incluída em documentos gerados como fichas cadastrais e certificados. Implementado nos módulos GEOWEB e REURBCAD com prioridade Could-have, este recurso adiciona dimensão visual ao cadastro humanizando registros e facilitando identificação presencial durante operações de campo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
