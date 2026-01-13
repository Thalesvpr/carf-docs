---
modules: [GEOWEB]
epic: performance
---

# RF-104: Vincular Documento a Entidade

O sistema deve permitir vinculação polimórfica de documentos a diferentes tipos de entidades através de campos entity_type e entity_id onde entity_type especifica categoria da entidade (UNIT HOLDER COMMUNITY) e entity_id referencia identificador específico da instância vinculada. Esta arquitetura polimórfica permite que mesmo modelo de documento seja reutilizado para anexação em contextos diversos, eliminando necessidade de criar tabelas separadas para documentos de unidades, documentos de titulares e documentos de comunidades mantendo estrutura unificada e queries simplificadas. A implementação garante integridade referencial validando que entity_id referenciado realmente existe na tabela correspondente ao entity_type especificado, prevenindo vínculos órfãos que apontam para entidades inexistentes ou excluídas. Queries por entidade utilizam índices compostos em (entity_type entity_id) garantindo performance otimizada ao listar documentos de unidade específica, titular específico ou comunidade específica mesmo com milhões de documentos na base de dados. A interface de visualização de cada tipo de entidade (unidade titular comunidade) apresenta seção dedicada listando documentos vinculados àquela instância específica, permitindo upload contextual onde documentos anexados durante visualização de unidade são automaticamente vinculados àquela unidade sem necessidade de especificação manual de vínculo. Implementado no módulo GEOAPI com prioridade Must-have, este design polimórfico oferece flexibilidade e extensibilidade mantendo simplicidade de modelo de dados.

---

**Última atualização:** 2025-12-30
