# EntityType

Value object enum representando tipo de entidade em contextos polimórficos onde múltiplas entidades podem ser referenciadas pelo mesmo campo, permitindo relacionamentos genéricos mantendo type-safety. Valores possíveis são UNIT (unidade habitacional), HOLDER (titular pessoa física), COMMUNITY (comunidade/assentamento), BLOCK (quadra urbana), PLOT (lote/terreno), e SURVEY_POINT (ponto topográfico), cobrindo as principais entidades que podem receber anotações, documentos ou auditorias.

Métodos incluem GetEntityName() retornando nome da classe para reflection, GetTableName() retornando nome da tabela para queries dinâmicas, SupportsAnnotations() verificando se tipo permite anotações (todos suportam), SupportsDocuments() verificando se tipo permite upload de arquivos, RequiresGeometry() verificando se entidade deve ter geometria espacial, e ToDisplayString() retornando nome amigável para UI.

Usado em Annotation.EntityType e Annotation.EntityId criando relacionamento polimórfico permitindo anotar qualquer entidade, Document.EntityType vinculando fotos e PDFs a diferentes entidades, AuditLog.EntityType rastreando mudanças em qualquer entidade do sistema, e em queries genéricas agregando resultados por tipo mantendo flexibilidade sem perder rastreabilidade.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
