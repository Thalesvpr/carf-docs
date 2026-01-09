---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: maintainability
---

# RF-121: Anexar Descrição a Foto

Este requisito estabelece que usuários devem poder adicionar descrições textuais ou observações a fotos para fornecer contexto documentação ou anotações sobre conteúdo da imagem, onde cada foto possui campo description opcional do tipo texto que pode ser preenchido durante upload ou adicionado posteriormente através de edição. A interface deve permitir edição inline da descrição diretamente na visualização da galeria ou detalhes da foto sem necessidade de abrir formulário separado, onde usuário clica no campo de descrição digita ou edita texto e mudança é salva automaticamente após blur ou explicitamente via botão. A descrição deve ser exibida consistentemente em todas as interfaces onde foto aparece, incluindo galeria miniatura popup no mapa e tela de detalhes completos, garantindo que contexto fornecido pelo usuário esteja sempre visível junto com imagem. O campo deve suportar texto livre com limite razoável de caracteres suficiente para observações detalhadas mas não excessivo, tipicamente entre 500 e 2000 caracteres. O sistema deve indexar descrições para permitir busca full-text onde usuários podem localizar fotos através de palavras-chave contidas nas descrições. A funcionalidade deve estar disponível nos módulos GEOWEB através de interface de edição e GEOAPI via endpoint PATCH para atualizar descrição de foto existente.

---

**Última atualização:** 2025-12-30