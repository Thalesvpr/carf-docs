# ANNOTATIONS

Entity sistema anotações colaborativas do GEOAPI permitindo usuários adicionarem comentários observações entidades durante workflow facilitando comunicação equipe e registro decisões. Annotation usa polymorphic relationship EntityType enum (UNIT/HOLDER/LEGITIMATION/COMMUNITY/DOCUMENT) e EntityId Guid identificando alvo, AnnotationType enum (COMMENT/ISSUE/RESOLUTION/NOTE) categorizando natureza, Content texto markdown suportando formatação básica links, CreatedBy AccountId autor permitindo mentions notifications, ParentAnnotationId nullable para threading replies nested conversations, Priority enum (LOW/NORMAL/HIGH/URGENT) sinalizando atenção requerida, Status enum (OPEN/RESOLVED/CLOSED) rastreando lifecycle issues identificados e Attachments lista DocumentIds referenciando fotos screenshots evidências. Casos uso incluem field agent anotando Issue foto unidade borrada requerendo nova coleta, analista comentando requisitando documentação adicional titular com mention notificando via SignalR, supervisor adicionando Note justificando decisão atípica aprovação legitimação fora padrões habituais auditoria futura e coordenador marcando Resolution após correção implementada fechando loop feedback garantindo comunicação assíncrona rastreável persistente evitando informações perdidas conversas informais email chat.

## Arquivos

- **[11-annotation.md](./11-annotation.md)** - Anotação comentário colaborativo entidades

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (1 arquivo)

| ID | Titulo |
|:---|:-------|
| [11-annotation](./11-annotation.md) | Annotation |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
