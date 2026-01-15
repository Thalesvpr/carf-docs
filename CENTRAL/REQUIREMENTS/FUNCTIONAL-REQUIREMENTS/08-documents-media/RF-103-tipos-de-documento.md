---
modules: [GEOWEB, REURBCAD]
epic: usability
---

# RF-103: Tipos de Documento

O sistema deve suportar categorização de documentos através de tipos predefinidos (RG CPF COMPROVANTE_RESIDENCIA CONTRATO PROCURACAO ESCRITURA CERTIDAO DECLARACAO OUTRO) facilitando organização e localização de documentação específica quando necessário para análise, auditoria ou geração de dossiês. A implementação utiliza enumeração armazenada no campo document_type garantindo valores consistentes e possibilitando queries eficientes para listar todos os documentos de tipo específico através de filtros baseados em categoria. A interface de upload apresenta seletor de tipo obrigatório exigindo que usuário categorize cada documento durante anexação, onde descrições claras de cada tipo orientam seleção adequada e opção OUTRO acomoda situações não contempladas pelos tipos predefinidos com campo adicional para especificação textual. Filtros por tipo de documento nas interfaces de listagem permitem visualização segmentada como "mostrar apenas comprovantes de residência" ou "listar todas as procurações" focalizando análise em subconjunto específico de documentação relevante ao contexto operacional. Implementado no módulo GEOAPI com prioridade Must-have, este recurso estrutura gestão documental através de taxonomia clara que reflete necessidades reais de processos de regularização fundiária onde diferentes categorias de documentos possuem papéis e requisitos específicos de validação, armazenamento e apresentação.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
