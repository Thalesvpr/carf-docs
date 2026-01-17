---
modules: [GEOWEB]
epic: performance
---

# RF-087: Listar Titulares

O sistema deve oferecer listagem paginada de titulares com recursos avançados de busca e filtragem, onde interface permite pesquisa textual por nome completo, CPF/CNPJ ou email encontrando titulares através de correspondência parcial (substring matching) facilitando localização mesmo quando informação completa não é conhecida. Filtros adicionais incluem tipo de titular (PESSOA_FISICA PESSOA_JURIDICA) e status (ativo inativo) permitindo segmentação da lista conforme critérios específicos de análise ou operação, onde combinação de múltiplos filtros possibilita consultas precisas como "pessoas físicas ativas com email @gmail.com". A listagem implementa paginação automática com controles de tamanho de página configurável garantindo performance adequada mesmo com dezenas de milhares de titulares cadastrados, apresentando metadados como total de registros encontrados e página atual para orientação do usuário. Capacidade de ordenação por diferentes campos (nome documento data de cadastro) através de clique em cabeçalhos de coluna permite organização flexível dos resultados conforme necessidade de cada contexto de uso. Implementado nos módulos GEOWEB e GEOAPI com prioridade Must-have, este recurso é fundamental para gestão e consulta eficiente do cadastro de pessoas vinculadas a unidades habitacionais.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
