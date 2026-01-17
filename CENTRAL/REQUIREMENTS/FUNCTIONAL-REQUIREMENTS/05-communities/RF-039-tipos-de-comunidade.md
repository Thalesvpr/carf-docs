---
modules: [GEOAPI, GEOWEB]
epic: communities
---

# RF-039: Tipos de Comunidade

Sistema deve suportar tipos predefinidos de comunidade sendo Assentamento Informal para ocupações irregulares sem infraestrutura completa Reassentamento para áreas destinadas a realocação de famílias Área Urbanizada para regiões consolidadas com infraestrutura Área Rural para comunidades em zona rural ou periurbana, enum com tipos definidos implementado em backend como tipo de dado restrito (PostgreSQL ENUM ou tabela de referência) garantindo integridade referencial e consistência de valores onde apenas valores permitidos aceitos em operações de criação e edição, validação de tipo no backend obrigatória antes de persistir dados rejeitando requisições com tipos inválidos ou não reconhecidos retornando HTTP 400 Bad Request com mensagem descritiva de erro, filtros por tipo disponíveis em listagens e relatórios permitindo análise segmentada por categoria de comunidade e geração de estatísticas específicas por tipo, implementação em módulo GEOAPI com constantes ou enums exportados para frontend garantindo sincronização de valores permitidos entre camadas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
