---
modules: [GEOWEB]
epic: performance
---

# RF-105: Listar Documentos

O sistema deve oferecer listagem de documentos com filtro por entidade permitindo visualização de todos os arquivos anexados a unidade específica, titular específico ou comunidade específica através de query baseada em entity_type e entity_id, onde interface apresenta documentos organizados cronologicamente ou por tipo conforme preferência do usuário. A listagem implementa paginação automática garantindo performance adequada mesmo quando entidade possui centenas de documentos anexados, apresentando metadados essenciais como nome do arquivo, tipo de documento (RG CPF CONTRATO etc), tamanho formatado em KB ou MB para legibilidade, e data de upload facilitando localização temporal. A interface oferece preview visual de documentos através de thumbnails para imagens e ícones tipificados para PDFs e outros formatos, permitindo reconhecimento rápido sem necessidade de abrir cada arquivo, além de funcionalidades de busca textual que filtra lista baseada em nome de arquivo ou tipo de documento. Cada item da lista apresenta ações contextuais como visualizar (abre preview ou download conforme tipo), baixar (força download ao invés de exibição inline), editar metadados (renomear alterar tipo) e excluir (com confirmação obrigatória), oferecendo gestão completa de documentação diretamente da listagem. Implementado nos módulos GEOWEB e GEOAPI com prioridade Must-have, este recurso é essencial para navegação eficiente e gestão de documentação anexada ao longo de processos de cadastramento e regularização.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
