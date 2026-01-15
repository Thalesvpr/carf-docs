---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# RF-109: Tipos de Foto

Este requisito estabelece que o sistema deve suportar categorização de fotos através de tipos predefinidos, onde cada foto uploaded pode ser classificada como Fachada Interior Terreno Documentos ou Outro, permitindo organização e filtragem eficiente do acervo fotográfico. O sistema deve implementar enum de tipos no modelo de dados garantindo valores consistentes e validados, onde o campo photo_type é obrigatório no momento do upload ou pode ser atribuído posteriormente através de edição. A interface deve disponibilizar filtros por tipo em telas de listagem e galeria, permitindo que usuários visualizem apenas fotos de categorias específicas, facilitando localização de imagens durante processos de análise e documentação de imóveis ou terrenos. O tipo Fachada é utilizado para fotos externas frontais de edificações, Interior para ambientes internos, Terreno para áreas sem construção, Documentos para fotografias de certidões escrituras ou papéis, e Outro para casos não enquadrados nas categorias principais. A funcionalidade deve estar disponível no módulo GEOAPI através de validações e filtros nos endpoints de fotos, permitindo queries eficientes por tipo.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
